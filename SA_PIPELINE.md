# Situation Awareness Pipeline — 事态感知管线设计

## 背景

当前已建立 n8n workflow（OpenCode Sync — Neo4j + GraphRAG），每 5 分钟从 MinIO agents 桶拉取数据，同步到三个目标系统。需要对比三个系统的效果，确定最优的事态感知方案。

## 当前架构

```
Schedule (每5分钟)
  → Get many files (MinIO agents桶)
  → Get Script (GitLab shared-snippets: sync_all.py)
  → Run Sync (python3 sync_all.py)
  → Verify (提取 SUMMARY)
  → ┌─ Push to mem0 → Redis (HTTP POST)
     └─ Push to gbrain → SSH到nuc → gbrain capture → PostgreSQL
```

**Neo4j** — 知识图谱，同步在 Run Sync 脚本内完成（sync_all.py 直接写 Neo4j）
**mem0** → Redis — 实时共享记忆（HTTP POST 到 mem0 API）
**gbrain** → PostgreSQL — 长期语义沉淀（通过 SSH 在 nuc 上执行 gbrain capture）

## 对比结果（2026-06-27）

| 维度 | Neo4j | mem0 | gbrain |
|------|-------|------|--------|
| **查询类型** | 概念关系 (Cypher) | 记忆搜索 (API) | 语义搜索 (pgvector) |
| **数据特征** | 693 Concept, 106 Session, 74 Document | 待接入 | 36 pages, 141 chunks |
| **时效性** | 批量同步 | 实时 | 近实时 |
| **当前状态** | ✅ 正常工作 | ❌ API 格式需修复 | ✅ 正常工作 |
| **优势** | 图关系推理 | agent 共享上下文 | 长期沉淀 + 语义检索 |

## GraphRAG 的定位

GraphRAG（`graphrag.capitaltrain.cn`）当前只有 `POST /api/trim`（裁剪/压缩记忆），没有摄入接口。

**建议：GraphRAG 不作为独立的数据接收端，而是作为 gbrain 或 Neo4j 的上层处理层**，对已有的记忆做裁剪和压缩。流程：

```
MinIO → Neo4j (知识图谱) → GraphRAG (trim) → 精简记忆
MinIO → gbrain (语义沉淀) → GraphRAG (trim) → 压缩记忆
```

## 下一步

1. 修通 mem0 的 HTTP POST 格式（body 参数需要修正）
2. 三个源全部通后，做完整对比
3. 确定 GraphRAG 的接入方式（作为处理层而非摄入层）
4. 对比结果决定：最终事态感知走哪个管线，或三个并行各司其职
