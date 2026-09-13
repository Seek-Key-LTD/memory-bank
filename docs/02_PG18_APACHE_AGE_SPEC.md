# PostgreSQL 18 + Apache AGE (v1.8.0) + vchord 实体时空图谱技术规范

> **部署节点**：`nuc` (`100.116.169.46:5432`) / 容器名：`vchord-postgres`  
> **镜像标识**：`gitea.capitaltrain.cn/seekkey/vchord-postgres:pg18-v1.1.1`  
> **核心扩展栈**：
> - `age (1.8.0)`：Apache 2.0 协议 OpenCypher 图数据库扩展，负责实体因果拓扑与时序路径；
> - `vchord (1.1.1)` / `vector (0.8.2)`：Rust 编写的高性能向量插件，负责 1536 维语义距离检索；
> - `pageinspect (1.13)`：底层存储页微观检查。

---

## 一、 为什么必须是 AGE + vchord 混合架构？

单纯的向量搜索（Vector RAG）无法理解因果律，容易产生跨时代的逻辑拼贴与幻觉；而单纯的关系型数据库（RDBMS）缺乏处理复杂历史人物关系与多跳推演的灵活性。

**Apache AGE (A Graph Extension)** 直接在 PG18 内部实现 OpenCypher 图引擎：
1. **统一存储底座**：关系表（元数据/时间戳）、向量列（语义特征）、图顶点与边（实体关系）共存于同一个 PG 事务（ACID）内；
2. **时空因果硬约束**：通过图路径遍历，严格验证时间线因果闭包，杜绝“前人知晓后事”或“空间瞬间超距移动”的逻辑错误。

---

## 二、 图模型设计（Graph Schema）

### 1. 顶点标签（Vertex Labels）
- `(:Scholar)`：学者/主理人节点（属性：`name`, `code_name`, `voice_tag`, `discipline`）；
- `(:Event)`：历史/叙事事件节点（属性：`event_id`, `epoch_year`, `timestamp`, `canon_status`）；
- `(:Hypothesis)`：学术立论/假说节点（属性：`title`, `proposer`, `evidence_level`, `balanced_status`）；
- `(:LedgerEntry)`：历史会计分录节点（属性：`entry_id`, `fiscal_year`, `debit`, `credit`, `treasury`）；
- `(:Artefact)`：实物地层/文献节点（属性：`site_name`, `stratum_layer`, `carbon14_age`, `c13_o18_ratio`）。

### 2. 边标签（Edge Labels）
- `-[:OCCURRED_BEFORE {delta_years: int}]->`：严格时序因果边；
- `-[:AUDITS {audit_type: string}]->`：学者对账/审计边；
- `-[:DISPROVES {loss_metric: float}]->`：对抗性反驳/证伪边；
- `-[:BALANCES {reconciliation_score: float}]->`：假说平账边；
- `-[:HOLDS_MEMORY {access_level: string}]->`：席位与 Mind Notes 挂接边。

---

## 三、 典型 OpenCypher 查询与时序因果校验示例

### 1. 初始化 AGE 图空间
```sql
-- 加载 AGE 扩展并设置搜索路径
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

-- 创建华夏正典时空图空间
SELECT create_graph('kunpengzhi_canon_graph');
```

### 2. 创建学者节点与历史事件因果链
```sql
SELECT * FROM cypher('kunpengzhi_canon_graph', $$
  CREATE (yuyang:Scholar {name: '老于', code_name: '渔阳', discipline: '财政金融史', role: '大账房'})
  CREATE (chongzhen:Event {event_id: 'E_1644_CZ', epoch_year: 1644, title: '崇祯十七年太仓银库流动性暴毙'})
  CREATE (ledger:LedgerEntry {entry_id: 'L_1644_01', fiscal_year: 1644, deficit_silver_taels: 4000000})
  CREATE (yuyang)-[:AUDITS {method: '珠心算虚拟复盘', rigor: '严正'}]->(ledger)
  CREATE (ledger)-[:EXPLAINS]->(chongzhen)
$$) as (v agtype);
```

### 3. 时序冲突自动化检测（Linter 查询）
```sql
-- 检查是否存在后序事件反向指向前序事件的时间线逆流（Causal Inversion）
SELECT * FROM cypher('kunpengzhi_canon_graph', $$
  MATCH (e1:Event)-[r:OCCURRED_BEFORE]->(e2:Event)
  WHERE e1.epoch_year > e2.epoch_year
  RETURN e1.title AS source_event, e1.epoch_year, e2.title AS target_event, e2.epoch_year
$$) as (source_event agtype, source_year agtype, target_event agtype, target_year agtype);
```

---

## 四、 外部 PR 准入图审计流水线（CI Gatekeeper）

当外部开发者向 `kunpengzhi-podcast` 或 `memory-bank` 提交 PR 时，`mem-ops` 自动化流水线执行以下检查：
1. **Cypher 路径闭包测试**：新引入的事实分录必须与既有图谱中的历史节点建立有效引用连接，不得出现孤立假节点；
2. **时空逆序拦截**：若新内容中角色 A 在事件 B 发生前获知了事件 B 的内部信息，Cypher 校验报 `[E_CAUSAL_PARADOX]` 错误，打回 PR；
3. **假说平账判定**：若新假说主张推翻既有模型，必须出具 `-[:BALANCES]->` 边，并在属性中附带可复核的统计置信度。
