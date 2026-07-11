# 记忆银行：n8n 管线 Flow 文档

> 版本：v1.0 | 2026-07-11
> 作者：觅钥科技（Seekkey）

---

## 1 总览：四条管子

记忆银行的 n8n 管线由 4 个 workflow 组成，形成一条从原始记忆到可查询上下文的完整链路。就像 17-18 世纪的化学实验——一大堆管子连接在一起，原料从一头进去，经过层层反应，最终产物从另一头出来。

```
┌─────────────────────────────────────────────────────────────┐
│                    n8n 管线总览                               │
│                                                             │
│  Flow 1: MemoryBank-AccessLayer    (5 分钟定时)              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ MinIO(S3)│───→│ Run Sync │───→│  Verify  │              │
│  │ 拉取文件  │    │ shell脚本 │    │ 统计校验  │              │
│  └──────────┘    └──────────┘    └────┬─────┘              │
│                                       │                     │
│                    ┌──────────────────┼──────────────┐      │
│                    ▼                  ▼              ▼      │
│              ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│              │  mem0    │    │  gbrain  │    │  Redis   │  │
│              │ HTTP POST│    │  CLI exec│    │  jsonSet │  │
│              └──────────┘    └──────────┘    └──────────┘  │
│                                                             │
│  Flow 2: Unified Context — Extraction_Raw  (Webhook 触发)   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────┐ │
│  │ Webhook  │───→│ MongoDB  │───→│  Clean   │───→│Insert│ │
│  │ 接收数据  │    │ 读原始    │    │ JS 清洗   │    │写回   │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────┘ │
│                                                             │
│  Flow 3: gbrain-query  (Webhook 触发)                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Webhook  │───→│ Exec cmd │───→│ Respond  │              │
│  │ 接收查询  │    │ gbrain   │    │ 返回结果  │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                             │
│  Flow 4: Mongo Rag  (已停用，历史参考)                       │
│  ┌──────┐  ┌──────┐  ┌──────────┐  ┌──────┐  ┌─────────┐ │
│  │Chat  │→ │Agent │→ │Mongo Mem │→ │Milvus│→ │OpenRouter│ │
│  │触发   │  │      │  │聊天记忆   │  │向量库 │  │LLM      │ │
│  └──────┘  └──────┘  └──────────┘  └──────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 2 Flow 1：MemoryBank-AccessLayer（接入层）

**状态**：✅ Active
**触发**：每 5 分钟定时 + Webhook 备用
**ID**：`LxZO0lIC0i61CSpE`

### 2.1 节点链

| # | 节点 | 类型 | 做什么 |
|---|------|------|--------|
| 1 | Schedule | scheduleTrigger | 每 5 分钟触发一次 |
| 2 | Webhook | webhook | 备用手动触发 |
| 3 | Get many files | S3 (MinIO) | 从 MinIO `agents` 桶拉取文件列表 |
| 4 | Run Sync | executeCommand | 执行 `pull-codebuddy-to-pipeline.sh` |
| 5 | Verify | code (JS) | 统计同步结果（agent 数量、Neo4j/mem0/GraphRAG 状态） |
| 6a | Push to mem0 | httpRequest | POST 到 mem0 API `:8801/v3/memories/add/` |
| 6b | Push to gbrain | executeCommand | gbrain 已合并到 Run Sync 脚本中 |
| 6c | Redis | redis | jsonSet 写入状态到 Redis |

### 2.2 数据流

```
MinIO (agents 桶)
    │  S3 ListObjects
    ▼
pull-codebuddy-to-pipeline.sh
    │  输出 JSONL（每行一个 agent 或 summary）
    ▼
Verify (JS)
    │  解析 JSONL，统计 agents_synced / neo4j / mem0 / graphrag
    ▼
    ├──→ mem0 API（HTTP POST，写入向量记忆）
    ├──→ Redis（写入同步状态，供监控查询）
    └──→ gbrain（已内联到 shell 脚本）
```

### 2.3 核心脚本：pull-codebuddy-to-pipeline.sh

这个脚本是整个管线的**心脏**：

```
Step 1: 从 MinIO 拉取 Agent 会话文件
Step 2: 调用 analyze_memory.py → Neo4j（ER 图）
Step 3: 调用 GraphRAG pipeline → 向量索引
Step 4: 调用 gbrain import → PostgreSQL + pgvector
Step 5: 输出 JSONL summary → 给 Verify 节点解析
```

### 2.4 Verify 节点的输出格式

```json
{
  "timestamp": "2026-07-11T04:15:00.000Z",
  "agents_synced": 14,
  "status": "success",
  "neo4j": { "agents": 14, "memories": 847, "sections": 2341 },
  "mem0": { "agents_written": 14 },
  "graphrag": {},
  "raw": "..."
}
```

---

## 3 Flow 2：Unified Context — Extraction_Raw（统一上下文抽取）

**状态**：✅ Active
**触发**：Webhook（外部系统推送原始数据）
**ID**：`4l3PJZIy0doGUci3`

### 3.1 节点链

| # | 节点 | 类型 | 做什么 |
|---|------|------|--------|
| 1 | Webhook | webhook | 接收外部推送的原始 Agent 记忆 |
| 2 | MongoDB | mongoDb | 从 MongoDB 读取原始数据（find + query） |
| 3 | Clean | code (JS) | 削皮：字段筛选、噪声过滤、格式标准化 |
| 4 | Mongo Insert | mongoDb | 写回 MongoDB 的 `daily_*` collection |

### 3.2 数据流

```
外部 Agent / 手动推送
    │  Webhook POST
    ▼
MongoDB (agent_sessions)
    │  find + query
    ▼
Clean (JS)
    │  正向字段保留 / 负向字段丢弃 / 格式标准化
    ▼
MongoDB (daily_YYYY-MM-DD)
    │  下游按日增量处理
    ▼
Neo4j / GraphRAG / gbrain
```

### 3.3 Clean 节点的职责

这是论文中"削皮"步骤的工程实现：

1. **字段筛选**：只保留 `agent_id`、`session_id`、`content`、`timestamp`、`metadata`
2. **噪声过滤**：丢弃 `token_count`、`cost`、`system_prompt`、`raw_request/response`
3. **格式标准化**：统一时间格式、统一 content 的 Markdown 结构
4. **去重**：按 `session_id` + `timestamp` 去重

---

## 4 Flow 3：gbrain-query（查询接口）

**状态**：✅ Active
**触发**：Webhook（Agent 发起查询请求）
**ID**：`vod9a8ijIWYPTSv9`

### 4.1 节点链

| # | 节点 | 类型 | 做什么 |
|---|------|------|--------|
| 1 | Webhook | webhook | 接收查询请求（包含 query 文本 + 可选参数） |
| 2 | Exec gbrain | executeCommand | 调用 `gbrain search` 或 `gbrain ask` CLI |
| 3 | Respond | respondToWebhook | 将 gbrain 输出返回给调用方 |

### 4.2 数据流

```
Agent 查询请求
    │  Webhook POST { "query": "...", "mode": "search|ask" }
    ▼
gbrain CLI
    │  gbrain search "..." 或 gbrain ask "..."
    │  → PostgreSQL + pgvector 语义搜索
    ▼
Respond
    │  JSON 响应
    ▼
Agent 获取上下文
```

### 4.3 查询模式

| 模式 | 命令 | 用途 |
|------|------|------|
| `search` | `gbrain search "关键词"` | 语义相似度检索 |
| `ask` | `gbrain ask "问题"` | 基于上下文的问答 |
| `query` | `gbrain query "..."` | 结构化查询 |

---

## 5 Flow 4：Mongo Rag（已停用）

**状态**：❌ Inactive
**用途**：历史参考，展示了早期 RAG 架构的探索

### 5.1 节点链

| # | 节点 | 类型 | 做什么 |
|---|------|------|--------|
| 1 | When chat message received | chatTrigger | 聊天触发 |
| 2 | AI Agent | agent | n8n AI Agent |
| 3 | MongoDB Chat Memory | memoryMongoDbChat | MongoDB 作为聊天记忆存储 |
| 4 | OpenRouter Chat Model | lmChatOpenRouter | LLM 调用 |
| 5 | Milvus Vector Store | vectorStoreMilvus | 向量存储 |
| 6 | Embeddings OpenAI | embeddingsOpenAi | 向量化 |
| 7 | Reranker Cohere | rerankerCohere | 重排序 |
| 8 | Send an Email | emailSend | 邮件通知 |

### 5.2 为什么停用

这个 flow 是早期的 RAG 实验，使用了 Milvus + OpenAI Embeddings + Cohere Reranker 的经典 RAG 栈。后来被四层查询总线架构取代——mem0 替代了 Milvus 的向量检索角色，Neo4j 替代了纯向量检索的关系推理能力。

保留此 flow 作为**架构演进的考古证据**。

---

## 6 管线全景：多米诺反应

```
Agent 产生记忆
    │
    ▼ ① MinIO 暂存
    │
    ▼ ② MemoryBank-AccessLayer（每 5 分钟）
    │   pull-codebuddy-to-pipeline.sh
    │   ├── analyze_memory.py → Neo4j
    │   ├── GraphRAG pipeline → 向量索引
    │   └── gbrain import → PostgreSQL
    │
    ▼ ③ Verify 校验
    │   ├── mem0 API 写入
    │   └── Redis 状态更新
    │
    ▼ ④ Unified Context Extraction（按需）
    │   MongoDB 削皮 → 切分 → 写回 daily_*
    │
    ▼ ⑤ 下游消费
        ├── Neo4j（ER 图 / 磁力线）
        ├── GraphRAG（藏宝图 / 卫星视角）
        ├── gbrain（破坏式演绎）
        └── mem0（向量落地 / 最快路径）
```

---

## 7 比赛评审要点

> 如果参赛团队要复刻记忆银行的 n8n 管线：

### 7.1 最小可运行配置

| 组件 | 版本 | 用途 |
|------|------|------|
| n8n | 自托管或 Cloud | 工作流引擎 |
| MongoDB | 8.0+ | 原始记忆存储 + 清洗 |
| MinIO | 最新 | 原始文件暂存 |
| Neo4j | 5.x | 知识图谱 |
| mem0 | v3 API | 向量检索 |
| gbrain | CLI | PostgreSQL + pgvector |
| Redis | 7.x | 状态存储 + Pub/Sub |

### 7.2 启动顺序

1. 启动 MongoDB + MinIO + Neo4j + Redis
2. 导入 n8n workflow JSON（从 `n8n-cli workflow export` 导出）
3. 配置凭据（MongoDB 密码、MinIO key、mem0 API key）
4. 激活 MemoryBank-AccessLayer flow
5. 向 MinIO `agents` 桶推送测试数据
6. 等待 5 分钟，观察 Verify 节点输出

### 7.3 关键调试点

| 节点 | 常见问题 | 排查方法 |
|------|---------|---------|
| Get many files | MinIO 连接失败 | 检查 S3 endpoint + credentials |
| Run Sync | shell 脚本执行失败 | 查看 `/tmp/sync_debug.log` |
| Verify | JSONL 解析异常 | 检查 `raw` 字段内容 |
| Push to mem0 | HTTP 401/403 | 检查 mem0 API key |
| Clean | 字段丢失 | 检查 MongoDB query 的 projection |
