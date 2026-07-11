# GitLab 配置

## 服务器信息

- Host: ch4.tailnet-68f9.ts.net
- HTTP API: http://ch4.tailnet-68f9.ts.net:80
- SSH Git: ssh://git@ch4.tailnet-68f9.ts.net:2224

## 认证信息

- Token: glpat-a8dfezSoShmD5hMH72B32W86MQp1OmEH.01.0w08k7wep
- SSH Key: ~/.ssh/id_ed25519_gitea

## 历史 Token（已失效或备用）

# 旧 Token: glpat-5CYcJWOxC3tmD-gCczU3_286MQp1OmEH.01.0w09c3ygs

## 使用方式

### API 调用
curl -H PRIVATE-TOKEN:<token> http://ch4.tailnet-68f9.ts.net:80/api/v4/user

### Git 操作
GIT_SSH_COMMAND=ssh -p 2224 -i ~/.ssh/id_ed25519_gitea git clone ssh://git@ch4.tailnet-68f9.ts.net:2224/用户名/仓库.git

## 测试状态

- [x] HTTP API 连接测试通过
- [x] SSH 连接测试通过
- [x] Token 认证有效
