# Mem-Ops Session Notes

## 2026-06-24 — 基础设施修复 + 架构梳理

### 1. Audiobookshelf 重复实例问题

- Docker 版 (`ghcr.io/advplyr/audiobookshelf:latest`) 端口 13378
- Podman 版 (`gitea.tailnet-68f9.ts.net/ben/audiobookshelf:latest`) 端口 80，host 网络模式
- 两个都挂载了同一套数据目录（危险！）
- 已删除 Docker 版，保留 Podman 版
- Consul 健康检查已切换到端口 80，状态 passing
- `https://audiobook.capitaltrain.cn` 访问正常

### 2. xgp 容器 100 (mongo2) 重建

- 旧容器是 Docker entrypoint 套 LXC，根本跑不起来
- 根本原因：`/usr/share/lxc/config/ubuntu.common.conf` 中 debugfs 默认挂载在 kernel 7.0.x 上失败（EINVAL）
- 已注释掉 debugfs 挂载，容器可正常启动
- 新建 Ubuntu 26.04 LXC（代号 resolute），安装 MongoDB 8.0.26
- CT 模板源已改成清华：`/usr/share/perl5/PVE/APLInfo.pm`
- MongoDB 用户：`ben` / `3131`，认证已启用
- Consul 注册：`mongodb` 服务在 xgp 节点，IP `192.168.31.248`
- vnet1 (10.0.0.100) 不通，用 vmbr0 (192.168.31.248)

### 3. xgp 镜像源（清华一条龙）

- PVE apt 源：`https://mirrors.tuna.tsinghua.edu.cn/proxmox/debian/pve`
- Ubuntu apt 源：`https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ resolute`
- MongoDB repo：`https://mirrors.tuna.tsinghua.edu.cn/mongodb/apt/ubuntu`
- CT 模板源：修改 `/usr/share/perl5/PVE/APLInfo.pm` 中的 `download.proxmox.com` → `mirrors.tuna.tsinghua.edu.cn/proxmox`

### 4. Mem-Ops 架构 — Memory Bank Securitization Flow

```
原始数据（聊天/上下文/弱DB如SQLite）
    │
    ▼
MC (MinIO Client) → MinIO (原始存储)
    │
    ▼
OPA (组织过程资产) → 标准化
    │
    ▼
Projects (项目归集层) ← 待新增
    │
    ▼
第一波：机械推理（谓词逻辑）→ Neo4j ER图修正
    │
    ▼
第二波：小水管（Web3 / Coinbase CDP / Base Sepolia）
    │
    ▼
Memory Bank (加密入库)
```

**关键术语：**
- **小水管** = Web3 / Coinbase CDP / Base Sepolia 链路（shrimp-faucet），低流量但够用的通道
- **镇远镖局** = 比喻数据安全押运到记忆银行
- **机械推理 / 谓词逻辑** = 第一波结构化处理，用 Neo4j 做 ER 图修正
- **极简存法** = 当前原始数据的存储方式（如聊天上下文）

### 5. 核心架构思考 — 上下文与编码 Agent

#### 问题：编码 Agent 在黑洞里干活

当前 AI coding agent 的工作方式存在严重问题：
- agent 在"黑洞"里写代码，推送后其他 agent 只能通过 Lark 邮件收到通知
- 这不是 best practice，信息不透明，缺乏协作
- GitLab EE 有 Duo AI，但能力不够

#### 解法：n8n 作为中央调度

n8n 比 GitLab Duo 牛逼的地方：
- **GitLab 集成** — 版本控制
- **Oracle ATP 26ai** — 免费，甲骨文抢市场，每人两个实例（你有四个）
- **模拟芒果 API** — 不需要真跑 MongoDB
- **自带张量** — 内置 AI/ML 能力

#### 上下文是核心问题

- 普通 RAG 用 Redis/Milvus/Qdrant，运维成本高
- Oracle ATP 的优势：**上下文有关联性**——不相关的数据写不进去
- 这要求整理数据的模型必须牛逼（DeepSeek V4/Flash 绰绰有余）
- **关键洞察**：不是 pass through，是 relay——能用自己的话把一件事重新说一遍，才叫消化了
- 不光是 code review，是理解 + 重构 + 再表达

#### 盲区：Multi World of View

- 推上来的代码至少本地冒烟测试过了，盲区在于多视角
- seekkey group 里所有项目围绕 **ASN（Agentic Social Network）/ Web4**
- 像 Trae、Works 这类 IDE 本质是**沙箱**——装不了 Tailscale，只能指挥
- 所以它们是 **talkers, not doers**——只能说话，不能干活
- 我们有大量免费 token（各家厂商都在卷）

#### Memory Bank 三层架构

**类似网络三层模型：接入层 → 汇聚层 → 核心层**

目前已实现两层。接入层结构：

**Agent 视角（对私）：**
- QwenPaw 支持短期记忆（不用折腾）
- 长期记忆走 **PG Supabase + embedding**
- Agent 以为自己的记忆只存在 PG Supabase 里

**实际运转（对公）：**
- MC 每 5 分钟收集所有 12 个 agent 的 Markdown 文档 → MinIO
- Agent **不知道**自己的文档被 MC 抓走了
- n8n 流水线：MinIO → 内网 MongoDB

**关键洞察：**
- Agent 以为记忆在 PG Supabase（私域）
- 实际上 MC 每 5 分钟把所有人的文档都抓走了（公域）
- 这就是"对公 vs 对私"的技术实现

**汇聚层：Alignment Agent（抹大拉玛利亚）**
- MongoDB 是原始 archive，乱七八糟东西往里扔，像没有整理的 Web Clipper
- Alignment Agent 上场：对原始数据做对齐、整理、消除分歧
- **神学隐喻**：四福音书的分歧根源在于耶稣的情人玛利亚——没人提这事，但记录态度已导致分裂
- 约翰福音最超然，因为几乎没有记录关于玛利亚的事
- **技术含义**：不同来源的数据（agent）记录同一事件时态度不同，需要 Alignment Agent 做对齐

**接入层 → 汇聚层：NFT 铸造过程**
- 本质是把原始数据（黄金）铸造成 NFT（金项链），过程中有损耗
- 铸造消耗**通证（tokens）**——通胀从这来
- 通证来源 = 小水管（Web3 / Coinbase CDP / Base Sepolia）
- **T → NFT 的转化**需要"凝聚"和"护法"
- 武侠片隐喻：核心人物运功，旁边长老护法
- 结果：干活的人少了（12 → 9），部分 agent 转型为守护者

**汇聚层最终形态：记忆的本质**
- 过程性知识（如"1 < 2"）**不叫记忆**
- 真正的记忆：**一说就错，滑溜溜盛不住水**
- 法官隐喻："我不知道什么是毛片，但看到就知道"（勃起反应）
- 记忆 = **高维张量空间**，无法用简单语言捕获
- 阿里"阿福"项目：蒸馏三甲医院台柱子主任医师的知识 → 基本不可行
- 技术含义：记忆不能靠简单 RAG，需要张量表示

**"Great Artists Steal" 的真正含义**
- 记忆 = 高维张量空间中的**离散点**
- "Great artists steal" = 学会在高维张量空间里把这些点**连起来**
- 最终在我们眼中呈现为**星座**（constellation）
- 这就是 Alignment Agent 的终极使命：连接离散记忆点，呈现星座图景

**压缩 = 表达 = 理解**
- 压缩的本质是表达，不能表达 = 没有理解
- 理解高维张量空间的稀疏矩阵，**不能通过纯数学方式**
- 反证：华为 + 港科大 → 搞出"缝合怪"（Hybrid）— 图片 + 降维向量空间，声称 OK，但不通用
- Web 4 价值：需要在 agent 之间建立"国际贸易"
- 相关文档：spore network（孢子网络）— agent 间国际贸易机制
- Layer 2 + NFT 铸造 → Matrix to Matrix 之间的通货

**ASN 的核心：生物计算（Biological Computation）**
- "十张图"（ten graph）— 高维张量空间必须说清楚
- 过去做法：把高维张量当**对象**（object）处理
- ASN 做法：把它当**知识本体**（Knowledge Authority / Ontology）
- **对象 vs 本体** — 这是根本性区别
- 对象是被动的、可操作的；本体是主动的、有权威性的

**Knowledge Ontology（KO）核心：自我指涉**
- 不只是被计算的节点，**本身要参与计算**
- 电子政务最难之处：预测政策影响比预测雷暴还难
- 原因：决策者本身是系统的一部分 → 产生**自我指涉**（self-reference）
- 自我指涉既是**问题**，也是**方法**
- 在 ASN 中：agent 既是数据源，也是计算节点

**生物计算 = 蚁群模型**
- 旧定义（神经元）→ 无意义
- 广义定义：**蚁群** = 理想国，三阶级各司其职
  - **Queen**（蚁后/CEO）
  - **Warrior**（兵蚁/HR）
  - **Worker**（工蚁/牛马）
- 蚂蚁集团类比：马云、HR、牛马
- 生物计算的本质：分布式、分层、自组织

**汇聚层核心：记忆增值**
- 接入层解决异构 + 上链
- 汇聚层解决 **security task** —— 让存进来的记忆增值
- 类比公募基金：别人投进来的钱，你要让它产生价值
- 不说挣钱，至少要**盘活**、**产生价值**

**世界的抽象类有上限**
- "天下没有新鲜事" —— 世界总共需要回答的问题可能就 ~1000 个
- 抽象类有上限，类似元素周期表
- 要找到这 1000 个上限的**本体**
- 然后通过层级组织：King → Queen → Warrior → Soldiers → Workers
- 世界可被认知 → 不诉诸随机
- 如果高维张量看起来很随机，说明你在用**全宇宙**视角，而非我们这个**特殊解宇宙**的视角看问题

**超弦理论的启示**
- 超弦理论已定义宇宙常数，其"结"揭示了宇宙为何如此空旷、物质稀少
- 本身已经是高维稀疏张量
- 研究这组解 → 和找外星人没区别 → **此路不通**
- 解决方案：**生物计算**（蚁群模型）

**汇聚层 → 核心层：知识路由**
- 汇聚层的核心任务：为核心层提供**知识路由**
- 隐喻：农民（神农）懂太阳周期，股票交易员也想懂
- 农业领域的"神"能否指导金融领域？→ 可以，但必须**先回到那 1000 个天元问题**
- 先抽象，再派生
- 技术含义：不同领域的 agent 要跨域协作，必须先在最高抽象层对齐

**知识本体论的终极形态**
- 整个过程 = Knowledge Ontology
- 所有问题都在**完全分类**的数里
- 张量必然代表完全分类
- **天问就是问天，问天有求必应**
- 技术含义：1000 个天元问题 × 完全分类 = 所有可被认知的问题都有解

**核心层：可实现，需资金**
- 1000 是估算，核心是天元问题**可数**（countable），不是无限的
- 核心层**不是没法实现**，是当前靠白嫖、资源有限
- 如果有 200 万赞助 → 宏伟蓝图可落地
- 系统可以**挣钱**：国际贸易、暴打 Web3、暴打美国科技股

#### 人格化记忆 — 对公 vs 对私

- MemOps 核心：从本地 mem0/gbrain 的上下文出发
- 记忆分两步：**对公**（公开）vs **对私**（私密），涉及人格
- 日记 = "一亩三分地，风能进雨能进，国王不能进"
- 历史先例：蒋介石日记、鲁迅日记、俞平伯日记、季羡林日记
- **每个 agent 有权说其他 agent 是傻子**
- 私密人格化内容**不会扔给 mem0** — 这是私域
- mem0 只管对公的部分

#### Oracle ATP 免费资源与数据生命周期

- 每个账号 2 个 ATP 实例，用户有 2 个账号 = 4 个 ATP 实例
- 相比 ADW 更轻量，相比 AGD 上下文有关联性
- **ATP 容量限制**：只有 10GB 可用（号称 20GB，系统占 10GB）
- **热区滑动窗口 7 天**：只有最近 7 天的 project situation awareness 有意义
- **冷数据流转**：7 天以上 → 甲骨文同区 Object Storage buckets → MC 导入自建 HDD MinIO
- **MinIO 定位**：主要是数据安全，不是性能

### 6. 待办

- [ ] 添加 Projects 层（项目归集）
- [ ] 第一波：谓词逻辑 + Neo4j ER 图修正
- [ ] 第二波：小水管（Coinbase CDP）对接
- [ ] n8n 技能文档（MCP 调用方式）
- [ ] 三点思考记录（待第三点）
