# GitLab 配置

## 服务器信息

- Host: ch4.tailnet-68f9.ts.net
- HTTP API: http://ch4.tailnet-68f9.ts.net:80
- SSH Git: ssh://git@ch4.tailnet-68f9.ts.net:2224

## 认证信息

- Token: glpat-U7L7MZkRz6VLmIxrT1VpO286MQp1OmgH.01.0w0ea17n9
- SSH Key: ~/.ssh/id_ed25519_gitea

## 使用方式

### API 调用
curl -H PRIVATE-TOKEN:<token> http://ch4.tailnet-68f9.ts.net:80/api/v4/user

### Git 操作
GIT_SSH_COMMAND="ssh -p 2224 -i ~/.ssh/id_ed25519_gitea" git clone ssh://git@ch4.tailnet-68f9.ts.net:2224/用户名/仓库.git
