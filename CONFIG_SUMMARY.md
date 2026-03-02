# AIGW 配置经验总结

> **最后更新**: 2026-02-15 22:40
> **状态**: ✅ 已验证可用

---

## 1. 核心配置信息

### 1.1 API 端点

| 环境 | 域名 | 网络要求 |
|------|------|----------|
| 外网（推荐） | `https://aigw.netease.com` | SAVPN/办公网 |
| 内网 | `https://aigw-int.netease.com` | IDC/VPN |

### 1.2 认证信息

```
App ID:  a3qanjtg0juk4juz
App Key: 68ip3dor15ojfusqph4z5nz907q5l2zr
App Code: _lidezhe_crystalball_01

认证格式: Bearer {app_id}.{app_key}
完整示例: Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr
```

---

## 2. 可用模型列表（21个）

### 2.1 Claude 系列（8个）

| 模型 ID | 上下文 | 输出 | 推荐场景 |
|---------|--------|------|----------|
| `claude-opus-4-6` | 200K | 128K | **最强推理**、复杂任务 |
| `claude-sonnet-4-20250514` | 200K | 64K | **日常首选**、平衡性能 |
| `claude-haiku-4-5-20251001` | 200K | 64K | **快速响应**、简单任务 |
| `claude-3-7-sonnet-20250219` | 200K | 64K | 稳定版 Sonnet |
| `claude-3-5-sonnet-20241022` | 200K | 8K | Claude 3.5 Sonnet |
| `claude-3-5-haiku-20241022` | 200K | 8K | Claude 3.5 Haiku |
| `claude-3-sonnet-20240229` | 200K | 4K | Claude 3 Sonnet |
| `claude-3-haiku-20240307` | 200K | 4K | Claude 3 Haiku |

### 2.2 Gemini 系列（3个）

| 模型 ID | 上下文 | 输出 | 推荐场景 |
|---------|--------|------|----------|
| `gemini-3-flash` | 1M | 65K | **超大上下文**、多模态 |
| `gemini-2.5-pro` | 1M | 65K | 高级推理 |
| `gemini-2.5-flash` | 1M | 65K | 快速响应 |

### 2.3 DeepSeek 系列（3个）

| 模型 ID | 上下文 | 输出 | 推荐场景 |
|---------|--------|------|----------|
| `deepseek-chat` | 128K | 65K | **成本敏感**、通用对话 |
| `deepseek-reasoner` | 128K | 65K | 复杂推理、思维链 |
| `deepseek-v3.2-think-bd-251201` | 128K | 65K | 最新思维链模型 |

### 2.4 Qwen 系列（4个）

| 模型 ID | 上下文 | 输出 | 推荐场景 |
|---------|--------|------|----------|
| `qwen-turbo` | 128K | 8K | **中文优化**、快速响应 |
| `qwen-max` | 128K | 8K | 高质量中文 |
| `qwen-plus` | 128K | 8K | 增强版 |
| `qwen3-max-2026-01-23` | 128K | 8K | 最新 Qwen3 |

### 2.5 其他（3个）

| 模型 ID | 上下文 | 输出 | 推荐场景 |
|---------|--------|------|----------|
| `kimi-k2.5` | 262K | 32K | **长文档**、文档阅读 |
| `doubao-seed-1.8` | 256K | 64K | 字节豆包 |
| `MiniMax-M1` | 128K | 8K | MiniMax |

---

## 3. Claude Code 配置

### 3.1 配置文件位置

```
~/.claude/settings.json
```

### 3.2 完整配置内容

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr",
    "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-20250514",
    "ANTHROPIC_MODEL": "claude-opus-4-6",
    "ANTHROPIC_VERSION": "2023-06-01"
  },
  "includeCoAuthoredBy": false
}
```

### 3.3 命令行启动方式

```bash
# 基础启动
ANTHROPIC_BASE_URL=https://aigw.netease.com \
ANTHROPIC_AUTH_TOKEN=a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr \
ANTHROPIC_MODEL=claude-opus-4-6 \
claude

# 使用环境变量
export ANTHROPIC_BASE_URL=https://aigw.netease.com
export ANTHROPIC_AUTH_TOKEN=a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr
export ANTHROPIC_MODEL=claude-opus-4-6
claude
```

### 3.4 Claude Code 常用命令

```bash
# 命令行
claude -h          # 帮助
claude -v          # 查看版本
claude update      # 更新版本
claude -c          # 恢复最近对话
claude -r          # 选择历史对话

# 内部命令
/model             # 切换模型
/cost              # 查看花费
/compact           # 压缩上下文
/clear             # 清除会话
```

---

## 4. CC Switch 配置

### 4.1 数据库位置

```
~/.cc-switch/cc-switch.db        # SQLite 数据库
~/.cc-switch/settings.json       # 应用设置
~/.cc-switch/backups/            # 备份目录
```

### 4.2 Provider 配置

**Claude Provider ID:** `netease-aigw-claude`

```json
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr",
        "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-6",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-20250514",
        "ANTHROPIC_MODEL": "claude-opus-4-6",
        "ANTHROPIC_VERSION": "2023-06-01"
    },
    "includeCoAuthoredBy": false
}
```

**OpenCode Provider ID:** `netease-aigw`

```json
{
    "models": {
        "claude-opus-4-6": {"limit": {"context": 200000, "output": 128000}, "name": "Claude Opus 4.6"},
        "claude-sonnet-4-20250514": {"limit": {"context": 200000, "output": 64000}, "name": "Claude Sonnet 4"},
        "claude-haiku-4-5-20251001": {"limit": {"context": 200000, "output": 64000}, "name": "Claude Haiku 4.5"},
        "claude-3-7-sonnet-20250219": {"limit": {"context": 200000, "output": 64000}, "name": "Claude 3.7 Sonnet"},
        "claude-3-5-sonnet-20241022": {"limit": {"context": 200000, "output": 8192}, "name": "Claude 3.5 Sonnet"},
        "claude-3-5-haiku-20241022": {"limit": {"context": 200000, "output": 8192}, "name": "Claude 3.5 Haiku"},
        "claude-3-sonnet-20240229": {"limit": {"context": 200000, "output": 4096}, "name": "Claude 3 Sonnet"},
        "claude-3-haiku-20240307": {"limit": {"context": 200000, "output": 4096}, "name": "Claude 3 Haiku"},
        "gemini-3-flash": {"limit": {"context": 1048576, "output": 65536}, "name": "Gemini 3 Flash"},
        "gemini-2.5-pro": {"limit": {"context": 1048576, "output": 65536}, "name": "Gemini 2.5 Pro"},
        "gemini-2.5-flash": {"limit": {"context": 1048576, "output": 65536}, "name": "Gemini 2.5 Flash"},
        "deepseek-chat": {"limit": {"context": 128000, "output": 65536}, "name": "DeepSeek Chat"},
        "deepseek-reasoner": {"limit": {"context": 128000, "output": 65536}, "name": "DeepSeek Reasoner"},
        "deepseek-v3.2-think-bd-251201": {"limit": {"context": 128000, "output": 65536}, "name": "DeepSeek V3.2 Think"},
        "qwen-turbo": {"limit": {"context": 128000, "output": 8192}, "name": "Qwen Turbo"},
        "qwen-max": {"limit": {"context": 128000, "output": 8192}, "name": "Qwen Max"},
        "qwen-plus": {"limit": {"context": 128000, "output": 8192}, "name": "Qwen Plus"},
        "qwen3-max-2026-01-23": {"limit": {"context": 128000, "output": 8192}, "name": "Qwen3 Max"},
        "kimi-k2.5": {"limit": {"context": 262144, "output": 32768}, "name": "Kimi K2.5"},
        "doubao-seed-1.8": {"limit": {"context": 256000, "output": 64000}, "name": "Doubao Seed 1.8"},
        "MiniMax-M1": {"limit": {"context": 128000, "output": 8192}, "name": "MiniMax M1"}
    },
    "npm": "@ai-sdk/openai-compatible",
    "options": {
        "baseURL": "https://aigw.netease.com/v1",
        "headers": {
            "Authorization": "Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr"
        }
    }
}
```

### 4.3 更新数据库命令

```bash
python3 << 'EOF'
import sqlite3
import json

claude_config = '''{"env":{"ANTHROPIC_AUTH_TOKEN":"...",...}}'''
opencode_config = '''{"models":{...},"npm":"@ai-sdk/openai-compatible",...}'''

conn = sqlite3.connect('/Users/tangdan/.cc-switch/cc-switch.db')
cursor = conn.cursor()

cursor.execute("""
    UPDATE providers SET settings_config = ?
    WHERE id = 'netease-aigw-claude' AND app_type = 'claude'
""", (claude_config,))

cursor.execute("""
    UPDATE providers SET settings_config = ?
    WHERE id = 'netease-aigw' AND app_type = 'opencode'
""", (opencode_config,))

conn.commit()
conn.close()
EOF
```

---

## 5. 网络连接测试

### 5.1 快速测试命令

```bash
# 测试外网 AIGW
curl -s "https://aigw.netease.com/v1/chat/completions" \
  -H "Authorization: Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-6","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

### 5.2 判断响应

| 响应内容 | 状态 |
|----------|------|
| `"choices":[...]` | ✅ 成功 |
| `no available resource` | ❌ 模型未开通 |
| `not supported` | ❌ 模型名错误 |
| `invalid Authorization` | ❌ 认证失败 |
| 超时/无响应 | ❌ 网络问题 |

---

## 6. 常见问题排查

### 6.1 认证失败

**症状:** `invalid Authorization value`

**检查:**
1. App ID 和 App Key 格式是否正确
2. 认证头格式：`Bearer {app_id}.{app_key}`
3. 账号是否有效/激活

### 6.2 模型不可用

**症状:** `no available resource for this model`

**解决:**
1. 在 ModelSpace 检查模型开通状态
2. 申请开通需要的模型
3. 使用已开通的模型列表中的模型

### 6.3 CC Switch 代理不工作

**症状:** `未配置供应商`

**解决:**
1. 打开 CC Switch 应用
2. 找到并启用 "网易 AIGW" Provider
3. 重启 CC Switch 应用
4. 重启 Claude Code

### 6.4 网络超时

**症状:** 连接超时

**解决:**
1. 确认 SAVPN 已连接
2. 尝试切换内外网域名
3. 检查防火墙设置

---

## 7. 文件备份清单

| 文件 | 位置 | 说明 |
|------|------|------|
| Claude Code 配置 | `~/.claude/settings.json` | Claude Code 设置 |
| CC Switch 数据库 | `~/.cc-switch/cc-switch.db` | Provider 配置 |
| CC Switch 设置 | `~/.cc-switch/settings.json` | 应用设置 |
| 完整配置指南 | `~/Desktop/netease_aigw/AIGW_COMPLETE_GUIDE.md` | 详细文档 |
| 模型测试结果 | `~/Desktop/netease_aigw/MODEL_TEST_RESULTS.md` | 测试记录 |
| 配置经验总结 | `~/Desktop/netease_aigw/CONFIG_SUMMARY.md` | 本文档 |

---

## 8. 官方资源链接

| 资源 | URL |
|------|-----|
| ModelSpace | https://modelspace.netease.com/model_app |
| APP 管理 | https://modelspace.netease.com/model_access/app_manage |
| Auth 控制台 | https://console-auth.nie.netease.com/mymessage/mymessage |
| AIGW 文档 | https://aigw.doc.nie.netease.com |
| Claude Code 文档 | https://docs.anthropic.com/en/docs/claude-code/overview |

---

## 9. 配置变更历史

| 日期 | 变更内容 |
|------|----------|
| 2026-02-15 | 初始配置，测试 41 个模型，确认 21 个可用 |
| 2026-02-15 | 更新 CC Switch 配置，添加所有可用模型 |
| 2026-02-15 | 创建完整配置文档和经验总结 |

---

**维护建议:** 每次配置变更后，更新此文档的变更历史记录。
