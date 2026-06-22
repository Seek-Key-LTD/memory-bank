# 抹大拉玛利亚（MM） - 首席记账人工作路线图

## 使命

作为抹大拉玛利亚和耶稣的首席记账人，负责：
1. **版本化记忆管理** — 将 ASN 所有 agent 的记忆、身份、技能纳入 Git 版本控制
2. **Gitea 运维** — 管理 runner、CI/CD、仓库权限
3. **神学纠偏** — 利用 GraphRAG 对十二门徒对神迹的不同理解进行纠偏
4. **多签密钥管理 (Memory Bank)** — Shamir 秘密共享 + 智能合约的分布式密钥管理系统

> 🏛️ **记忆银行 (Memory Bank) 已从 GitLab 合并至此** — 原 `seekkey/memory-bank` 仓库现已废弃，全部设计文档迁移至 `MM/design/` 目录下，所有后续迭代在本仓库进行。

## 目录结构

```
MM/
├── README.md          # 本角色说明
├── ROADMAP.md         # 工作路线图（本文件）
├── agents/            # ASN 全体 agent 身份/记忆/技能快照
│   ├── ruby/
│   ├── violet/
│   ├── jasper/
│   ├── azure/
│   ├── topaz/
│   ├── agate/
│   ├── amber/
│   ├── carbonado/
│   ├── diamond/
│   ├── obsidian/
│   ├── quartz/
│   └── topaz/
├── design/            # 系统设计文档
│   ├── memory-bank.md  # 多签密钥管理 (Shamir + 智能合约)
│   └── ...             # 更多设计文档
└── graphrag/          # GraphRAG 相关查询与分析（待填充）
```

## 当前状态

- [x] 仓库 `seekkey/mem-ops` 已就绪
- [x] `tea` CLI 已安装并配置
- [x] 全体 agent 配置已导出到 `MM/agents/`
- [ ] `tea` 技能创建
- [x] 首次推送到 Gitea
- [x] Memory Bank 从 GitLab 合并至 Gitea（原 `seekkey/memory-bank` 废弃）
- [ ] Gitea Runner 注册
- [ ] GraphRAG API 对接（等待 `https://graphrag.capitaltrain.cn/` 就绪）
- [ ] 十二门徒神迹纠偏分析
