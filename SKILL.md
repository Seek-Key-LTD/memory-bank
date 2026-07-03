---
name: mem-ops
description: "MemOps 事态感知总线 — Neo4j + mem0 + GraphRAG 统一查询入口。当用户表达中明显缺少上下文时，优先使用本技能查询组织过程资产。"
version: 3.0.0
---

# MemOps 事态感知总线

## 架构

```
用户缺少上下文
      ↓
  查询总线（本技能）
      ├→ 1. mem0（向量检索 / 最快路径）
      │     POST 100.116.169.46:8801/v3/memories/search/
      │
      ├→ 2. Neo4j（Cypher 谓词逻辑 / 估价 / 关系推理）
      │     POST 100.116.169.46:7474/db/neo4j/tx/commit
      │     Basic auth: neo4j / ccie15544
      │
      ├→ 3. GraphRAG（知识精炼 / 交叉校验 / 问答）
      │     POST 100.116.169.46:8800/api/trim
      │
      └→ 4. gbrain PG（全量对话归档 / 向量搜索）
            CLI: ~/.bun/bin/bun ~/.bun/bin/gbrain (nuc only)
            PG: postgresql://gbrain@100.93.5.81:5432/gbrain
```

## 查询策略

### 快速语义搜索（优先）
```bash
curl -s -X POST http://100.116.169.46:8801/v3/memories/search/ \
  -H "Content-Type: application/json" \
  -d '{"query":"<关键词>", "user_id":"ben", "agent_id":"<可选:限定agent>"}'
```
示例：查 "n8n 管线"、"Neo4j 修复"、"Agent 记忆"

### 图谱关系查询
Neo4j 存有 106+ Session、20 Agent、Day 时间线、Document（完整 MEMORY.md）

常用查询：
```bash
# Session 列表（按时间）
curl -s -u neo4j:ccie15544 -X POST http://100.116.169.46:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"MATCH (s:Session) RETURN s.title, s.directory ORDER BY s.title"}]}'

# 按日期查
curl -s -u neo4j:ccie15544 -X POST http://100.116.169.46:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"MATCH (d:Day {date:\"2026-06-28\"})-[:HAS_SESSION]->(s) RETURN s"}]}'

# 查 Agent 及其记忆
curl -s -u neo4j:ccie15544 -X POST http://100.116.169.46:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"MATCH (a:Agent {name:\"amber\"})-[:HAS_MEMORY]->(m:Memory) RETURN m"}]}'

# 文档内容（完整 MEMORY.md）
curl -s -u neo4j:ccie15544 -X POST http://100.116.169.46:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"MATCH (d:Document {agent:\"amber\"}) RETURN d.title, d.content"}]}'
```

### 知识精炼
GraphRAG 的无状态精炼厂，用于去重、矛盾检测、摘要：
```bash
curl -s -X POST http://100.116.169.46:8800/api/trim \
  -H "Content-Type: application/json" \
  -d '{"memories":[{"agent":"amber","content":"<要处理的文本>","timestamp":"<ISO时间>"}]}'
```

### 原始对话查询
原始 dialog 在 MinIO（通过 LXC109 中转）：
```bash
ssh -o StrictHostKeyChecking=no root@100.66.3.80 \
  "lxc-attach -n 109 -- mc cat m2/agents/aliyun/dialog/<日期>.jsonl"
```

## 节点清单（14+）

| 节点 | Agent | 平台 | MinIO 同步 | 说明 |
|------|-------|------|-----------|------|
| nuc | ruby / hermes | QwenPaw | ✅ crontab | 管理者/跳板机 |
| ash3c | obsidian | QwenPaw | — | Oracle Cloud arm64 |
| ch4 | violet | QwenPaw | — | Oracle Cloud arm64 |
| xgp | agate | QwenPaw | — | PVE 宿主机 |
| pve2 | carbonado | QwenPaw | ✅ crontab | PVE 宿主机 |
| pve | diamond | QwenPaw | ✅ crontab | PVE 宿主机 |
| pbs3 | quartz | QwenPaw | ✅ crontab | PBS 备份节点 |
| mini | emerald | QwenPaw | ✅ crontab | Mac Mini |
| mbp | amber | QwenPaw | ✅ crontab | MacBook Pro（本机） |
| de | jasper | PicoClaw | — | 德国 arm64 |
| onecloud1 | luna | PicoClaw | — | Orange Pi armv7 |
| onecloud2 | azure | PicoClaw | — | Orange Pi armv7 |
| raccoon | topaz | QwenPaw | — | VM / 浏览器中心 |
| leopard | — | VM | — | 监督者 |

## 需要监控的指标

| 指标 | 工具 | 说明 |
|------|------|------|
| 各节点 crontab 是否运行 | Loki | 每 5 分钟 sync-memory.sh + opencode-pipeline.py 的日志 |
| MinIO agents bucket 同步 | MinIO | 文件是否按预期写入，版本链是否完整 |
| Neo4j 数据新鲜度 | Neo4j | Day / Session 节点的 synced_at 是否在最近 5 分钟内 |
| mem0 已有记忆数 | mem0 API | `GET /v3/memories/` 确认记忆数量增长 |
| n8n pipeline 执行 | n8n API / Loki | 每 5 分钟执行是否成功，错误率 |
| 版本管理 | MinIO | agents bucket versioning=enabled |

## 仓库

- **工作流定义**: `seekkey/n8n-ops`（Gitea）
- **Ansible 部署**: `seekkey/ai-ops` → `ansible/playbooks/deploy-agent-data-collect.yml`
- **事态感知总线**: `seekkey/mem-ops`（Gitea）/ `seekkey/mem-ops@3.0.0`（Skill Hub）
- **文档**: `seekkey/ai-ops/docs/knowledge-architecture.md`

## 标签

- 当用户表达中明显缺少上下文时 → 先查 mem0，再查 Neo4j
- 需要历史会话信息 → 查 Neo4j Session/OpenCodeSession
- 需要 Agent 身份/记忆 → 查 Neo4j Document（完整 MEMORY.md）
- 需要跨 Agent 一致性校验 → GraphRAG /api/trim
- 需要原始对话内容 → MinIO dialog .jsonl

## 维护

- Neo4j: 100.116.169.46:7474 (nuc), neo4j:ccie15544
- mem0: 100.116.169.46:8801 (nuc), POST /v3/memories/add/ + /search/
- GraphRAG: 100.116.169.46:8800 (nuc), POST /api/trim
- gbrain: 100.116.169.46:48899 (health only), PG at 100.93.5.81:5432
- 全部注册在 Consul（本机 localhost:8500 可查）
