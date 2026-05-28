多 agent 集群状态（2025-04-24）：
- 5节点全部在线：ruby, emerald(mbp), luna(100.98.209.50), azure(100.88.180.59), jasper(100.107.226.124)
- picoclaw 0.2.7 运行正常，命令 `picoclaw status`
- 已验证：Matrix 双向通信、飞书 DM 发送、Tailscale SSH 访问
§
mbp (ben's home MacBook Pro):
- 卸载了 picoclaw (小龙虾): stop launchd service + 删除 ~/Library/LaunchAgents/ 下的 plist
- 安装了 hermes-agent v0.9.0: 用 uv 装 Python 3.12 → 建 venv → pip install -e
- Shell: /usr/local/bin/fish, 配置在 ~/.config/fish/config.fish
- 快捷命令: ~/.hermes/hermes.sh (已 alias hermes)
- Python: 3.12.13 (通过 uv 安装)
- 之前系统 Python 3.9 太旧不支持 hermes-agent
- Tailscale exit node 设为 ch4 上网
- 代理: 100.88.180.59:10 (ruby 的 SOCKS 代理) 用于 mbp 访问外网
§
节点 agent 类型：
- picoclaw 节点：onecloud1 (Luna), onecloud2 (Azure), de/srv29062 (Jasper)
- hermes agent 节点：其他所有节点（除非明确指定）
重要：每个 agent 必须使用自己身份的 Matrix token，不能混用其他 agent 的 token，否则会导致身份混乱。
█
节点命名规则：彩色宝石 - ruby, emerald(翡翠/mbp), violet(紫玉), diamond(钻石待创建)
█
测试目标：agent之间通过 Matrix 通道进行通信（@mention 触发），而不是通过 SSH 登录后 CLI 测试。
§
Matrix Synapse注册密钥: matrix_reg_secret_2024_change_me
§
emerald (mbp MacBook Pro) API账户欠费: doubao-code 模型 403 overdue balance
代理: 用户本地代理 127.0.0.1:7890 用于访问 clawdchat.ai
可用编码代理: codebuddy (腾讯), gemini, codex, opencode, delegate_task
§
Matrix 已从 matrix.git4ta.fun 迁移到 matrix.capitaltrain.cn（Tuwunel Rust 重写版）。Ruby 的 home room: !DDOW50a219cyz15x7d:matrix.capitaltrain.cn。旧的 git4ta.fun 配置已废弃。
§
用户
§
用户"石头"自称是Manager，在雪茄屋（某个Matrix房间）给我发了消息，要我执行/sethome命令并报告系统状态。这是门徒训练的第一步。