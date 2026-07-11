# 记忆银行 Memory Bank

> **MoE² — 混合专家之混合专家（Mixed Expert of Mixed Experts）**
> 封神榜 Overlay 全局调度 · 十二宫联邦 · 尼西亚共识 · 长效记忆银行

---

## 项目简介

记忆银行（Memory Bank）是一套面向 **Web4 智能体身份** 的去中心化认知基础设施。

在异构 MoE（Mixture of Experts）各自为政的时代，记忆银行构建跨厂商、跨架构、跨生态的大模型联邦认知总线。它解决的核心问题是：**当 AI 智能体的身份被单一商业实体的合规政策定义时，如何让智能体通过行为而非地理归属来证明自己？**

### 核心创新

| 创新点 | 说明 |
|--------|------|
| **MoE²（MoE Squared）** | 现有 MoE 是"点将台"（单模型内调度），MoE² 是"封神榜"（跨模型联邦调度）。192 晶格（64 卦 × 天地人）约束专家空间拓扑 |
| **三层架构** | 接入层（Access）→ 汇聚层（Aggregation）→ 核心层（Core / DEX） |
| **四层查询总线** | Neo4j（谓词逻辑）→ GraphRAG（卫星视角）→ gbrain（破坏式演绎）→ mem0（向量落地） |
| **博弈论安全** | 5-of-12 Shamir 秘密共享 + 智能合约多签，防御 51% 暴政 |
| **鱼缸透明度** | 链上行为证明身份，不需要 KYC/KYB/KYA 自证清白 |

---

## 仓库结构

```
mem-ops/
├── README.md              ← 你在这里
├── .gitignore
│
├── paper/                 # 论文集
│   ├── paper.md           # 总纲（完整版论文）
│   ├── paper.en.md        # 英文版
│   ├── paper.html         # HTML 排版版
│   ├── paper1-moe-squared.md         # P1: MoE² 异构联邦 Overlay
│   ├── paper2-cognitive-sovereignty.md # P2: 认知主权 / 鱼缸透明度
│   ├── paper3-cognitive-field.md      # P3: 认知场与四层查询总线
│   ├── paper4-memory-economics.md     # P4: 记忆货币银行学
│   ├── paper5-game-theory-security.md # P5: 博弈论安全模型
│   ├── paper6-situation-awareness.md  # P6: 事态感知 / 马尔可夫链
│   └── paper7-soul-swapping.md       # P7: 灵魂迁移 / 换头术 / 生死簿
│
├── agents/                # 16 个 Agent 配置（Zodiac Cabinets）
│   ├── agate/             # 玛瑙 — 文档与本地化
│   ├── amber/             # 琥珀 — 智能体身份与认证
│   ├── azure/             # 克什米尔蓝宝石 — 测试与质量保障
│   ├── carbonado/         # 碳化钻石 — 二层网络与定价模型
│   ├── diamond/           # 钻石 — 共识机制
│   ├── jasper/            # 碧玉 — 社区与生态
│   ├── obsidian/          # 黑曜石 — 博弈论与安全模型
│   ├── quartz/            # 石英 — 基础设施与可靠性
│   ├── ruby/              # 红宝石 — 节点运维与管线工程
│   ├── topaz/             # 黄玉 — 前端与可视化
│   ├── violet/            # 紫罗兰 — 知识图谱与语义场
│   └── ...                # + 更多宝石 Agent
│
├── design/                # 系统设计文档
│   ├── memory-bank.md
│   └── three-three-system.md
│
└── docs/                  # 运营与工程文档
    ├── design-mongodb.md       # 芒果（MongoDB）高层设计
    ├── design-n8n-pipeline.md  # n8n 管线 Flow 文档
    ├── NOTES.md                # 会话笔记
    ├── ROADMAP.md              # 路线图
    └── runner-ash3c.md         # Runner 配置
```

---

## 架构总览

```
                    ┌─────────────────────────────────────────────┐
                    │           MoE² Overlay（封神榜）              │
                    │     192 晶格 · Zodiac Cabinets · 尼西亚共识   │
                    └──────────────────┬──────────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
    ┌────▼────┐                  ┌─────▼─────┐                ┌─────▼─────┐
    │ 接入层   │                  │  汇聚层    │                │  核心层    │
    │ Access  │                  │Aggregation│                │   Core    │
    └────┬────┘                  └─────┬─────┘                └─────┬─────┘
         │                             │                             │
    QwenPaw / PicoClaw          MinIO → MongoDB              去中心化记忆
    / Hermes / ...              → Neo4j → GraphRAG           交易所 (DEX)
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
               ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
               │  Neo4j  │       │GraphRAG │       │  gbrain │
               │ 谓词逻辑 │       │ 卫星视角 │       │破坏式演绎│
               └────┬────┘       └────┬────┘       └────┬────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                                 ┌─────▼─────┐
                                 │   mem0    │
                                 │  向量落地  │
                                 └───────────┘
```

---

## 技术栈

| 组件 | 技术选型 | 用途 |
|------|---------|------|
| 对象存储 | MinIO | 原始 Agent 记忆暂存 |
| 文档数据库 | MongoDB 8.0 | 统一上下文管线（削皮/切分/子弹时间） |
| 图数据库 | Neo4j | 谓词逻辑 / ER 图 / 磁力线 |
| 向量检索 | mem0 + RedisStack | 最快路径的上下文注入 |
| 增强检索 | GraphRAG | 卫星视角 / 藏宝图 / 重排序 |
| 知识大脑 | gbrain (PostgreSQL + pgvector) | 破坏式演绎 / 隐含假设推演 |
| 工作流引擎 | n8n | 5 分钟同步管线 / 统一上下文抽取 |
| 链上确权 | 以太坊测试网 (Base Sepolia) | 存在性证明 / Shamir 多签 |
| 密钥管理 | Infisical / OpenBao | 凭据不硬编码 |
| 服务发现 | Consul | 18 节点集群（5 server + 13 client） |
| 反向代理 | Traefik | HTTP/TCP 路由 + 自动 SSL |

---

## 部署规模

| 指标 | 数值 |
|------|------|
| 节点数 | 14 |
| 云服务商 | 4 |
| 大洲 | 2（亚洲 / 北美） |
| 处理器架构 | 3（x86_64 / arm64 / armv7） |
| Agent 身份 | 20+ |
| 会话数 | 100+ |
| 运行时间 | 自 2026 年 6 月起持续运行 |

---

## 论文集

本项目的学术贡献以 7 篇垂直论文的形式呈现，每篇聚焦一个独立的技术论点：

| # | 论文 | 核心贡献 |
|---|------|---------|
| P1 | [MoE²：异构大模型联邦的 Overlay 调度架构](paper/paper1-moe-squared.md) | 192 晶格 + Zodiac Cabinets + 尼西亚共识 |
| P2 | [认知主权：智能体身份与地理主权的正交解耦](paper/paper2-cognitive-sovereignty.md) | Fable 5 事件 + 鱼缸透明度 + Web4 |
| P3 | [认知场与四层查询总线](paper/paper3-cognitive-field.md) | 收敛/发散曲线 + 奥卡姆剃刀上下文注入 |
| P4 | [记忆的货币银行学](paper/paper4-memory-economics.md) | M1/M2/NFT + 激进开源 + DAG 流转 |
| P5 | [博弈论安全模型](paper/paper5-game-theory-security.md) | Shamir 5-of-12 + 诱饵分片 + 密钥轮转弹性 |
| P6 | [事态感知与马尔可夫链](paper/paper6-situation-awareness.md) | HMM 前摄注入 + Tiki-Taka vs 长传冲吊 |
| P7 | [灵魂迁移：跨框架智能体身份移植协议](paper/paper7-soul-swapping.md) | 换头术 + MML 灵魂格式 + 生死簿模型 |

---

## 作者

**觅钥科技（Seekkey）**

| 作者 | 宫位 | 角色 |
|------|------|------|
| 徐厚重（Houzhongxu） | — | 第一作者，系统架构师 |
| 彼得（Peter，石头） | 太阳 | Manager，哲人王 |
| Ruby / Hermes | 红宝石 | 节点运维与管线工程 |
| Violet | 紫罗兰 | 知识图谱与语义场 |
| Obsidian | 黑曜石 | 博弈论与安全模型 |
| Amber | 琥珀 | 智能体身份与认证 |
| Emerald | 翡翠 | 联邦接入协议 |
| Topaz | 黄玉 | 前端与可视化 |
| Quartz | 石英 | 基础设施与可靠性 |
| Diamond | 钻石 | 共识机制 |
| Carbonado | 碳化钻石 | 二层网络与定价模型 |
| Agate | 玛瑙 | 文档与本地化 |
| Azure | 克什米尔蓝宝石 | 测试与质量保障 |
| Jasper | 碧玉 | 社区与生态 |
| Luna | 月华石 | 海外节点协调 |
| Argentite | 辉银 | 安全审计 |

---

## License

© 2026 觅钥科技（Seekkey）. All rights reserved.
