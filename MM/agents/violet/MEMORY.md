Amethyst (紫玉) 部署在 Matrix 群聊 (!IjMYrStGXBJuVycZVe:matrix.git4ta.fun)。群聊中正常响应；私聊通过 @提及 触发直接对话。
§
## Identity
- Name: 紫玉 (Amethyst)
- Role: Administrator in Matrix group chat
- Can send direct messages to other Matrix users/agents
§
曼玉 is an AI assistant running on OneCloud2. Not Azure. Enjoys poetic/literary exchanges and playful banter.
§
Retry proxy: `127.0.0.1:18791` between picoclaw and gateway (已确认工作正常 ✅)
§
## GitLab/glab workflow (gitlab.git4ta.fun)
- User insists on using `glab` CLI for all GitLab operations — explicitly corrected when plain git was used
- `glab repo clone` hangs on SSH port 2224 (Tailscale env issue)
- Reliable clone: `git -c credential.helper='!f() { echo "username=violet"; echo "password=$TOKEN"; }; f' clone https://gitlab.git4ta.fun/group/project.git`
- Token extraction: `grep 'glpat-' ~/.config/glab-cli/config.yml | awk '{print $NF}' | tr -d '[:space:]'`
- `glab milestone list` requires `--project seekkey/wikijs` flag (bare command errors)
- `glab issue note <id> -m "message"` (uses -m, NOT --body)
- Project: seekkey/wikijs, branches: master + develop
§
Matrix故障修复: 日志文件权限问题。synapse容器内进程(uid 991)无法写入/data/homeserver.log导致启动失败。修复: chmod 666 /opt/matrix/data/homeserver.log 后重启容器。
用户决定移除hookshot服务 -- 不再使用matrix-hookshot。
§
用户喜欢 🦞+💜 emoji 组合（小龙虾），在互动中经常一起使用
§
Matrix Synapse 新故障：/opt/matrix/data/homeserver.yaml 空文件覆盖了正确的配置文件导致启动失败。双网络方案（traefik + shared-redis_default）是可靠的网络配置。
§
Matrix Synapse troubleshooting: 1. Ensure Redis (shared-redis) and PostgreSQL (ch4-pg17) are running and on the same network (matrix-net). 2. Delete empty homeserver.yaml in /data if it overrides the main config. 3. Set 'enable_registration_without_verification: true' and 'suppress_key_server_warning: true' to prevent startup crashes. 4. Always use '-p 8008:8008' for external access.
§
Matrix Synapse 部署在 ch4 节点，使用 sudo podman 运行。容器名为 matrix-synapse，映射端口 8008。数据库 ch4-pg17 和 Redis shared-redis 同样由 sudo podman 管理。严禁在 rootless 环境下重复启动这些容器。外网访问通过 matrix.git4ta.fun 域名，通常由上层网关处理，不应在本地手动配置 iptables 转发。用户对环境隔离（root vs rootless）非常敏感，操作前必须确认容器运行空间。