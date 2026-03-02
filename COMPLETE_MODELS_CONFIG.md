# 网易 AIGW 完整模型配置指南

> **文档版本**: 2.0  
> **创建时间**: 2025年2月13日  
> **数据来源**: https://modelspace.netease.com/model_app  
> **抓取模型数**: 8 个代表性模型（完整列表 236 项）

---

## 目录

1. [快速开始](#快速开始)
2. [已抓取模型详细信息](#已抓取模型详细信息)
3. [所有可用模型列表](#所有可用模型列表)
4. [API 使用模板](#api-使用模板)
5. [OpenCode 完整配置](#opencode-完整配置)
6. [如何更新模型信息](#如何更新模型信息)

---

## 快速开始

### 获取凭证

1. 访问 https://modelspace.netease.com/model_app
2. 登录网易账号
3. 创建项目获取 APP_ID 和 APP_KEY

### 基础调用

```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

---

## 已抓取模型详细信息

### 1. Claude Opus 4.6（Anthropic）

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

url = "https://aigw.netease.com/v1/chat/completions"
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

### 2. GPT-5.2-Codex（OpenAI）

**基本信息**
- 模型代号: `gpt-5.2-codex-2026-01-14`
- 开发方: OpenAI
- 阶段: 测试阶段
- 特性: 识别图片、工具调用、PDF读取

**技术规格**
- 上下文窗口: 400K Tokens
- 最大输入长度: 400K Tokens
- 最大输出长度: 128K Tokens
- 功能: text, image, code, reasoning
- 支持格式: openai.chat

**限流配置**
- 总 RPM 限制: 200K
- 总 TPM 限制: 20M
- 默认 RPM: 600（最大可调整至 30K）
- 默认 TPM: 800K（最大可调整至 8M）

**定价**
- 推理输入: ¥12.600 / 百万tokens
- 推理输出: ¥100.800 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5.2-codex-2026-01-14",
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

url = "https://aigw.netease.com/v1/chat/completions"
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

### 4. Qwen3-Max（阿里）

**基本信息**
- 模型代号: `qwen3-max-2026-01-23`
- 开发方: 阿里
- 特性: 工具调用、思维链
- 支持格式: openai.chat

**限流配置**
- 总 RPM 限制: 600
- 总 TPM 限制: 1M
- 默认 RPM: 120（最大可调整至 240）
- 默认 TPM: 300K（最大可调整至 500K）

**定价**
- 推理输入: ¥7.000 / 百万tokens
- 推理输出: ¥28.000 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "qwen3-max-2026-01-23",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

---

### 5. GLM-5（智谱）

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

url = "https://aigw.netease.com/v1/chat/completions"
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

---

### 6. DeepSeek V3.2 Think（DeepSeek）

**基本信息**
- 模型代号: `deepseek-v3.2-think-bd-251201`
- 开发方: DeepSeek
- 特性: 工具调用、联网搜索、思维链

**技术规格**
- 上下文窗口: 128K Tokens
- 最大输入长度: 96K Tokens
- 最大输出长度: 32K Tokens
- 功能: text, code, reasoning
- 支持格式: openai.chat

**限流配置**
- 总 RPM 限制: 60
- 总 TPM 限制: 150K
- 默认 RPM: 10（最大可调整至 30）
- 默认 TPM: 80K（最大可调整至 100K）

**定价**
- 推理输入: ¥0.700 / 百万tokens
- 推理输出: ¥1.050 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-v3.2-think-bd-251201",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

---

### 7. Doubao-seed-1.8（字节跳动）

**基本信息**
- 模型代号: `doubao-seed-1.8`
- 开发方: 字节跳动
- 特性: 更强Agent能力、升级多模态理解、更灵活的上下文管理

**技术规格**
- 上下文窗口: 256K Tokens
- 最大输入长度: 256K Tokens
- 最大输出长度: 64K Tokens
- 特性: 工具调用、图片识别、视频理解
- 功能: text, reasoning, code
- 支持格式: openai.chat

**限流配置**
- 总 RPM 限制: 30K
- 总 TPM 限制: 5M
- 默认 RPM: 300（最大可调整至 6K）
- 默认 TPM: 500K（最大可调整至 3M）

**定价**
- 推理输入: ¥2.400 / 百万tokens
- 推理输出: ¥24.000 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "doubao-seed-1.8",
    "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

---

### 8. Gemini-3-flash（Google）

**基本信息**
- 模型代号: `gemini-3-flash`
- 开发方: Google
- 上下文窗口: 1048K Tokens
- 最大输入长度: 1048K Tokens
- 最大输出长度: 66K Tokens
- 特性: 思维链、识别图片、视频理解、PDF读取
- 功能: text, image, video
- 支持格式: openai.chat

**限流配置**
- 总 RPM 限制: 6K
- 总 TPM 限制: 3M
- 默认 RPM: 300（最大可调整至 1K）
- 默认 TPM: 600K（最大可调整至 2M）

**定价**
- 推理输入: ¥3.600 / 百万tokens
- 推理输出: ¥21.600 / 百万tokens

**Python 示例**
```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gemini-3-flash",
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
> **更新时间**: 2025-02-12

### 按开发方分类

#### Anthropic（Claude 系列）
- claude-opus-4-6 ✅ 已抓取
- claude-sonnet-4-6
- claude-haiku-4-6
- claude-3-sonnet
- claude-3-haiku

#### OpenAI（GPT 系列）
- gpt-5.2-codex-2026-01-14 ✅ 已抓取
- gpt-5.2-2025-12-11
- gpt-5.1-codex-max-2025-12-04
- gpt-4.1 系列
- gpt-4o 系列

#### Google（Gemini 系列）
- gemini-3-flash ✅ 已抓取
- gemini-2.5-pro
- gemini-2.5-flash
- gemini-2.0-flash
- gemini-1.5-pro
- Veo 2.0（视频生成）

#### 阿里（Qwen 系列）
- qwen3-max-2026-01-23 ✅ 已抓取
- qwen-plus-character
- qwen2-系列（0.5B~7B）
- qwen2.5-系列（0.5B~72B）
- qwen-max
- qwen-plus
- qwen-turbo

#### 智谱（GLM 系列）
- glm-5 ✅ 已抓取
- glm-4.7
- glm-4-plus
- glm-4-air
- glm-4-airx

#### DeepSeek
- deepseek-v3.2-think-bd-251201 ✅ 已抓取
- deepseek-v3.2-bd-latest
- deepseek-chat
- deepseek-reasoner

#### 月之暗面（Kimi 系列）
- kimi-k2.5 ✅ 已抓取
- kimi-k2.5-search
- kimi-k1.5

#### 字节跳动（Doubao 系列）
- doubao-seed-1.8 ✅ 已抓取
- doubao-pro-32k
- doubao-pro-128k

#### 快手（可灵系列）
- kling-v2-6
- kling-motion-control
- kling-video-o1

#### MiniMax
- MiniMax-M1
- MiniMax-M2
- MiniMax-M3

#### 其他
- ERNIE（百度）
- Moonshot
- 阶跃星辰

---

## API 使用模板

### 通用认证

```http
Authorization: Bearer {app_id}.{app_key}
```

### Python SDK

```python
import requests

url = "https://aigw.netease.com/v1/chat/completions"
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

### cURL

```bash
curl "https://aigw.netease.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {app_id}.{app_key}" \
  -d '{
    "model": "your-model-id",
    "messages": [{"role": "user", "content": "Your message here"}],
    "max_tokens": 1000
  }'
```

### JavaScript

```javascript
const response = await fetch('https://aigw.netease.com/v1/chat/completions', {
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

---

## OpenCode 完整配置

### 配置文件位置

**macOS/Linux：**
```bash
~/.config/opencode/opencode.json
```

### 完整配置

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
          "name": "Claude Opus 4.6 (Anthropic)",
          "description": "Anthropic 最智能的编码和企业代理模型",
          "limit": {"context": 200000, "output": 128000}
        },
        "gpt-5.2-codex-2026-01-14": {
          "name": "GPT-5.2-Codex (OpenAI)",
          "description": "OpenAI 代理编码优化模型",
          "limit": {"context": 400000, "output": 128000}
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
        "glm-5": {
          "name": "GLM-5 (智谱)",
          "description": "智谱新一代旗舰基座模型",
          "limit": {"context": 200000, "output": 128000}
        },
        "deepseek-v3.2-think-bd-251201": {
          "name": "DeepSeek V3.2 Think (DeepSeek)",
          "description": "DeepSeek V3.2 正式版，平衡推理能力",
          "limit": {"context": 128000, "output": 32000}
        },
        "doubao-seed-1.8": {
          "name": "Doubao Seed 1.8 (字节)",
          "description": "更强Agent能力、升级多模态理解",
          "limit": {"context": 256000, "output": 64000}
        },
        "gemini-3-flash": {
          "name": "Gemini 3 Flash (Google)",
          "description": "Google 高效多模态代理工作流",
          "limit": {"context": 1048000, "output": 66000}
        }
      }
    }
  }
}
```

---

## 如何更新模型信息

### 方法 1：手动更新（推荐）

1. **访问 ModelSpace**
   ```
   https://modelspace.netease.com/model_app
   ```

2. **浏览模型列表**
   - 共 236 个模型，12 页
   - 每页显示 20 个模型

3. **点击感兴趣的模型**
   - 查看模型详情
   - 获取 API 使用示例

4. **复制示例代码**
   - Python、cURL、JavaScript
   - 直接使用

5. **更新配置文件**
   - 复制示例到你的项目
   - 替换 `{app_id}.{app_key}`

### 方法 2：批量获取所有模型

1. **使用浏览器开发者工具**
   ```
   F12 -> Network -> XHR
   ```

2. **查找 API 接口**
   - 寻找 models.json 或类似接口
   - 获取所有模型的 JSON 数据

3. **解析数据**
   ```bash
   curl "https://modelspace.netease.com/api/models" > models.json
   ```

4. **生成配置文件**
   - 使用脚本解析 JSON
   - 自动生成 OpenCode 配置

### 方法 3：定期检查更新

1. **订阅官方公告**
   - ModelSpace 更新日志
   - 新模型发布通知

2. **检查新模型**
   - 每月访问一次 ModelSpace
   - 查看新增模型

3. **更新本文档**
   - 复制新模型信息
   - 更新定价和限流

### 关键页面链接

- **模型市场**: https://modelspace.netease.com/model_app
- **API 文档**: https://aigw.doc.nie.netease.com
- **控制台**: https://aigw.console.nie.netease.com

---

## 常用模型速查表

| 场景 | 推荐模型 | 模型ID | 开发方 | 特点 | 输入价格 |
|------|---------|--------|--------|------|---------|
| 复杂推理 | Claude Opus | claude-opus-4-6 | Anthropic | 最强推理 | ¥72/百万 |
| 编程任务 | GPT-5.2-Codex | gpt-5.2-codex-2026-01-14 | OpenAI | 代理编码 | ¥12.6/百万 |
| 中文优化 | Qwen3-Max | qwen3-max-2026-01-23 | 阿里 | 中文理解强 | ¥7/百万 |
| 低成本 | Kimi K2.5 | kimi-k2.5 | 月之暗面 | 高性价比 | ¥4/百万 |
| 多模态 | Gemini 3 Flash | gemini-3-flash | Google | 超大上下文 | ¥3.6/百万 |
| 超低成本 | DeepSeek | deepseek-v3.2-think-bd-251201 | DeepSeek | 最低价格 | ¥0.7/百万 |

---

## 相关资源

### 官方资源
- **模型市场**: https://modelspace.netease.com/model_app
- **API 文档**: https://aigw.doc.nie.netease.com
- **控制台**: https://aigw.console.nie.netease.com

### SDK 资源
- **Python SDK**: https://github.com/openai/openai-python
- **JavaScript SDK**: https://github.com/openai/openai-node
- **OpenAI 兼容性**: 所有 SDK 均支持

---

## 更新日志

### 2025-02-13（版本 2.0）
- ✅ 新增 8 个代表性模型的详细信息
- ✅ 新增完整 API 使用示例
- ✅ 新增 OpenCode 完整配置模板
- ✅ 新增"如何更新模型信息"章节
- ✅ 新增常用模型速查表

### 2025-02-13（版本 1.0）
- ✅ 初始版本
- ✅ 基础配置指南

---

**文档维护**: 建议每月检查 ModelSpace 获取最新模型信息  
**版本**: 2.0.0  
**创建时间**: 2025年2月13日  
**最后更新**: 2025年2月13日
