# NetEase AI Gateway API 规范

## 基础信息

- **Base URL**：`https://aigw-int.netease.com`
- **认证方式**：Bearer Token（APP_ID.APP_KEY）
- **Content-Type**：`application/json`

## 认证

### 获取凭证

从 NetEase 内部系统获取：
- APP_ID：`a3qanjtg0juk4juz`
- APP_KEY：`68ip3dor15ojfusqph4z5nz907q5l2zr`

### 请求头格式

```
Authorization: Bearer {app_id}.{app_key}
Content-Type: application/json
```

## 端点

### POST /v1/chat/completions

发送聊天请求到 AI 模型。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 模型名称 |
| messages | array | 是 | 消息列表 |
| max_tokens | integer | 否 | 最大生成 token 数（默认：1000） |
| temperature | float | 否 | 温度参数，范围 0.0-1.0（默认：0.7） |
| stream | boolean | 否 | 是否流式输出（默认：false） |

#### messages 格式

```json
[
  {
    "role": "user",
    "content": "用户输入内容"
  }
]
```

#### 支持的模型

| 模型名称 | 说明 |
|---------|------|
| claude-oplus-4-6 | Claude Plus 模型 |
| claude-opus-4-6 | Claude Opus 高级模型 |
| gpt-5.2-codex-2026-01-14 | GPT 代码生成模型 |
| gpt-4.5-2024-01-27 | GPT-4.5 模型 |

#### 请求示例

```bash
curl -X POST "https://aigw-int.netease.com/v1/chat/completions" \
  -H "Authorization: Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-oplus-4-6",
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "max_tokens": 1000,
    "stream": false
  }'
```

#### 响应示例

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "claude-oplus-4-6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是 AI 助手，很高兴为您服务。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

#### 流式响应示例

当 `stream=true` 时，响应以 SSE 格式返回：

```
data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":"你"},"index":0}]}

data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":"好"},"index":0}]}

data: [DONE]
```

## 错误码

| HTTP 状态码 | 说明 |
|-----------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

### 错误响应示例

```json
{
  "error": {
    "message": "Invalid authentication",
    "type": "invalid_request_error",
    "code": "invalid_api_key"
  }
}
```

## 限制

- **Token 有效期**：24 小时
- **请求频率**：根据账号配置
- **最大并发数**：根据账号配置

## 最佳实践

### 1. 合理设置 max_tokens

```python
# 简单问答：200-500 tokens
max_tokens = 300

# 代码生成：500-1000 tokens
max_tokens = 800

# 长文本生成：1000-2000 tokens
max_tokens = 1500
```

### 2. 温度参数选择

```python
# 确定性输出（代码、事实）
temperature = 0.2

# 平衡对话
temperature = 0.7

# 创意写作
temperature = 0.9
```

### 3. 流式输出

对于长文本，使用流式输出获得更好体验：

```python
for chunk in client.chat_stream(...):
    print(chunk, end='', flush=True)
```

### 4. 错误处理

```python
try:
    response = client.chat(...)
except Exception as e:
    print(f"调用失败：{e}")
    # 重试逻辑或降级处理
```

## Python 完整示例

```python
import requests

def call_netease_aigw(prompt, model="claude-oplus-4-6"):
    url = "https://aigw-int.netease.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data, timeout=60)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 调用失败：{response.status_code}")

# 使用
result = call_netease_aigw("你好")
print(result["choices"][0]["message"]["content"])
```

## 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 响应 ID |
| object | string | 对象类型（chat.completion） |
| created | integer | 创建时间戳 |
| model | string | 实际使用的模型 |
| choices | array | 生成结果数组 |
| usage | object | Token 使用统计 |

### usage 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| prompt_tokens | integer | 提示词 token 数 |
| completion_tokens | integer | 生成内容 token 数 |
| total_tokens | integer | 总 token 数 |
