# MemOps — Memory Bank: MoE² Cognitive Infrastructure

**记忆银行：面向 Web4 智能体身份的去中心化认知基础设施**

MoE²（Mixed Expert of Mixed Experts）— 在异构 MoE 各自为政的时代，构建跨厂商、跨架构、跨生态的大模型联邦认知总线。

## 核心概念

- **MoE² Overlay** — 封神榜全局调度层，在各大模型厂商的 MoE 点将台之上建立统一路由
- **Zodiac Cabinets** — 十二宫联邦架构，1 配 12 的管理幅度模型
- **Nicaea Consensus** — 尼西亚共识机制，防止大模型生态技术生殖隔离
- **Memory Bank** — 长效统一上下文记忆银行，Agent afterlife 全局台账

## 论文

参见 [`paper/`](./paper/) 目录：

- [`paper.md`](./paper/paper.md) — 中文全文
- [`paper.en.md`](./paper/paper.en.md) — English version
- [`paper.html`](./paper/paper.html) — 可读排版 HTML 版

## 架构

```
MinIO (原始记忆存储)
  → Neo4j (谓词逻辑 / 知识图谱)
  → GraphRAG (矛盾检测 / 交叉验证)
  → mem0 + RedisStack (向量检索)
  → Chain (存在性证明 / 链上确权)
```

## 快速开始

```bash
pip install -e .
export MINIO_KEY=your_key
export MINIO_SECRET=your_secret
python analyze_memory.py
```

## License

Memory Bank © 2026 Seekkey （觅钥科技）

激进开源 — 详细许可证待定。
