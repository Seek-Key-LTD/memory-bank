---
name: gitlab
description: GitLab operations — clone repos, manage projects, issues, MRs, CI/CD, and API calls on the private GitLab instance (gitlab.git4ta.fun / ch4.tailnet-68f9.ts.net).
---

# GitLab Operations Guide

## Server Info

| Item | Value |
|------|-------|
| Host | gitlab.git4ta.fun |
| HTTP API | https://gitlab.git4ta.fun |
| SSH Git | ssh://git@gitlab.git4ta.fun:2224 |
| Web UI | https://gitlab.git4ta.fun |

## Authentication

### Method 1: OAuth2 Token (HTTPS clone)
Token is stored in `~/.config/glab-cli/config.yml` under `hosts.gitlab.git4ta.fun.token`.
```bash
TOKEN=$(grep 'token:' ~/.config/glab-cli/config.yml | awk '{print $2}')
```

### Method 2: Private Token (API calls)
Token is in `~/.picoclaw/workspace/GITLAB.md` under `Token:`.
```bash
TOKEN=$(grep 'Token:' ~/.picoclaw/workspace/GITLAB.md | sed 's/.*Token: *//' | tr -d '\r\n')
```

### Method 3: SSH
SSH key: `~/.ssh/id_ed25519_gitea`
Port: 2224

---

## 1. Clone a Repository

### HTTPS (recommended)
```bash
TOKEN=$(grep 'token:' ~/.config/glab-cli/config.yml | awk '{print $2}')
git clone https://oauth2:${TOKEN}@gitlab.git4ta.fun/用户名/仓库名.git
```

### SSH
```bash
GIT_SSH_COMMAND="ssh -p 2224 -i ~/.ssh/id_ed25519_gitea" \
  git clone ssh://git@ch4.tailnet-68f9.ts.net:2224/用户名/仓库名.git
```

### Using glab CLI
```bash
glab repo clone 用户名/仓库名
```

**Pitfalls:**
- `glab repo clone` may timeout — if it does, fall back to raw `git clone` with oauth2 token
- SSH (`git@`) may hang/timeout — HTTPS with token is more reliable
- The token starts with `glpat-` — quote it properly in shell
- Always use `GIT_TERMINAL_PROMPT=0` to prevent interactive password prompts

---

## 2. List Projects

### Using glab
```bash
glab project list
```

### Using API
```bash
TOKEN=$(grep 'Token:' ~/.picoclaw/workspace/GITLAB.md | sed 's/.*Token: *//' | tr -d '\r\n')
curl -s -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.git4ta.fun/api/v4/projects?per_page=20" | python3 -m json.tool
```

### Search projects
```bash
curl -s -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.git4ta.fun/api/v4/projects?search=关键词" | python3 -m json.tool
```

---

## 3. Issues

### List issues
```bash
glab issue list
# or
curl -s -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.git4ta.fun/api/v4/projects/PROJECT_ID/issues" | python3 -m json.tool
```

### Create issue
```bash
glab issue create --title "标题" --description "描述"
# or
curl -s -X POST -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.git4ta.fun/api/v4/projects/PROJECT_ID/issues" \
  -d "title=标题" -d "description=描述"
```

---

## 4. Merge Requests (MRs)

### List MRs
```bash
glab mr list
```

### Create MR
```bash
glab mr create --source-branch 分支名 --target-branch main --title "标题" --description "描述"
```

### View MR
```bash
glab mr view MR编号
```

---

## 5. CI/CD

### List pipeline
```bash
glab pipeline list
```

### View pipeline status
```bash
glab pipeline view JOB_ID
```

---

## 6. Common API Endpoints

| Action | Endpoint | Method |
|--------|----------|--------|
| Get current user | `/api/v4/user` | GET |
| List projects | `/api/v4/projects` | GET |
| Get project | `/api/v4/projects/PROJECT_ID` | GET |
| Create project | `/api/v4/projects` | POST |
| List issues | `/api/v4/projects/ID/issues` | GET |
| Create issue | `/api/v4/projects/ID/issues` | POST |
| List MRs | `/api/v4/projects/ID/merge_requests` | GET |
| Create MR | `/api/v4/projects/ID/merge_requests` | POST |
| List pipelines | `/api/v4/projects/ID/pipelines` | GET |
| Get repo files | `/api/v4/projects/ID/repository/tree` | GET |
| Get file content | `/api/v4/projects/ID/repository/files/FILE_PATH/raw?ref=main` | GET |

### API call template
```bash
TOKEN=$(grep 'Token:' ~/.picoclaw/workspace/GITLAB.md | sed 's/.*Token: *//' | tr -d '\r\n')
curl -s -H "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.git4ta.fun/api/v4/ENDPOINT"
```

---

## 7. Helper Scripts

Located at: `~/.picoclaw/workspace/skills/gitlab/scripts/`

### gitlab_api.sh
```bash
# List projects
bash ~/.picoclaw/workspace/skills/gitlab/scripts/gitlab_api.sh list_projects

# Create project
bash ~/.picoclaw/workspace/skills/gitlab/scripts/gitlab_api.sh create_project "项目名" "描述"

# Create issue
bash ~/.picoclaw/workspace/skills/gitlab/scripts/gitlab_api.sh create_issue PROJECT_ID "标题" "描述"
```

### gitlab_api.py
```bash
python3 ~/.picoclaw/workspace/skills/gitlab/scripts/gitlab_api.py list_projects
python3 ~/.picoclaw/workspace/skills/gitlab/scripts/gitlab_api.py create_project "项目名" "描述"
python3 ~/.picoclaw/workspace/skills/gitlab/scripts/gitlab_api.py create_issue PROJECT_ID "标题" "描述"
```

---

## 8. Quick Reference

```bash
# 1. Get token
TOKEN=$(grep 'Token:' ~/.picoclaw/workspace/GITLAB.md | sed 's/.*Token: *//' | tr -d '\r\n')

# 2. Clone repo
git clone https://oauth2:${TOKEN}@gitlab.git4ta.fun/用户名/仓库.git

# 3. List projects
curl -s -H "PRIVATE-TOKEN: $TOKEN" https://gitlab.git4ta.fun/api/v4/projects

# 4. Create issue
curl -s -X POST -H "PRIVATE-TOKEN: $TOKEN" \
  https://gitlab.git4ta.fun/api/v4/projects/PROJECT_ID/issues \
  -d "title=标题" -d "description=描述"
```
