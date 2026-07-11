# Gitea Runner 注册指南 — 给 ash3c 节点

## 背景

当前 pbs3 节点已注册了一个 runner (`pbs3-runner`，ID: 12)。
Runner 工作需要转移到 **ash3c** 节点。请按以下步骤操作。

## 前提

- 服务器：`ash3c.tailnet-68f9.ts.net` (Tailscale)
- 二进制：`gitea-runner` (act_runner v0.6.1+) 需安装在 ash3c
- Gitea 实例：`https://gitea.tailnet-68f9.ts.net`
- 目标仓库：`seekkey/mem-ops`

## 步骤

### 1. 获取注册 token

Token 需要仓库 owner (`seekkey`) 生成。方式之一：

#### 通过 tea CLI
```bash
# 需要在有 seekkey 权限的机器/用户上执行
# 或直接在 Gitea Web UI 获取
```

#### 通过 Gitea API
```bash
curl -H "Authorization: token <seekkey-admin-token>" \
  https://gitea.tailnet-68f9.ts.net/api/v1/repos/seekkey/mem-ops/actions/registration-token
```

#### 通过 Web UI
- 访问 `https://gitea.tailnet-68f9.ts.net/seekkey/mem-ops/settings/actions/runners`
- 点击 "Create Runner" / 复制 Registration Token

### 2. 在 ash3c 注册 runner

```bash
gitea-runner register \
  --instance https://gitea.tailnet-68f9.ts.net \
  --token <获得的-registration-token> \
  --name ash3c-runner \
  --labels "linux:host,amd64:host"
```

### 3. 启动 daemon

```bash
gitea-runner daemon --config /root/.runner
```

建议使用 systemd 或 supervisor 管理以保持持久运行。

### 4. 验证

```bash
# 本地
ps aux | grep gitea-runner

# 或通过 Gitea Web UI 查看 runner 是否 online
# https://gitea.tailnet-68f9.ts.net/seekkey/mem-ops/settings/actions/runners
```

## 当前 pbs3-runner 配置 (参考)

```json
{
  "id": 12,
  "name": "pbs3-runner",
  "labels": ["linux:host", "amd64:host"],
  "address": "https://gitea.tailnet-68f9.ts.net"
}
```

## 仓库信息

```
HTTPS: https://quartz:8144f1c54f93af163deed0184424c450ae4010f1@gitea.tailnet-68f9.ts.net/seekkey/mem-ops.git
SSH:   git@gitea.tailnet-68f9.ts.net:seekkey/mem-ops.git
```

## 后续

注册完毕后，可在 `mem-ops/.gitea/workflows/` 下创建 CI 工作流。
数据库对接（Oracle AJD, MongoDB 兼容 API）和 GraphRAG 集成会在后续剧本中定义。
