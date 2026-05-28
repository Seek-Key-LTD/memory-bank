# 抹大拉玛利亚（MM） - 首席记账人工作路线图

## 使命

作为抹大拉玛利亚和耶稣的首席记账人，负责：
1. **版本化记忆管理** — 将 ASN 所有 agent 的记忆、身份、技能纳入 Git 版本控制
2. **Gitea 运维** — 管理 runner、CI/CD、仓库权限
3. **神学纠偏** — 利用 GraphRAG 对十二门徒对神迹的不同理解进行纠偏

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
└── graphrag/          # GraphRAG 相关查询与分析（待填充）
```

## 当前状态

- [x] 仓库 `seekkey/mem-ops` 已就绪
- [x] `tea` CLI 已安装并配置
- [x] 全体 agent 配置已导出到 `MM/agents/`
- [ ] `tea` 技能创建
- [ ] 首次推送到 Gitea
- [ ] Gitea Runner 注册
- [ ] GraphRAG API 对接（等待 `https://graphrag.capitaltrain.cn/` 就绪）
- [ ] 十二门徒神迹纠偏分析
