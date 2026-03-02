# NetEase AIGW

NetEase AI Gateway API 调用技能——在 OpenCode 中使用网易 AI 大模型。

## 描述

提供便捷的 NetEase AI Gateway API 调用接口，支持多种 AI 模型（包括 Claude、GPT 等）。该技能封装了认证、请求和响应处理，让你在 OpenCode 中直接使用网易的 AI 模型进行对话、代码生成、问题解答等任务。

## 使用场景

- **代码生成**：根据需求生成代码片段、函数、类
- **代码审查**：分析代码质量、提供建议
- **问题解答**：技术问题咨询、概念解释
- **文档生成**：自动生成代码注释、README、API 文档
- **重构建议**：代码优化建议、重构方案

## 配置

在使用前，需要设置环境变量或在代码中配置认证信息：

```python
APP_ID = "a3qanjtg0juk4juz"
APP_KEY = "68ip3dor15ojfusqph4z5nz907q5l2zr"
AUTHORIZATION = f"Bearer {APP_ID}.{APP_KEY}"
```

## 支持的模型

- `claude-opus-4-6`——Claude 模型
- `gpt-5.2-codex-2026-01-14`——GPT 代码模型
- `claude-opus-4-6`——Claude 高级模型
- 以及更多支持的模型……

## 使用方法

### 基础用法

```python
import requests

# 配置
url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr",
    "Content-Type": "application/json"
}

# 请求
data = {
    "model": "claude-opus-4-6",
    "messages": [
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### 使用提供的脚本

```python
from scripts.netease_aigw_client import NetEaseAIGWClient

# 初始化客户端
client = NetEaseAIGWClient(
    app_id="a3qanjtg0juk4juz",
    app_key="68ip3dor15ojfusqph4z5nz907q5l2zr"
)

# 简单对话
response = client.chat(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "帮我写一个 Python 排序算法"}],
    max_tokens=1000
)

print(response["choices"][0]["message"]["content"])

# 代码生成
code_response = client.chat(
    model="gpt-5.2-codex-2026-01-14",
    messages=[{"role": "user", "content": "写一个快速排序函数"}],
    max_tokens=500
)
```

### 代码审查示例

```python
code = '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
'''

response = client.chat(
    model="claude-opus-4-6",
    messages=[{
        "role": "user",
        "content": f"请审查以下代码，指出潜在问题和改进建议：\n\n{code}"
    }],
    max_tokens=1000
)

print(response["choices"][0]["message"]["content"])
```

## API 参考

### `NetEaseAIGWClient` 类

#### 构造函数

```python
NetEaseAIGWClient(app_id: str, app_key: str, base_url: str = "https://aigw.netease.com")
```

**参数说明：**
- `app_id`：网易 AIGW 的 App ID
- `app_key`：网易 AIGW 的 App Key
- `base_url`：API 基础 URL（默认为内部网关）

#### 方法

##### `chat(model, messages, max_tokens=1000, stream=False, temperature=0.7, **kwargs)`

发送聊天请求到 AI 模型。

**参数说明：**
- `model`：模型名称（如 "claude-opus-4-6"）
- `messages`：消息列表，格式为 `[{"role": "user", "content": "..."}]`
- `max_tokens`：最大生成 token 数
- `stream`：是否使用流式响应
- `temperature`：温度参数（0.0-1.0，控制随机性）

**返回值：**
- `dict`：API 响应数据

**异常：**
- `Exception`：当请求失败时抛出异常

##### `chat_stream(model, messages, max_tokens=1000, temperature=0.7, **kwargs)`

发送流式聊天请求，实时接收响应。

**参数说明：**
- 同 `chat()` 方法，但 `stream` 参数自动设置为 `True`

**返回值：**
- `Generator`：逐个 yield 响应片段

## 错误处理

```python
try:
    response = client.chat(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": "测试"}]
    )
except Exception as e:
    print(f"调用失败：{e}")
```

## 最佳实践

1. **设置合适的 max_tokens**：根据需要调整，避免浪费 token
2. **使用 stream 模式**：对于长文本，使用流式响应获得更好体验
3. **合理设置 temperature**：
   - 0.0-0.3：更确定性的输出（代码、事实）
   - 0.4-0.7：平衡（一般对话）
   - 0.8-1.0：更创造性（创意写作）
4. **缓存常用响应**：避免重复调用相同请求

## 故障排除

### 连接失败
- 检查网络连接
- 确认 API URL 正确
- 检查防火墙设置

### 认证失败
- 验证 APP_ID 和 APP_KEY 正确
- 检查 Authorization header 格式
- 确认账号权限正常

### 响应超时
- 增加 timeout 参数
- 检查请求内容长度
- 简化提示词

## 注意事项

- API 凭证已硬编码在示例中，**生产环境请使用环境变量**
- Token 有效期为 24 小时，过期需要重新获取
- 遵守 API 使用规范，避免频繁调用

## 参考资源

- [NetEase AI Gateway 文档](https://console-auth.nie.netease.com/)
- [API 参考](references/api-spec.md)
- [使用示例](examples.py)
