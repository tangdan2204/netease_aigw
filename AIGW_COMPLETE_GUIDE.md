# 网易 AIGW 完整配置指南

> **文档版本**: 2.0  
> **最后更新**: 2026-02-15  
> **验证状态**: 所有配置已实测通过

---

## 目录

1. [网络连接信息](#1-网络连接信息)
2. [认证方式](#2-认证方式)
3. [已验证可用模型](#3-已验证可用模型)
4. [Claude Code 配置](#4-claude-code-配置)
5. [CC Switch 配置](#5-cc-switch-配置)
6. [OpenCode 配置](#6-opencode-配置)
7. [API 调用示例](#7-api-调用示例)
8. [故障排查](#8-故障排查)
9. [配置文件备份](#9-配置文件备份)

---

## 1. 网络连接信息

### 域名选择

| 域名 | 用途 | 网络要求 | 推荐场景 |
|------|------|----------|----------|
| `aigw.netease.com` | 外网 | SAVPN/办公网 | 工位测试、无VPN |
| `aigw-int.netease.com` | 内网 | IDC/VPN | 机房部署、有VPN |

### 网络测试命令

```bash
# 测试外网连通性
curl -s --connect-timeout 5 --max-time 15 \
  "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "claude-3-5-sonnet-20241022", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}'

# 测试内网连通性（需要VPN）
curl -s --connect-timeout 5 --max-time 15 \
  "https://aigw-int.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{"model": "claude-opus-4-6", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}'
```

### DNS 解析

```
aigw.netease.com      -> 外网IP
aigw-int.netease.com  -> 10.91.39.75, 10.204.61.53 (内网IP)
```

---

## 2. 认证方式

### 方式一：APP 账号认证（推荐）

**获取凭证：**
1. 访问 [ModelSpace APP 管理](https://modelspace.netease.com/model_access/app_manage)
2. 创建或选择 APP
3. 获取 `App ID` 和 `App Key`

**认证格式：**
```
Authorization: Bearer {app_id}.{app_key}
```

**示例：**
```bash
Authorization: Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr
```

### 方式二：Auth 体系认证

适用于多用户、多角色管理场景。

**请求头：**
```
X-AIGW-APP: {app_code}
X-Access-Token: {auth_token}
```

**获取 Auth Token：**
访问 [Auth 权限中心](https://console-auth.nie.netease.com/mymessage/mymessage) 获取 v2 Token

---

## 3. 已验证可用模型

> **测试时间**: 2026-02-15 22:10  
> **可用模型总数**: 21个

### 3.1 Claude 系列（8个可用）

| 模型 ID | 验证状态 | 说明 | 上下文 | 输出 |
|---------|----------|------|--------|------|
| `claude-opus-4-6` | ✅ | 最新最强推理模型 | 200K | 128K |
| `claude-sonnet-4-20250514` | ✅ | Claude 4 Sonnet | 200K | 64K |
| `claude-haiku-4-5-20251001` | ✅ | Claude 4.5 Haiku | 200K | 64K |
| `claude-3-7-sonnet-20250219` | ✅ | Claude 3.7 Sonnet | 200K | 64K |
| `claude-3-5-sonnet-20241022` | ✅ | Claude 3.5 Sonnet | 200K | 8K |
| `claude-3-5-haiku-20241022` | ✅ | Claude 3.5 Haiku | 200K | 8K |
| `claude-3-sonnet-20240229` | ✅ | Claude 3 Sonnet | 200K | 4K |
| `claude-3-haiku-20240307` | ✅ | Claude 3 Haiku | 200K | 4K |

### 3.2 Gemini 系列（3个可用）

| 模型 ID | 验证状态 | 说明 | 上下文 | 输出 |
|---------|----------|------|--------|------|
| `gemini-3-flash` | ✅ | Gemini 3 Flash | 1M | 65K |
| `gemini-2.5-pro` | ✅ | Gemini 2.5 Pro | 1M | 65K |
| `gemini-2.5-flash` | ✅ | Gemini 2.5 Flash | 1M | 65K |

### 3.3 DeepSeek 系列（3个可用）

| 模型 ID | 验证状态 | 说明 | 上下文 | 输出 |
|---------|----------|------|--------|------|
| `deepseek-chat` | ✅ | 通用对话 | 128K | 65K |
| `deepseek-reasoner` | ✅ | 推理专家 | 128K | 65K |
| `deepseek-v3.2-think-bd-251201` | ✅ | V3.2 思维链 | 128K | 65K |

### 3.4 Qwen 系列（4个可用）

| 模型 ID | 验证状态 | 说明 | 上下文 | 输出 |
|---------|----------|------|--------|------|
| `qwen-turbo` | ✅ | 快速版 | 128K | 8K |
| `qwen-max` | ✅ | 高级版 | 128K | 8K |
| `qwen-plus` | ✅ | 增强版 | 128K | 8K |
| `qwen3-max-2026-01-23` | ✅ | Qwen3 Max | 128K | 8K |

### 3.5 其他（3个可用）

| 模型 ID | 验证状态 | 说明 | 上下文 | 输出 |
|---------|----------|------|--------|------|
| `kimi-k2.5` | ✅ | 月之暗面 | 262K | 32K |
| `doubao-seed-1.8` | ✅ | 字节豆包 | 256K | 64K |
| `MiniMax-M1` | ✅ | MiniMax | 128K | 8K |

### 3.6 需要申请开通

| 模型 ID | 状态 | 说明 |
|---------|------|------|
| `glm-5` | ❌ 无资源 | 智谱 GLM-5，需要在 ModelSpace 申请 |

### 3.7 不支持（20个）

- **GPT 系列**: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4`, `gpt-3.5-turbo`, `gpt-5`, `gpt-5.2-codex`
- **旧版 Gemini**: `gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **智谱 GLM**: `glm-4-plus`, `glm-4-air`, `glm-4-airx`, `glm-4v`
- **其他**: `kimi-k2.5-search`, `kimi-k1.5`, `doubao-pro-32k`, `doubao-pro-128k`, `MiniMax-M2`, `MiniMax-M3`, `ernie-4.5-turbo`, `ernie-4.0`

---

## 4. Claude Code 配置

### 4.1 命令行启动

```bash
# 基础启动（使用 claude-opus-4-6）
ANTHROPIC_BASE_URL=https://aigw.netease.com \
ANTHROPIC_AUTH_TOKEN=YOUR_APP_ID.YOUR_APP_KEY \
ANTHROPIC_MODEL=claude-opus-4-6 \
claude

# 完整参数启动
ANTHROPIC_BASE_URL=https://aigw.netease.com \
ANTHROPIC_AUTH_TOKEN=YOUR_APP_ID.YOUR_APP_KEY \
ANTHROPIC_MODEL=claude-opus-4-6 \
ANTHROPIC_SMALL_FAST_MODEL=claude-3-5-haiku-20241022 \
claude
```

### 4.2 配置文件方式

**文件位置：** `~/.claude/settings.json`

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_APP_ID.YOUR_APP_KEY",
    "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-20250514",
    "ANTHROPIC_MODEL": "claude-opus-4-6",
    "ANTHROPIC_VERSION": "2023-06-01",
    "ENABLE_TOOL_SEARCH": "false"
  },
  "includeCoAuthoredBy": false
}
```

> ⚠️ **重要**：必须设置 `ENABLE_TOOL_SEARCH": "false"`，否则长时间对话后会出现 `tool_reference` 相关 API 错误。详见 [8.5 ToolSearch 兼容问题](#85-toolsearch-兼容问题重要)。

### 4.3 Auth 认证方式配置

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
    "ANTHROPIC_API_KEY": "foo",
    "ANTHROPIC_CUSTOM_HEADERS": "X-Aigw-App:YOUR_APP_CODE\nX-Access-Token:YOUR_AUTH_TOKEN"
  }
}
```

### 4.4 Claude Code 常用命令

```bash
claude -h          # 帮助
claude -v          # 查看版本
claude update      # 更新 Claude Code
claude -c          # 恢复最近对话
claude -r          # 选择恢复历史对话

# 在 Claude Code 内部
/model             # 切换模型
/cost              # 查看花费
/compact           # 压缩上下文
/clear             # 清除会话
```

---

## 5. CC Switch 配置

### 5.1 数据库位置

```
~/.cc-switch/cc-switch.db (SQLite)
~/.cc-switch/settings.json (设备设置)
```

### 5.2 Claude Provider 配置

**Provider ID:** `netease-aigw-claude`

```json
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_APP_ID.YOUR_APP_KEY",
        "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-3-5-haiku-20241022",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-3-7-sonnet-20250219",
        "ANTHROPIC_MODEL": "claude-opus-4-6",
        "ANTHROPIC_VERSION": "2023-06-01"
    },
    "includeCoAuthoredBy": false
}
```

### 5.3 OpenCode Provider 配置

**Provider ID:** `netease-aigw`

```json
{
    "models": {
        "claude-opus-4-6": {
            "limit": {"context": 200000, "output": 128000},
            "name": "Claude Opus 4.6"
        },
        "claude-3-7-sonnet-20250219": {
            "limit": {"context": 200000, "output": 64000},
            "name": "Claude 3.7 Sonnet"
        },
        "claude-3-5-sonnet-20241022": {
            "limit": {"context": 200000, "output": 8192},
            "name": "Claude 3.5 Sonnet"
        },
        "claude-3-5-haiku-20241022": {
            "limit": {"context": 200000, "output": 8192},
            "name": "Claude 3.5 Haiku"
        },
        "deepseek-chat": {
            "limit": {"context": 128000, "output": 65536},
            "name": "DeepSeek Chat"
        },
        "deepseek-reasoner": {
            "limit": {"context": 128000, "output": 65536},
            "name": "DeepSeek Reasoner"
        },
        "qwen-turbo": {
            "limit": {"context": 128000, "output": 8192},
            "name": "Qwen Turbo"
        },
        "qwen-max": {
            "limit": {"context": 128000, "output": 8192},
            "name": "Qwen Max"
        },
        "kimi-k2.5": {
            "limit": {"context": 262144, "output": 32768},
            "name": "Kimi K2.5"
        },
        "gemini-3-flash": {
            "limit": {"context": 1048576, "output": 65536},
            "name": "Gemini 3 Flash"
        }
    },
    "npm": "@ai-sdk/openai-compatible",
    "options": {
        "baseURL": "https://aigw.netease.com/v1",
        "headers": {
            "Authorization": "Bearer YOUR_APP_ID.YOUR_APP_KEY"
        }
    }
}
```

### 5.4 更新 CC Switch 配置命令

```bash
# 备份数据库
cp ~/.cc-switch/cc-switch.db ~/.cc-switch/cc-switch.db.bak.$(date +%Y%m%d%H%M%S)

# 使用 Python 更新
python3 << 'EOF'
import sqlite3

config = '''{"env":{"ANTHROPIC_AUTH_TOKEN":"YOUR_APP_ID.YOUR_APP_KEY",...}}'''

conn = sqlite3.connect('/Users/tangdan/.cc-switch/cc-switch.db')
cursor = conn.cursor()
cursor.execute("""
    UPDATE providers 
    SET settings_config = ?
    WHERE id = 'netease-aigw-claude' AND app_type = 'claude'
""", (config,))
conn.commit()
conn.close()
EOF
```

---

## 6. OpenCode 配置

### 6.1 配置文件位置

```
~/.config/opencode/opencode.json
```

### 6.2 完整配置

```json
{
  "provider": {
    "openai": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://aigw.netease.com/v1",
        "headers": {
          "Authorization": "Bearer YOUR_APP_ID.YOUR_APP_KEY"
        }
      },
      "models": {
        "claude-opus-4-6": {
          "name": "Claude Opus 4.6 (AIGW)",
          "description": "最强推理能力，适合复杂分析和代码生成",
          "limit": {"context": 200000, "output": 128000}
        },
        "claude-3-7-sonnet-20250219": {
          "name": "Claude 3.7 Sonnet (AIGW)",
          "description": "最新平衡版，适合日常对话和内容创作",
          "limit": {"context": 200000, "output": 64000}
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5 (AIGW)",
          "description": "长文本理解，适合文档阅读",
          "limit": {"context": 262144, "output": 32768}
        },
        "deepseek-chat": {
          "name": "DeepSeek Chat (AIGW)",
          "description": "通用对话模型，高性价比",
          "limit": {"context": 128000, "output": 65536}
        },
        "qwen-max": {
          "name": "Qwen Max (AIGW)",
          "description": "高质量输出，适合内容生成",
          "limit": {"context": 128000, "output": 8192}
        }
      }
    }
  }
}
```

---

## 7. API 调用示例

### 7.1 cURL 示例

```bash
# 基础对话
curl -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{
    "model": "claude-opus-4-6",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 1000
  }'

# 流式输出
curl -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -d '{
    "model": "claude-opus-4-6",
    "messages": [{"role": "user", "content": "讲一个故事"}],
    "max_tokens": 1000,
    "stream": true
  }'
```

### 7.2 Python 示例

```python
import requests

def call_aigw(prompt, model="claude-opus-4-6"):
    url = "https://aigw.netease.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer YOUR_APP_ID.YOUR_APP_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# 使用
result = call_aigw("你好，请介绍一下你自己")
print(result)
```

### 7.3 使用 OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_APP_ID.YOUR_APP_KEY",
    base_url="https://aigw.netease.com/v1"
)

response = client.chat.completions.create(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "你好"}],
    max_tokens=1000
)

print(response.choices[0].message.content)
```

---

## 8. 故障排查

### 8.1 连接问题

| 症状 | 可能原因 | 解决方案 |
|------|----------|----------|
| 连接超时 | 网络不通 | 检查VPN/办公网，尝试切换域名 |
| DNS 解析失败 | 内网DNS不可用 | 使用外网域名 |
| 403 Forbidden | IP不在白名单 | 确认SAVPN已连接 |

### 8.2 认证问题

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Invalid authentication` | 凭证格式错误 | 确认 `Bearer {app_id}.{app_key}` 格式 |
| `App not found` | App ID 错误 | 检查 ModelSpace 中的 App ID |
| `Invalid app key` | App Key 错误 | 重新复制 App Key |

### 8.3 模型问题

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `model is not supported` | 模型名错误 | 使用本文档中的正确模型名 |
| `no available resource` | APP 未开通该模型 | 联系管理员开通或更换模型 |
| `tool_reference tool_name: Field required` | Claude Code ToolSearch 兼容问题 | 详见 8.5 |
| `tool_reference ... does not match any of the expected tags` | Claude Code ToolSearch 兼容问题 | 详见 8.5 |

### 8.5 ToolSearch 兼容问题（重要）

> 当使用 Claude Code + AIGW 时，如果启用了 MCP 工具（Plugin），长时间对话后会出现 tool_reference 相关错误。

#### 错误示例

```
API Error: 400 [{"error":{"code":400,"message":"supplier response failed...
messages.3.content.0.tool_result.content.0.tool_reference.tool_name: Field required"}}]
```

或

```
messages.166.content.0.tool_result.content.0: Input tag 'tool_reference' found using 'type'
does not match any of the expected tags: 'document', 'image', 'search_result', 'text'
```

#### 原因

Claude Code 的 ToolSearch 功能会在工具结果中返回 `tool_reference` 类型的内容块，但 AIGW API 不支持这种类型（只支持 `text`, `image`, `document`, `search_result`）。

#### 解决方案

**方法一：关闭 ToolSearch（推荐）**

在配置中添加 `ENABLE_TOOL_SEARCH=false`：

```json
// ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "YOUR_APP_ID.YOUR_APP_KEY",
    "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
    "ANTHROPIC_MODEL": "claude-opus-4-6",
    "ENABLE_TOOL_SEARCH": "false"
  }
}
```

CC Switch 配置文件中也需添加相同配置。

**方法二：提高 ToolSearch 阈值**

如果不想完全关闭，可以提高触发阈值：

```json
{
  "env": {
    "ENABLE_TOOL_SEARCH": "auto:30"
  }
}
```

这表示当工具描述超过 30% 上下文时才启用 ToolSearch（默认是 10%）。

#### 影响说明

- **关闭 ToolSearch 的影响**：如果你的 MCP 工具很多（>10% 上下文），所有工具描述会随请求发送，消耗更多 token
- **建议**：如果平时只使用几个 MCP 工具，直接关闭即可，无明显影响

#### 相关 Issue

- [Claude Code Issue #28870](https://github.com/anthropics/claude-code/issues/28870): ToolSearch tool_reference causes API 400 error
- [Claude Code Issue #25212](https://github.com/anthropics/claude-code/issues/25212): ToolSearch generates tool_reference blocks on Bedrock

### 8.4 诊断命令

```bash
# 1. 测试网络连通性
ping aigw.netease.com
ping aigw-int.netease.com

# 2. 测试 DNS 解析
nslookup aigw.netease.com
nslookup aigw-int.netease.com

# 3. 测试 API 连通性
curl -v https://aigw.netease.com/v1/models \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY"

# 4. 测试特定模型
curl -s https://aigw.netease.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-6","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

---

## 9. 配置文件备份

### 9.1 需要备份的文件

```bash
# Claude Code
~/.claude/settings.json

# CC Switch
~/.cc-switch/cc-switch.db
~/.cc-switch/settings.json

# OpenCode
~/.config/opencode/opencode.json
```

### 9.2 备份命令

```bash
# 创建备份目录
mkdir -p ~/aigw-backup-$(date +%Y%m%d)

# 备份所有配置
cp ~/.claude/settings.json ~/aigw-backup-$(date +%Y%m%d)/claude-settings.json
cp ~/.cc-switch/cc-switch.db ~/aigw-backup-$(date +%Y%m%d)/cc-switch.db
cp ~/.cc-switch/settings.json ~/aigw-backup-$(date +%Y%m%d)/cc-switch-settings.json
cp ~/.config/opencode/opencode.json ~/aigw-backup-$(date +%Y%m%d)/opencode.json
```

---

## 附录：官方资源

| 资源 | URL | 说明 |
|------|-----|------|
| ModelSpace | https://modelspace.netease.com/model_app | 模型管理、APP管理 |
| Auth 控制台 | https://console-auth.nie.netease.com/mymessage/mymessage | 获取 Auth Token |
| AIGW 文档 | https://aigw.doc.nie.netease.com | 官方文档（内网） |
| Claude Code 文档 | https://docs.anthropic.com/en/docs/claude-code/overview | 官方使用指南 |

---

**文档维护**: 建议每次配置变更后更新此文档  
**版本**: 2.0.0  
**创建时间**: 2026-02-15  
**最后更新**: 2026-02-15
