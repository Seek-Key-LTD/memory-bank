# Situation Awareness Pipeline — 事态感知管线设计

## 背景

当前已建立 n8n workflow（OpenCode Sync — Neo4j + GraphRAG），每 5 分钟从 MinIO agents 桶拉取数据，同步到三个目标系统。需要对比三个系统的效果，确定最优的事态感知方案。

## 当前架构

```
Schedule (每5分钟)
  → Get many files (MinIO agents桶)
  → Get Script (GitLab shared-snippets: sync_all.py)
  → Run Sync (python3 sync_all.py → 并行线程 Neo4j + mem0 + GraphRAG)
  → Verify (提取 SUMMARY)
```

**Neo4j** — 知识图谱，同步在 Run Sync 脚本内完成（sync_all.py 直接写 Neo4j via HTTP API）
**mem0** → Redis Stack — 向量记忆搜索（HTTP POST 到 mem0 API: `https://mem0.capitaltrain.cn`）
**GraphRAG** — 交叉一致性校验（`POST /api/trim`，不存数据只做修剪）

## LLM 迁移（2026-06-27）

所有服务统一走 LiteLLM 网关 + StepFun `step-3.7-flash`：

| 旧方案 | 新方案 |
|---------|--------|
| LM Studio (127.0.0.1:1234, nvidia-nemotron-3-nano-4b) | LiteLLM (litellm.capitaltrain.cn) |
| mem0 → LM Studio (LLM extraction 失败) | mem0 → `infer=false`（纯向量, 不调用 LLM） |
| GraphRAG → LM Studio | GraphRAG → StepFun via LiteLLM |

✅ `response_format: json_object` 支持
✅ 无 reasoning_content 干扰
✅ API key: `sk-47318`

## 对比结果（2026-06-27 更新）

| 维度 | Neo4j | mem0 | GraphRAG |
|------|-------|------|----------|
| **查询类型** | 概念关系 (Cypher) | 向量记忆搜索 (API) | 交叉一致修剪 |
| **数据特征** | 21 Agent, 95 Section | 20 条向量记忆 | 不存数据 |
| **时效性** | 批量同步 | 实时写入 | 修剪时实时 |
| **当前状态** | ✅ 正常工作 | ✅ 修复完成 | ✅ 正常工作 |
| **优势** | 图关系推理 | agent 共享上下文 | 多agent一致性 |

### mem0 修复记录

**问题**: `infer=false` 写入后 metadata 为空字符串，Redis 读取时 `json.loads("")` 崩溃

**修复** (3处)：
1. `server.py`: `memory.search()` 返回嵌套 `{"results": {"results": [...]}}`，展平处理
2. `vector_stores/redis.py`: 添加 `_safe_parse_metadata()` 函数，try/except 兜底所有 json 解析
3. `.env`: LLM 模型 `nova2-sensenova-6.7-flash-lite` → `step-3.7-flash`

**结果**：写入 1.7s, 搜索返回带分数结果, get_all 正确列出

## GraphRAG 的定位

GraphRAG（`graphrag.capitaltrain.cn`）当前只有 `POST /api/trim`（裁剪/压缩记忆），没有摄入接口。

**建议：GraphRAG 不作为独立的数据接收端，而是作为 Neo4j 的上层处理层**，对已有的记忆做裁剪和压缩。流程：

```
MinIO → Neo4j (知识图谱) → GraphRAG (trim) → 精简记忆
MinIO → mem0 (向量记忆) → GraphRAG (trim) → 一致性校验
```

GraphRAG 当前已接入 StepFun `step-3.7-flash`，稳定工作。

## 下一步

1. ~~修通 mem0 的 HTTP POST 格式~~ ✅ 已完成（2026-06-27）
2. **综合对比测试**：三个管线全通后，做端到端对比
   - 查询速度
   - 结果准确性
   - 维护成本
3. **确定最终事态感知方案**：单管线 or 并行各司其职
4. **GitLab 同步脚本提交**：`sync_all.py` 推送至 GitLab，n8n workflow 固化