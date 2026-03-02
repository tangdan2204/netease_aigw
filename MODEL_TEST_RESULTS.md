# AIGW 模型测试结果

> **测试时间**: 2026-02-15 22:10
> **APP Code**: `_lidezhe_crystalball_01`
> **测试环境**: 外网 `aigw.netease.com`

---

## 测试统计

| 状态 | 数量 |
|------|------|
| ✅ 可用 | 21 |
| ❌ 无资源(未开通) | 1 |
| ❌ 不支持 | 20 |

---

## ✅ 可用模型（21个）

### Claude 系列（8个）

| 模型 ID | 上下文 | 输出 | 说明 |
|---------|--------|------|------|
| `claude-opus-4-6` | 200K | 128K | 最新最强 |
| `claude-sonnet-4-20250514` | 200K | 64K | Claude 4 Sonnet |
| `claude-haiku-4-5-20251001` | 200K | 64K | Claude 4.5 Haiku |
| `claude-3-7-sonnet-20250219` | 200K | 64K | Claude 3.7 Sonnet |
| `claude-3-5-sonnet-20241022` | 200K | 8K | Claude 3.5 Sonnet |
| `claude-3-5-haiku-20241022` | 200K | 8K | Claude 3.5 Haiku |
| `claude-3-sonnet-20240229` | 200K | 4K | Claude 3 Sonnet |
| `claude-3-haiku-20240307` | 200K | 4K | Claude 3 Haiku |

### Gemini 系列（3个）

| 模型 ID | 上下文 | 输出 | 说明 |
|---------|--------|------|------|
| `gemini-3-flash` | 1M | 65K | Gemini 3 Flash |
| `gemini-2.5-pro` | 1M | 65K | Gemini 2.5 Pro |
| `gemini-2.5-flash` | 1M | 65K | Gemini 2.5 Flash |

### DeepSeek 系列（3个）

| 模型 ID | 上下文 | 输出 | 说明 |
|---------|--------|------|------|
| `deepseek-chat` | 128K | 65K | 通用对话 |
| `deepseek-reasoner` | 128K | 65K | 推理专家 |
| `deepseek-v3.2-think-bd-251201` | 128K | 65K | V3.2 思维链 |

### Qwen 系列（4个）

| 模型 ID | 上下文 | 输出 | 说明 |
|---------|--------|------|------|
| `qwen-turbo` | 128K | 8K | 快速版 |
| `qwen-max` | 128K | 8K | 高级版 |
| `qwen-plus` | 128K | 8K | 增强版 |
| `qwen3-max-2026-01-23` | 128K | 8K | Qwen3 Max |

### 其他（3个）

| 模型 ID | 上下文 | 输出 | 说明 |
|---------|--------|------|------|
| `kimi-k2.5` | 262K | 32K | 月之暗面 |
| `doubao-seed-1.8` | 256K | 64K | 字节豆包 |
| `MiniMax-M1` | 128K | 8K | MiniMax |

---

## ❌ 需要申请开通（1个）

| 模型 ID | 状态 | 说明 |
|---------|------|------|
| `glm-5` | 无资源 | 智谱 GLM-5，需要在 ModelSpace 申请 |

**申请方式：**
1. 访问 https://modelspace.netease.com/model_app/detail/glm-5
2. 点击"申请使用"
3. 等待审批通过

---

## ❌ 不支持（20个）

### GPT 系列（全部不支持）

- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-4`
- `gpt-3.5-turbo`
- `gpt-5`
- `gpt-5.2-codex-2026-01-14`

### 旧版 Gemini（不支持）

- `gemini-2.0-flash`
- `gemini-1.5-pro`
- `gemini-1.5-flash`

### 智谱 GLM 系列（全部不支持）

- `glm-4-plus`
- `glm-4-air`
- `glm-4-airx`
- `glm-4v`

### 其他（不支持）

- `kimi-k2.5-search`
- `kimi-k1.5`
- `doubao-pro-32k`
- `doubao-pro-128k`
- `MiniMax-M2`
- `MiniMax-M3`
- `ernie-4.5-turbo`
- `ernie-4.0`

---

## 快速测试命令

```bash
# 测试单个模型
curl -s "https://aigw.netease.com/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_APP_ID.YOUR_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-opus-4-6","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

---

## 推荐模型选择

| 场景 | 推荐模型 |
|------|----------|
| 最强推理 | `claude-opus-4-6` |
| 日常对话 | `claude-sonnet-4-20250514` |
| 快速响应 | `claude-haiku-4-5-20251001` |
| 超大上下文 | `gemini-3-flash` (1M) |
| 成本敏感 | `deepseek-chat` |
| 中文优化 | `qwen-max` |
| 长文档 | `kimi-k2.5` |
