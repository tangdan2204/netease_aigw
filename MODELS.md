# 网易 AIGW 完整模型列表

> **最后更新**: 2025年2月13日  
> **数据来源**: https://modelspace.netease.com/model_app

---

## 目录

1. [已抓取详细信息的模型](#已抓取详细信息的模型)
2. [所有可用模型列表](#所有可用模型列表)
3. [模型按开发方分类](#模型按开发方分类)
4. [API 使用模板](#api-使用模板)
5. [OpenCode 配置](#opencode-配置)

---

## 已抓取详细信息的模型

### 1. GLM-5（智谱）

**基本信息**
- 模型代号: `glm-5`
- 开发方: 智谱（zhipu）
- 类型: 语言模型
- 阶段: 测试阶段
- 特性: 思维链

**技术规格**
- 上下文窗口: 200K Tokens
- 最大输出长度: 128K Tokens
- 支持格式: openai.chat

**限流配置**
- 总 RPM 限制: 600
- 总 TPM 限制: 3M
- 默认 RPM: 60（最大可调整至 120）
- 默认 TPM: 500K（最大可调整至 1M）

**定价**
- 推理输入: ¥6.000 / 百万tokens
- 推理输出: ¥22.000 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "glm-5",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

**官方文档**: https://docs.bigmodel.cn/cn/guide/models/text/glm-5

---

### 2. Claude Opus 4.6（Anthropic）

**基本信息**
- 模型代号: `claude-opus-4-6`
- 开发方: Anthropic
- 类型: 语言模型、多模态
- 阶段: 测试阶段
- 特性: 工具调用、识别图片、混合推理

**技术规格**
- 上下文窗口: 200K Tokens（启用 beta 头部可达 1M）
- 最大输入长度: 200K Tokens（启用 beta 头部可达 1M）
- 最大输出长度: 128K Tokens
- 功能: text, image, code, reasoning
- 支持格式: openai.chat, atrp.messages

**限流配置**
- 总 RPM 限制: 9K
- 总 TPM 限制: 24M
- 默认 RPM: 120（最大可调整至 300）
- 默认 TPM: 1M（最大可调整至 2M）

**定价**
- 推理输入: ¥72.000 / 百万tokens
- 推理输出: ¥270.000 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "claude-opus-4-6",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

---

### 3. Kimi K2.5（月之暗面）

**基本信息**
- 模型代号: `kimi-k2.5`
- 开发方: 月之暗面
- 类型: 语言模型
- 阶段: 准生产阶段
- 特性: 工具调用、识别图片、混合推理、视频理解

**技术规格**
- 上下文窗口: 262K Tokens
- 最大输出长度: 32K Tokens
- 功能: text, code, reasoning
- 支持格式: openai.chat, atrp.messages

**限流配置**
- 总 RPM 限制: 10K
- 总 TPM 限制: 5M
- 默认 RPM: 120（最大可调整至 480）
- 默认 TPM: 480K（最大可调整至 800K）

**定价**
- 推理输入: ¥4.000 / 百万tokens
- 推理输出: ¥21.000 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

---

## 所有可用模型列表

> **总模型数**: 236 项（共 12 页）
> **数据更新时间**: 2025-02-12

### 语言模型（部分）

| 模型名称 | 开发方 | 上下文 | 输出 | 阶段 | 特性 |
|---------|--------|--------|------|------|------|
| glm-5 | 智谱 | 200K | 128K | 测试阶段 | 思维链 |
| claude-opus-4-6 | Anthropic | 200K | 128K | 测试阶段 | 工具调用、识别图片、混合推理 |
| kimi-k2.5 | 月之暗面 | 262K | 32K | 准生产阶段 | 工具调用、识别图片、混合推理、视频理解 |
| qwen3-max-2026-01-23 | 阿里 | - | - | - | 工具调用、思维链 |
| gpt-5.2-codex-2026-01-14 | OpenAI | - | - | 测试阶段 | 识别图片、工具调用、PDF读取 |
| doubao-seed-1.8 | 字节跳动 | - | - | 测试阶段 | 工具调用、图片识别、视频理解 |
| gemini-3-flash | Google | - | - | 测试阶段 | 思维链、识别图片、视频理解、PDF读取 |
| glm-4.7 | 智谱 | - | - | 测试阶段 | 思维链 |
| gpt-5.2-2025-12-11 | OpenAI | - | - | 测试阶段 | 识别图片、工具调用、PDF读取 |
| gpt-5.1-codex-max-2025-12-04 | OpenAI | - | - | 测试阶段 | 识别图片、工具调用、PDF读取 |
| gpt-5.2-chat-2025-12-11 | OpenAI | - | - | 测试阶段 | 识别图片、工具调用、PDF读取 |

### 视频生成模型

| 模型名称 | 开发方 | 阶段 | 特性 |
|---------|--------|------|------|
| kling-motion-control | 快手 | 稳定生产阶段 | 动作控制 |
| kling-v2-6 | 快手 | 稳定生产阶段 | 音画同出 |
| kling-custom-voices | 快手 | 稳定生产阶段 | 音色定制 |
| kling-video-o1 | 快手 | 稳定生产阶段 | 视频生成 |

### DeepSeek 系列

| 模型名称 | 上下文 | 特性 |
|---------|--------|------|
| deepseek-v3.2-think-bd-251201 | - | 工具调用、联网搜索、思维链 |
| deepseek-v3.2-bd-latest | - | 工具调用、联网搜索 |
| deepseek-v3.2-bd-251201 | - | 工具调用、联网搜索 |
| deepseek-v3.2-think-bd-latest | - | 工具调用、联网搜索、思维链 |

---

## 模型按开发方分类

### Anthropic（Claude 系列）
- claude-opus-4-6
- claude-sonnet-4-6
- claude-haiku-4-6
- claude-3-sonnet
- claude-3-haiku
- （更多 Claude 变体）

### OpenAI（GPT 系列）
- gpt-5.2-codex-2026-01-14
- gpt-5.2-2025-12-11
- gpt-5.1-codex-max-2025-12-04
- gpt-5.2-chat-2025-12-11
- gpt-4.1 系列
- gpt-4o 系列
- gpt-3.5-turbo
- （更多 GPT 变体）

### Google（Gemini 系列）
- gemini-3-flash
- gemini-2.5-pro
- gemini-2.5-flash
- gemini-2.0-flash
- gemini-1.5-pro
- gemini-1.5-flash
- Veo 2.0（视频生成）

### 阿里（Qwen 系列）
- qwen3-max-2026-01-23
- qwen-plus-character
- qwen2-系列（0.5B~7B）
- qwen2.5-系列（0.5B~72B）
- qwen2.5-coder
- qwen2-vl-系列
- qwen-max
- qwen-plus
- qwen-turbo

### 智谱（GLM 系列）
- glm-5
- glm-4.7
- glm-4-plus
- glm-4-air
- glm-4-airx
- glm-4v
- glm-3-turbo

### DeepSeek
- deepseek-v3.2-think-bd-251201
- deepseek-v3.2-bd-latest
- deepseek-v3.2-bd-251201
- deepseek-v3.2-think-bd-latest
- deepseek-chat
- deepseek-reasoner
- Janus 系列

### 月之暗面（Kimi 系列）
- kimi-k2.5
- kimi-k2.5-search
- kimi-k1.5

### 字节跳动（Doubao 系列）
- doubao-seed-1.8
- doubao-pro-32k
- doubao-pro-128k
- doubao-1.5-系列

### 快手（可灵系列）
- kling-v2-6
- kling-motion-control
- kling-custom-voices
- kling-video-o1

### 其他开发方
- MiniMax（M1、M2、M3 系列）
- ERNIE（百度）
- Moonshot
- 阶跃星辰

---

## API 使用模板

### 通用 API 认证

```http
Authorization: Bearer {app_id}.{app_key}
```

### 基础调用模板

#### Python
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "your-model-id",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Your message here"}
    ],
    "max_tokens": 1000,
    "temperature": 0.7,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

#### cURL
```bash
curl "https://aigw-int.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {app_id}.{app_key}" \
  -d '{
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "Your message here"}],
    "max_tokens": 1000
  }'
```

#### JavaScript
```javascript
const response = await fetch('https://aigw-int.netease.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {app_id}.{app_key}'
  },
  body: JSON.stringify({
    model: 'your-model-id',
    messages: [{role: 'user', content: 'Your message here'}],
    max_tokens: 1000
  })
});

const result = await response.json();
console.log(result.choices[0].message.content);
```

### 流式输出模板

#### Python
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "Tell me a story"}],
    "stream": True
}

response = requests.post(url, headers=headers, json=data, stream=True)

for line in response.iter_lines():
    if line:
        chunk = line.decode('utf-8')
        print(chunk, flush=True)
```

### 函数调用模板

#### Python
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    }
]

data = {
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "What's the weather in Beijing?"}],
    "tools": tools
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["tool_calls"])
```

---

## OpenCode 配置

### 完整配置模板

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
        "glm-5": {
          "name": "GLM-5 (智谱)",
          "description": "智谱新一代旗舰基座模型",
          "limit": {"context": 200000, "output": 128000}
        },
        "claude-opus-4-6": {
          "name": "Claude Opus 4.6 (Anthropic)",
          "description": "Anthropic 最智能的编码和企业代理模型",
          "limit": {"context": 200000, "output": 128000}
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5 (月之暗面)",
          "description": "Kimi 迄今最智能的模型",
          "limit": {"context": 262000, "output": 32000}
        },
        "qwen3-max-2026-01-23": {
          "name": "Qwen3-Max (阿里)",
          "description": "通义千问3系列Max模型",
          "limit": {"context": 128000, "output": 8000}
        },
        "gpt-5.2-codex--14": {
2026-01          "name": "GPT-5.2-Codex (OpenAI)",
          "description": "OpenAI 代理编码优化模型",
          "limit": {"context": 128000, "output": 16384}
        },
        "doubao-seed-1.8": {
          "name": "Doubao Seed 1.8 (字节)",
          "description": "更强Agent能力、升级多模态理解",
          "limit": {"context": 128000, "output": 4096}
        },
        "gemini-3-flash": {
          "name": "Gemini 3 Flash (Google)",
          "description": "Google 高效多模态代理工作流",
          "limit": {"context": 1000000, "output": 65536}
        },
        "deepseek-v3.2-think-bd-251201": {
          "name": "DeepSeek V3.2 Think (百度)",
          "description": "DeepSeek V3.2 正式版，平衡推理能力",
          "limit": {"context": 128000, "output": 65536}
        }
      }
    }
  }
}
```

### 配置说明

1. **baseURL**: 使用生产环境 `https://aigw.netease.com/v1`
2. **headers**: 认证格式 `Authorization: Bearer {app_id}.{app_key}`
3. **模型选择**: 在 OpenCode 中选择对应的模型名称即可使用

---

## 快速参考

### 常用模型速查表

| 场景 | 推荐模型 | 模型ID | 开发方 | 特点 |
|------|---------|--------|--------|------|
| 日常对话 | Claude Sonnet | claude-sonnet-4-6 | Anthropic | 平衡性能与速度 |
| 复杂推理 | Claude Opus | claude-opus-4-6 | Anthropic | 最强推理能力 |
| 编程任务 | GPT-5.2-Codex | gpt-5.2-codex-2026-01-14 | OpenAI | 代理编码优化 |
| 中文优化 | Qwen-Max | qwen3-max-2026-01-23 | 阿里 | 中文理解能力强 |
| 低成本 | Kimi K2.5 | kimi-k2.5 | 月之暗面 | 高性价比 |
| 多模态 | Gemini 3 Flash | gemini-3-flash | Google | 支持图像、视频 |
| 通用智能 | GLM-5 | glm-5 | 智谱 | Agentic Engineering |

### 价格对比（输入价格，单位：¥/百万tokens）

| 模型 | 输入价格 | 输出价格 | 相对成本 |
|------|---------|---------|---------|
| Kimi K2.5 | ¥4 | ¥21 | 最低 |
| GLM-5 | ¥6 | ¥22 | 低 |
| Claude Opus 4.6 | ¥72 | ¥270 | 高 |
| GPT-5.2-Codex | 约 ¥30 | 约 ¥100 | 中高 |

---

## 相关资源

### 官方资源
- **模型广场**: https://modelspace.netease.com/model_app
- **API 文档**: https://aigw.doc.nie.netease.com
- **控制台**: https://aigw.console.nie.netease.com

### 认证相关
- **APP 账号申请**: https://aigw.doc.nie.netease.com/13_账号申请/13_账号申请.html
- **认证说明**: https://aigw.doc.nie.netease.com/21_开发指南/11_身份认证/2_身份认证.html

### SDK 文档
- **Python SDK**: https://github.com/openai/openai-python
- **JavaScript SDK**: https://github.com/openai/openai-node
- **OpenAI 兼容性**: 所有 SDK 均支持

---

## 注意事项

1. **认证信息**: 示例代码使用 `{app_id}.{app_key}` 格式，请替换为你的实际凭证
2. **环境选择**: 
   - 测试环境: `https://aigw-int.netease.com/v1`
   - 生产环境: `https://aigw.netease.com/v1`
3. **限流调整**: 默认限流可在控制台中调整
4. **模型更新**: 模型会定期更新，请关注官方公告
5. **价格变动**: 价格可能随时调整，请以控制台显示为准

---

**文档维护**: 建议定期检查 ModelSpace 获取最新模型信息  
**版本**: 1.0.0  
**创建时间**: 2025年2月13日
