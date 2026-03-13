# CC Switch 配置 OpenAI 兼容模型指南

> **适用版本**: CC Switch 3.10.x+
> **创建时间**: 2026-03-14
> **场景**: 在 CC Switch 中配置 AIGW 提供的 OpenAI 兼容模型（GPT-5.2 Codex、DeepSeek、Gemini 等），使 Claude Code 能通过 AIGW 调用这些模型

---

## 目录

- [背景说明](#背景说明)
- [架构原理](#架构原理)
- [配置步骤](#配置步骤)
- [关键注意事项](#关键注意事项)
- [验证配置](#验证配置)
- [常见问题排查](#常见问题排查)
- [多 Provider 切换](#多-provider-切换)
- [附录：支持的 OpenAI 兼容模型](#附录支持的-openai-兼容模型)

---

## 背景说明

Claude Code 原生只支持 Anthropic API 格式。当你想通过 AIGW 使用 OpenAI 兼容模型（如 GPT-5.2 Codex）时，需要 CC Switch 作为中间代理，自动完成 **Anthropic 格式 ↔ OpenAI Chat 格式** 的双向转换。

```
Claude Code (Anthropic 格式)
  → CC Switch 本地代理 (格式转换)
    → 网易 AIGW (OpenAI Chat 格式)
      → GPT-5.2 Codex / DeepSeek / Gemini / ...
```

---

## 架构原理

### CC Switch 的 API 格式转换

CC Switch 内部有一个 `apiFormat` 字段控制请求格式：

| apiFormat 值 | 行为 | 适用模型 |
|-------------|------|----------|
| `"anthropic"` (默认) | 直接以 Anthropic 格式转发 | Claude 系列 |
| `"openai_chat"` | 将 Anthropic 格式**转换为 OpenAI Chat 格式**后转发 | GPT、Codex、Gemini、Qwen、DeepSeek 等 |

### 转换内容

CC Switch 的 `transform.rs` 模块处理以下转换：

| 方向 | 转换内容 |
|------|----------|
| 请求（Anthropic → OpenAI） | `messages` 格式、`system` 提示词、`tools` 工具定义、`max_tokens` 等参数 |
| 响应（OpenAI → Anthropic） | `choices` → Anthropic `content` 格式、`usage` 统计、`stop_reason` 等 |

---

## 配置步骤

### 前提条件

1. 已安装 CC Switch（`/Applications/CC Switch.app`）
2. 已有 AIGW 账号和 API 凭证
3. AIGW 账号已开通目标模型的访问权限

### 第一步：准备信息

你需要以下信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| Provider ID | 唯一标识符（自定义） | `netease-aigw-myaccount-codex` |
| Provider 名称 | 显示名称 | `网易 AIGW - Codex` |
| AIGW 凭证 | `AppID.AppKey` | `xxxx.yyyy` |
| 模型 ID | AIGW 中的模型代号 | `gpt-5.2-codex-2026-01-14` |

### 第二步：在数据库中新增 Provider

> CC Switch 的配置存储在 SQLite 数据库 `~/.cc-switch/cc-switch.db` 的 `providers` 表中。

```sql
-- 插入新的 Codex Provider
INSERT INTO providers (
  id, app_type, name, settings_config, meta, is_current, provider_type
) VALUES (
  'netease-aigw-myaccount-codex',
  'claude',
  '网易 AIGW - MyAccount (GPT-5.2 Codex)',
  json('{
    "env": {
      "ANTHROPIC_AUTH_TOKEN": "你的AppID.你的AppKey",
      "ANTHROPIC_BASE_URL": "https://aigw.netease.com",
      "ANTHROPIC_MODEL": "gpt-5.2-codex-2026-01-14",
      "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gpt-5.2-codex-2026-01-14",
      "ANTHROPIC_DEFAULT_SONNET_MODEL": "gpt-5.2-codex-2026-01-14",
      "ANTHROPIC_DEFAULT_OPUS_MODEL": "gpt-5.2-codex-2026-01-14",
      "ANTHROPIC_REASONING_MODEL": "gpt-5.2-codex-2026-01-14",
      "ANTHROPIC_VERSION": "2023-06-01"
    },
    "includeCoAuthoredBy": false
  }'),
  json('{"endpointAutoSelect": true, "apiFormat": "openai_chat"}'),
  0,
  NULL
);
```

**执行命令：**

```bash
sqlite3 ~/.cc-switch/cc-switch.db "INSERT INTO providers (id, app_type, name, settings_config, meta, is_current, provider_type) VALUES ('netease-aigw-myaccount-codex', 'claude', '网易 AIGW - MyAccount (GPT-5.2 Codex)', '{\"env\":{\"ANTHROPIC_AUTH_TOKEN\":\"你的AppID.你的AppKey\",\"ANTHROPIC_BASE_URL\":\"https://aigw.netease.com\",\"ANTHROPIC_MODEL\":\"gpt-5.2-codex-2026-01-14\",\"ANTHROPIC_DEFAULT_HAIKU_MODEL\":\"gpt-5.2-codex-2026-01-14\",\"ANTHROPIC_DEFAULT_SONNET_MODEL\":\"gpt-5.2-codex-2026-01-14\",\"ANTHROPIC_DEFAULT_OPUS_MODEL\":\"gpt-5.2-codex-2026-01-14\",\"ANTHROPIC_REASONING_MODEL\":\"gpt-5.2-codex-2026-01-14\",\"ANTHROPIC_VERSION\":\"2023-06-01\"},\"includeCoAuthoredBy\":false}', '{\"endpointAutoSelect\":true,\"apiFormat\":\"openai_chat\"}', 0, NULL);"
```

### 第三步：切换到新 Provider

**方式一：通过 CC Switch 界面**（推荐）

1. 打开 CC Switch 应用
2. 在 Provider 列表中找到新建的 Codex Provider
3. 点击切换

**方式二：通过数据库 + 配置文件**

```bash
# 1. 取消当前 Provider
sqlite3 ~/.cc-switch/cc-switch.db "UPDATE providers SET is_current = 0 WHERE app_type = 'claude' AND is_current = 1;"

# 2. 激活 Codex Provider
sqlite3 ~/.cc-switch/cc-switch.db "UPDATE providers SET is_current = 1 WHERE id = 'netease-aigw-myaccount-codex' AND app_type = 'claude';"
```

同时更新 `~/.cc-switch/settings.json`：

```bash
# macOS/Linux - 使用 sed 更新（或手动编辑）
sed -i '' 's/"currentProviderClaude": "[^"]*"/"currentProviderClaude": "netease-aigw-myaccount-codex"/' ~/.cc-switch/settings.json
```

### 第四步：重启 CC Switch

配置修改后**必须重启 CC Switch** 才能生效。

---

## 关键注意事项

### 1. apiFormat 必须是 `"openai_chat"`（最重要！）

CC Switch 源码中的格式判断逻辑：

```rust
// src-tauri/src/proxy/providers/claude.rs
fn get_api_format(&self, provider: &Provider) -> &'static str {
    if let Some(api_format) = meta.api_format.as_deref() {
        return if api_format == "openai_chat" {
            "openai_chat"     // ← 只有精确匹配 "openai_chat" 才走 OpenAI 格式
        } else {
            "anthropic"       // ← 其他任何值（包括 "openai"）都走 Anthropic 格式
        };
    }
    // ...
}
```

| 设置值 | 结果 | 是否正确 |
|--------|------|----------|
| `"openai_chat"` | 转换为 OpenAI Chat 格式 | **正确** |
| `"openai"` | 走 Anthropic 格式（else 分支） | **错误** |
| `"OpenAI_Chat"` | 走 Anthropic 格式（大小写敏感） | **错误** |
| `""` 或 不设置 | 走 Anthropic 格式 | **错误** |

**踩坑经验**：设置 `"apiFormat": "openai"` 会导致报错 `format [atrp.messages] is not available for [gpt-5.2-codex-2026-01-14]`，因为 AIGW 收到了 Anthropic 格式的请求，但 GPT/Codex 模型不支持该格式。

### 2. 所有模型环境变量都要设置为目标模型

Claude Code 在不同场景会使用不同的模型环境变量：

| 环境变量 | 用途 |
|---------|------|
| `ANTHROPIC_MODEL` | 主模型 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 默认 Sonnet 级别任务 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | 默认 Opus 级别任务 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 默认 Haiku 级别任务 |
| `ANTHROPIC_REASONING_MODEL` | 推理任务 |

**全部设置为同一个模型 ID**，否则部分请求仍会尝试调用 Claude 模型。

### 3. 新建 Provider 而非覆盖现有 Claude Provider

建议为每个模型创建独立的 Provider，这样可以在 CC Switch 中自由切换：

```
├── 网易 AIGW - Claude Opus 4.6    (apiFormat: anthropic)
├── 网易 AIGW - GPT-5.2 Codex      (apiFormat: openai_chat)  ← 新建
├── 网易 AIGW - DeepSeek Chat       (apiFormat: openai_chat)  ← 新建
└── 网易 AIGW - Gemini 2.5 Pro      (apiFormat: openai_chat)  ← 新建
```

### 4. 切换 Provider 需要同步两个位置

| 位置 | 字段 | 说明 |
|------|------|------|
| 数据库 `providers` 表 | `is_current = 1` | 标记活跃 Provider |
| `~/.cc-switch/settings.json` | `currentProviderClaude` | 启动时读取 |

两者不一致会导致 CC Switch 重启后回退到旧 Provider。

### 5. 修改数据库后必须重启 CC Switch

CC Switch 启动时加载配置到内存，运行中不会自动重新读取数据库。

---

## 验证配置

### 1. 检查数据库配置

```bash
# 查看当前活跃的 Provider
sqlite3 ~/.cc-switch/cc-switch.db \
  "SELECT id, name, is_current, json_extract(meta, '$.apiFormat') as fmt FROM providers WHERE app_type='claude';"

# 期望输出（Codex 行的 is_current=1, fmt=openai_chat）：
# netease-aigw-myaccount-codex|网易 AIGW - Codex|1|openai_chat
```

### 2. 检查 settings.json

```bash
grep currentProviderClaude ~/.cc-switch/settings.json
# 期望输出：
# "currentProviderClaude": "netease-aigw-myaccount-codex"
```

### 3. 测试 AIGW 直连（排除 CC Switch 问题）

```bash
curl -s -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Authorization: Bearer 你的AppID.你的AppKey" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.2-codex-2026-01-14",
    "messages": [{"role": "user", "content": "Say hello"}],
    "max_tokens": 50
  }'
```

### 4. 测试 CC Switch 代理转发

```bash
# 确认代理在运行
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:15721/
# 期望输出: 404（代理在运行，只是根路径没有处理）

# 通过代理发送 Anthropic 格式请求（模拟 Claude Code）
curl -s -X POST "http://127.0.0.1:15721/v1/messages" \
  -H "x-api-key: 你的AppID.你的AppKey" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.2-codex-2026-01-14",
    "max_tokens": 50,
    "messages": [{"role": "user", "content": "Say hello"}]
  }'
```

---

## 常见问题排查

### 问题 1: `format [atrp.messages] is not available for [model]`

**原因**：请求以 Anthropic 格式（`atrp.messages`）发送，但目标模型不支持 Anthropic 格式。

**排查步骤**：

```bash
# 1. 检查 apiFormat 是否正确
sqlite3 ~/.cc-switch/cc-switch.db \
  "SELECT json_extract(meta, '$.apiFormat') FROM providers WHERE id = '你的provider_id';"

# 如果输出不是 openai_chat，执行修复：
sqlite3 ~/.cc-switch/cc-switch.db \
  "UPDATE providers SET meta = json_set(meta, '$.apiFormat', 'openai_chat') WHERE id = '你的provider_id';"

# 2. 重启 CC Switch
```

### 问题 2: Provider 切换后不生效

**排查步骤**：

```bash
# 检查 settings.json 是否同步
grep currentProviderClaude ~/.cc-switch/settings.json

# 检查数据库 is_current
sqlite3 ~/.cc-switch/cc-switch.db \
  "SELECT id, is_current FROM providers WHERE app_type='claude' AND is_current=1;"

# 两者必须一致，然后重启 CC Switch
```

### 问题 3: CC Switch 代理未运行

```bash
# 检查代理端口
curl -s http://127.0.0.1:15721/ 2>&1 || echo "代理未运行"

# 检查 CC Switch 进程
ps aux | grep -i "CC Switch" | grep -v grep

# 解决：打开 CC Switch 应用，确保代理处于"已接管"状态
```

### 问题 4: 代理已接管但请求失败

```bash
# 查看 CC Switch 日志
cat ~/.cc-switch/logs/cc-switch.log | tail -50

# 检查 Claude Code 的环境变量
cat ~/.claude/settings.json
# 应该包含：
# "ANTHROPIC_BASE_URL": "http://127.0.0.1:15721"
# "ANTHROPIC_AUTH_TOKEN": "PROXY_MANAGED"
```

---

## 多 Provider 切换

### 创建多个模型 Provider 的脚本

项目提供了 `scripts/create_ccswitch_provider.sh` 脚本来快速创建 Provider：

```bash
chmod +x scripts/create_ccswitch_provider.sh

# Claude 模型（使用 anthropic 格式）
./scripts/create_ccswitch_provider.sh "aigw-claude" "AIGW Claude Opus" "claude-opus-4-6" "appid.appkey" "anthropic"

# Codex 模型（使用 openai_chat 格式）
./scripts/create_ccswitch_provider.sh "aigw-codex" "AIGW Codex" "gpt-5.2-codex-2026-01-14" "appid.appkey" "openai_chat"

# DeepSeek 模型（使用 openai_chat 格式）
./scripts/create_ccswitch_provider.sh "aigw-deepseek" "AIGW DeepSeek" "deepseek-chat" "appid.appkey" "openai_chat"

# Gemini 模型（使用 openai_chat 格式）
./scripts/create_ccswitch_provider.sh "aigw-gemini" "AIGW Gemini" "gemini-2.5-pro" "appid.appkey" "openai_chat"
```

### apiFormat 速查表

| 模型系列 | apiFormat | 说明 |
|---------|-----------|------|
| Claude 系列 | `anthropic` | 原生 Anthropic 格式，无需转换 |
| GPT / Codex 系列 | `openai_chat` | 需要格式转换 |
| DeepSeek 系列 | `openai_chat` | OpenAI 兼容接口 |
| Qwen 系列 | `openai_chat` | OpenAI 兼容接口 |
| Gemini 系列 | `openai_chat` | OpenAI 兼容接口 |
| Kimi 系列 | `openai_chat` | OpenAI 兼容接口 |
| 豆包系列 | `openai_chat` | OpenAI 兼容接口 |
| MiniMax 系列 | `openai_chat` | OpenAI 兼容接口 |
| GLM 系列 | `openai_chat` | OpenAI 兼容接口 |

**简单规则**：除了 Claude 系列用 `anthropic`，其他所有模型都用 `openai_chat`。

---

## 附录：支持的 OpenAI 兼容模型

以下模型均可通过 AIGW + CC Switch（`apiFormat: openai_chat`）在 Claude Code 中使用：

| 模型 ID | 提供商 | 说明 |
|---------|--------|------|
| `gpt-5.2-codex-2026-01-14` | OpenAI | 代码优化模型 |
| `gpt-4o` | OpenAI | 多模态模型 |
| `deepseek-chat` | DeepSeek | 通用对话 |
| `deepseek-reasoner` | DeepSeek | 推理增强 |
| `qwen-max` | 阿里 | 通义千问旗舰 |
| `qwen3-coder-plus` | 阿里 | 代码专用 |
| `gemini-2.5-pro` | Google | Gemini Pro |
| `gemini-3-flash` | Google | 超大上下文 |
| `kimi-k2.5` | 月之暗面 | 中文优化 |
| `doubao-seed-1.8` | 字节 | 快速便宜 |
| `MiniMax-M2.5` | MiniMax | 平衡型 |
| `glm-5` | 智谱 | 旗舰模型 |

> 完整模型列表请参考 [MODELS.md](MODELS.md) 和 [ModelSpace 控制台](https://modelspace.netease.com/)。

---

**文档版本**: 1.0.0
**最后更新**: 2026-03-14
