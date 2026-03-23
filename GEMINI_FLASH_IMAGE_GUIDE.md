# Gemini 3.1 Flash Image 调用指南

## 模型信息

| 项目 | 值 |
|------|-----|
| **模型名称** | `gemini-3.1-flash-image` |
| **模型页面** | https://modelspace.netease.com/model_app/detail/gemini-3.1-flash-image |
| **能力** | 文本生成 + 图像生成（多模态输出） |
| **支持推理链** | 是（返回 `reasoning_content`） |

---

## 认证配置

```
App ID:   p4x4nxxigw2ccja7
App Key:  7vfnst67x7dcmghii83cw47uovjqpmrx
App Code: _td_aigwcoding

Authorization Header:
Bearer p4x4nxxigw2ccja7.7vfnst67x7dcmghii83cw47uovjqpmrx
```

---

## 关键参数

> **必须**在请求体中包含 `vertexai.response_modalities`，否则返回 400 错误。

```json
"vertexai": {
  "response_modalities": ["IMAGE", "TEXT"]
}
```

| `response_modalities` 值 | 说明 |
|--------------------------|------|
| `["TEXT"]` | 仅返回文本（不可单独使用，此模型强制要求包含 IMAGE） |
| `["IMAGE", "TEXT"]` | 返回文本 + 图像（**推荐，也是唯一可用的配置**） |

---

## 调用方式

### 1. cURL

```bash
curl -X POST "https://aigw.netease.com/v1/chat/completions" \
  -H "Authorization: Bearer p4x4nxxigw2ccja7.7vfnst67x7dcmghii83cw47uovjqpmrx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.1-flash-image",
    "messages": [
      {"role": "user", "content": "用一句话介绍自己"}
    ],
    "max_tokens": 200,
    "temperature": 0.7,
    "vertexai": {
      "response_modalities": ["IMAGE", "TEXT"]
    }
  }'
```

### 2. Python (requests)

```python
import requests
import json

API_URL = "https://aigw.netease.com/v1/chat/completions"
AUTH_TOKEN = "Bearer p4x4nxxigw2ccja7.7vfnst67x7dcmghii83cw47uovjqpmrx"

def chat(prompt: str, max_tokens: int = 200) -> dict:
    """调用 gemini-3.1-flash-image 模型"""
    response = requests.post(
        API_URL,
        headers={
            "Authorization": AUTH_TOKEN,
            "Content-Type": "application/json",
        },
        json={
            "model": "gemini-3.1-flash-image",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "vertexai": {
                "response_modalities": ["IMAGE", "TEXT"],
            },
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


# --- 使用示例 ---
if __name__ == "__main__":
    result = chat("你好，请用一个词回复确认你在工作")
    message = result["choices"][0]["message"]

    print("回复:", message["content"])

    # 如果有推理过程
    if "reasoning_content" in message:
        print("推理过程:", message["reasoning_content"][:200], "...")

    # Token 用量
    usage = result["usage"]
    print(f"Token: prompt={usage['prompt_tokens']}, "
          f"completion={usage['completion_tokens']}, "
          f"total={usage['total_tokens']}")
```

### 3. Python (OpenAI SDK 兼容)

```python
from openai import OpenAI

client = OpenAI(
    api_key="p4x4nxxigw2ccja7.7vfnst67x7dcmghii83cw47uovjqpmrx",
    base_url="https://aigw.netease.com/v1",
)

response = client.chat.completions.create(
    model="gemini-3.1-flash-image",
    messages=[{"role": "user", "content": "你好"}],
    max_tokens=200,
    temperature=0.7,
    extra_body={
        "vertexai": {
            "response_modalities": ["IMAGE", "TEXT"],
        }
    },
)

print(response.choices[0].message.content)
```

### 4. 图像生成示例

```python
import requests
import base64

API_URL = "https://aigw.netease.com/v1/chat/completions"
AUTH_TOKEN = "Bearer p4x4nxxigw2ccja7.7vfnst67x7dcmghii83cw47uovjqpmrx"

def generate_image(prompt: str, output_path: str = "output.png") -> str:
    """使用 gemini-3.1-flash-image 生成图像"""
    response = requests.post(
        API_URL,
        headers={
            "Authorization": AUTH_TOKEN,
            "Content-Type": "application/json",
        },
        json={
            "model": "gemini-3.1-flash-image",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.7,
            "vertexai": {
                "response_modalities": ["IMAGE", "TEXT"],
            },
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    message = data["choices"][0]["message"]

    # 检查是否返回了图像内容（base64 编码）
    content = message.get("content", "")

    # 如果内容中包含 base64 图像数据，解码并保存
    # 具体格式取决于 AIGW 返回结构，可能在 content 或 parts 中
    print("文本回复:", content[:500])
    print(f"Token 用量: {data['usage']}")

    return content


# --- 使用示例 ---
if __name__ == "__main__":
    generate_image("画一只可爱的橘猫，卡通风格")
```

---

## 响应格式

### 纯文本回复

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "文本回复内容",
      "reasoning_content": "推理思考过程（可选）",
      "thinking_signature": "签名（可选）"
    }
  }],
  "usage": { "prompt_tokens": 7, "completion_tokens": 104, "total_tokens": 111 }
}
```

### 图像生成回复

> **重要**：生成图像时，图像数据在 `message.image_urls` 数组中，`content` 可能为空字符串。

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "",
      "reasoning_content": "推理过程...",
      "thinking_signature": "...",
      "image_urls": [
        "data:image/png;base64,iVBORw0KGgoAAAANSUh..."
      ]
    }
  }],
  "usage": { "prompt_tokens": 226, "completion_tokens": 2748, "total_tokens": 2974 }
}
```

**提取图像的方式**：
```python
import base64

image_urls = message.get("image_urls", [])
for url in image_urls:
    header, b64data = url.split(",", 1)  # "data:image/png;base64," + data
    with open("output.png", "wb") as f:
        f.write(base64.b64decode(b64data))
```
```

---

## 常见错误

### 400: 缺少 response_modalities

```json
{
  "error": {
    "message": "vertexai.response_modalities must be set to [\"IMAGE\", \"TEXT\"]",
    "type": "InvalidRequestErrorFromAIGW"
  }
}
```

**解决**：请求体中必须加上 `"vertexai": {"response_modalities": ["IMAGE", "TEXT"]}`。

### 网络访问

| 网络环境 | API 地址 |
|---------|---------|
| 外网 (SAVPN/办公网) | `https://aigw.netease.com` |
| 内网 (VPN) | `https://aigw-int.netease.com` |

---

## 与 NetEaseAIGWClient 集成

可直接使用项目中已有的客户端，通过 `**kwargs` 传递 `vertexai` 参数：

```python
from skills.scripts.netease_aigw_client import NetEaseAIGWClient

client = NetEaseAIGWClient(
    app_id="p4x4nxxigw2ccja7",
    app_key="7vfnst67x7dcmghii83cw47uovjqpmrx",
)

result = client.chat(
    model="gemini-3.1-flash-image",
    messages=[{"role": "user", "content": "你好"}],
    vertexai={"response_modalities": ["IMAGE", "TEXT"]},
)

print(result["choices"][0]["message"]["content"])
```
