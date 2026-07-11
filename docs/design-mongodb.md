# 记忆银行：芒果（MongoDB）高层设计文档

> 版本：v1.0 | 2026-07-11
> 作者：觅钥科技（Seekkey）

---

## 1 定位：芒果在记忆银行中的角色

MongoDB（芒果）是记忆银行四层查询总线的**入口漏斗**——所有原始 Agent 记忆的第一站。

```
原始 Agent 记忆（JSON/Markdown）
        │
        ▼
  ┌──────────┐
  │  MongoDB │  ← 你在这里：削皮、切分、子弹时间
  └────┬─────┘
       │
       ├──→ Neo4j（谓词逻辑 / ER 图）
       ├──→ GraphRAG（卫星视角 / 藏宝图）
       ├──→ gbrain（破坏式演绎）
       └──→ mem0（向量落地 / 最快路径）
```

MongoDB 不做检索，不做推理。它只做一件事：**把脏数据洗干净，切成下游能吃的形状**。

---

## 2 三步管线

### 2.1 削皮（Peeling）— 字段筛选

原始 JSON 数据从各 Agent 的本地存储（SQLite / JSON 文件 / API 输出）写入 MongoDB。

**正向字段**（保留）：
- `agent_id` — 哪个 Agent 产生的
- `session_id` — 属于哪个会话
- `content` — 实际认知内容（对话、决策、状态变更）
- `timestamp` — 时间戳
- `metadata` — 来源、工具链、模型版本

**负向字段**（丢弃）：
- `token_count`、`cost` — 计费信息，不属于认知内容
- `system_prompt` — 系统提示词，噪声
- `raw_request` / `raw_response` — 原始 HTTP 报文
- 调试字段、内部 ID、trace ID

**实现**：MongoDB collection `agent_sessions`，通过 n8n 的 MongoDB 节点执行 `find` + projection，只拉取正向字段。

### 2.2 切分（Slicing）— 每日文件夹

清洗后的数据按 `timestamp` 的日期维度组织：

```
agent_sessions/
├── 2026-07-09/
│   ├── agent_ruby_session_001.json
│   ├── agent_violet_session_002.json
│   └── ...
├── 2026-07-10/
└── 2026-07-11/
```

**目的**：从混沌的 JSON 流中切分出有边界的时间片。下游的 Neo4j 和 GraphRAG 按日增量处理，避免全量扫描。

**实现**：n8n Code 节点按 `timestamp` 分组，写入 MongoDB 的 `daily_{YYYY-MM-DD}` collection。

### 2.3 子弹时间（Bullet Time）— 精细化时间序列

对于时间复杂度高的任务（如期货 5 分钟 K 线、高频交易决策），进入"子弹时间"模式：

- 以 5 分钟为窗口
- 形成精细化时间序列
- 每个窗口内的记忆被压缩为一条摘要

**实现**：MongoDB 的 Aggregation Pipeline，`$bucketAuto` 按时间窗口分桶，`$group` + `$push` 聚合。

---

## 3 部署拓扑

```
MBP (macOS)                    xgp (Proxmox LXC)
┌─────────────┐               ┌──────────────────┐
│  Agent 本地  │               │  MongoDB 8.0.26  │
│  SQLite/JSON │──mc──→ MinIO  │  (Ubuntu 26.04)  │
└─────────────┘               │  CT 100 resolute │
                              │  192.168.31.248   │
                              └────────┬─────────┘
                                       │
                              n8n (nuc:5678)
                              ├── MongoDB 节点（读）
                              ├── Code 节点（清洗）
                              └── MongoDB 节点（写回）
```

**MongoDB 实例**：
- 主机：xgp（Proxmox LXC CT 100，代号 resolute）
- 版本：MongoDB 8.0.26
- 认证：用户名/密码（凭据在 Infisical）
- 端口：27017
- Consul 注册：`mongodb` 服务，IP `192.168.31.248`

---

## 4 Collection 设计

| Collection | 用途 | 写入方 | 读取方 |
|-----------|------|--------|--------|
| `agent_sessions` | 原始 Agent 会话数据 | Agent 本地 → mc → MinIO → pull 脚本 | n8n (MongoDB 读节点) |
| `daily_YYYY-MM-DD` | 清洗后的每日数据 | n8n (MongoDB 写节点) | Neo4j 导入脚本 / GraphRAG |
| `bullet_time_*` | 子弹时间窗口聚合 | n8n Aggregation | 时间敏感任务下游 |

---

## 5 与其他组件的关系

```
MinIO ──mc──→ pull-codebuddy-to-pipeline.sh ──→ MongoDB (agent_sessions)
                                                        │
                                              n8n: Clean + Slice
                                                        │
                                              MongoDB (daily_*)
                                                        │
                                    ┌───────────────────┼───────────────────┐
                                    ▼                   ▼                   ▼
                              analyze_memory.py    GraphRAG pipeline    gbrain import
                                    │                   │                   │
                                    ▼                   ▼                   ▼
                                 Neo4j              向量索引            PostgreSQL
```

MongoDB 是**单向漏斗**：数据从 MinIO 进来，清洗后流出去，从不回流。

---

## 6 为什么选 MongoDB 而不是 PostgreSQL

| 维度 | MongoDB | PostgreSQL |
|------|---------|------------|
| Schema | Schemaless — Agent 记忆格式多变 | 需要预定义 schema |
| 嵌套文档 | 原生支持 — 对话天然是嵌套结构 | 需要 JSONB，查询复杂 |
| 写入速度 | 高 — 适合高频写入 | 中等 |
| 聚合管线 | `$bucketAuto` 天然适合时间窗口 | 需要窗口函数，更复杂 |
| 下游兼容 | Neo4j/GraphRAG 都有 MongoDB 连接器 | 同样支持 |

选择 MongoDB 的核心理由：**Agent 记忆的 schema 是不稳定的**。不同 Agent、不同会话、不同模型产生的 JSON 结构差异巨大。Schemaless 是唯一现实的选择。

---

## 7 安全考量

- **认证**：MongoDB 认证已启用，凭据存储在 Infisical
- **网络**：仅内网可达（192.168.31.248），不暴露公网
- **Consul 注册**：通过 Consul 服务发现，其他 Agent 通过服务名 `mongodb` 访问
- **备份**：Proxmox 层面快照（CT 100）

---

## 8 比赛评审要点

> 如果参赛团队要复刻记忆银行的芒果层，需要：

1. **MongoDB 8.0+** 实例（社区版即可）
2. **n8n** 工作流引擎（自托管或 n8n Cloud）
3. **MinIO** 对象存储（用于原始记忆暂存）
4. **Infisical / Vault** 密钥管理（凭据不硬编码）

最小可运行配置：一台 4C8G 的机器跑 MongoDB + n8n + MinIO 即可。
