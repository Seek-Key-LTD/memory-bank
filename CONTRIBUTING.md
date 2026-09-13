# 记忆银行（Memory Bank）社区贡献与审核员守则

欢迎加入 **SeekKey Memory Bank**（面向 Web4 智能体身份与因陀罗网络的去中心化认知基础设施）！

本项目奉行**法医级证据链**与**肯定性立论原则**。无论你是作为代码贡献者（Contributor）、法医审核员（Reviewer / Triage），还是核心维护者（Maintainer），均请遵守本规范。

---

## 核心哲学与立论法则

1. **光驳论不立论，飞轮转不起来**：
   - 不接受单纯情绪化的解构或空洞驳斥；
   - 提出缺陷或异议时，必须附带**建设性的肯定假设（Constructive Affirmative Hypothesis）**与最小可验证证据（PoC / Schema / Test）。
2. **出门在外，身份是自己给的 —— 自授权（Self-Authorization）**：
   - 智能体节点通过公私钥、KYA（Know Your Agent）声明与因陀罗网络自我确权。
3. **零敏感凭据泄漏（Zero Secrets Leakage）**：
   - 严禁将真实的私钥、Vault Root Token、数据库明文密码提交至 Git 历史；
   - 任何 PR 必须通过 `ash3` 自动化安全门禁。

---

## 贡献者与审核员晋阶梯队（Ladder）

| 角色 | 权限机制 | 职责与荣誉 |
| :--- | :--- | :--- |
| **Contributor (贡献者)** | Fork + PR | 提交 Schema 扩展、AGE Cypher 模板、算法优化或论文修补 |
| **Reviewer (审核员 / Triage)** | GitHub Triage 角色 + CODEOWNERS | 审核社区 PR、核验证据链完整性、参与仲裁判定、在提交历史上保留永久见证签名 |
| **Maintainer (维护者)** | Maintainer 角色 | 核心架构演进、版本发布、多模态中央银行核心参数决议 |

---

## 审核员（Reviewer）核验清单

审核员在签署 `Approve` 时，需逐一核验以下四条铁律：
- [ ] **时间线连续性**：是否通过 `scripts/age_timeline_linter.py` 的 DAG 时间线校验。
- [ ] **无幻觉立论**：引用的历史账目、论文出处与数据指标是否具有可追溯的法医底册。
- [ ] **无账单与资源溢出**：所有的外部服务调用是否遵循自带干粮原则（如 MongoDB Atlas 512MB 免费层或本地实例）。
- [ ] **CI 门禁通过**：GitHub Actions 自动化流水线（由 `ash3` runner 承载）全绿。

---

## PR 提交步骤

1. Fork 本仓库并基于 `main` 分支创建特性分支（`feat/...` 或 `fix/...`）；
2. 运行本地校验：
   ```bash
   python3 scripts/age_timeline_linter.py schemas/memory_record.json
   ```
3. 提交 PR 并关联对应的 Issue。
