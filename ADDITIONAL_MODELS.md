# 额外抓取的模型配置

> **更新时间**: 2025年2月13日  
> **数据来源**: https://modelspace.netease.com/model_app

---

## 目录

1. [gemini-3-pro-image](#1-gemini-3-pro-image)
2. [gemini-3-pro](#2-gemini-3-pro)
3. [doubao-seedream-4.5](#3-doubao-seedream-45)

---

## 1. gemini-3-pro-image

### 基本信息
- **模型代号**: `gemini-3-pro-image`
- **开发方**: Google
- **类别**: LLM 多模态
- **阶段**: 测试阶段
- **描述**: 专为专业素材资源制作和复杂指令而设计

### 技术规格
- **上下文窗口**: 1048K Tokens
- **最大输入长度**: 1048K Tokens
- **最大输出长度**: 66K Tokens
- **特性**: 思维链、图片生成、图片编辑
- **功能**: image
- **支持格式**: openai.chat

### 限流配置
- **总 RPM 限制**: 6K
- **总 TPM 限制**: 3M
- **默认 RPM**: 120（最大可调整至 1K）
- **默认 TPM**: 240K（最大可调整至 1M）

### 定价
- **推理输入**: ¥14.400 / 百万tokens
- **推理输出**: ¥86.400 / 百万tokens

### Python 示例
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gemini-3-pro-image",
    "messages": [
        {
            "role": "user",
            "content": "你好，请介绍一下你自己"
        }
    ],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

### 官方文档
- https://aigw.doc.nie.netease.com/22_供应商指南/7_Google/4_模型.html

---

## 2. gemini-3-pro

### 基本信息
- **模型代号**: `gemini-3-pro`
- **开发方**: Google
- **类别**: LLM 多模态
- **阶段**: 测试阶段
- **描述**: Google最先进的AI模型，擅长高级推理、编码、数学和科学任务

### 技术规格
- **上下文窗口**: 1048K Tokens
- **最大输入长度**: 1048K Tokens
- **最大输出长度**: 66K Tokens
- **特性**: 思维链、识别图片、音频理解、视频理解、PDF读取
- **功能**: text, image, audio, video
- **支持格式**: openai.chat

### 限流配置
- **总 RPM 限制**: 6K
- **总 TPM 限制**: 3M
- **默认 RPM**: 300（最大可调整至 1K）
- **默认 TPM**: 600K（最大可调整至 2M）

### 定价
- **推理输入**: ¥28.800 / 百万tokens
- **推理输出**: ¥129.600 / 百万tokens

### Python 示例
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gemini-3-pro",
    "messages": [
        {
            "role": "user",
            "content": "你好，请介绍一下你自己"
        }
    ],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

### 官方文档
- https://aigw.doc.nie.netease.com/22_供应商指南/7_Google/4_模型.html

---

## 3. doubao-seedream-4.5

### 基本信息
- **模型代号**: `doubao-seedream-4-5`
- **开发方**: 字节跳动
- **供应商**: 火山引擎
- **类型**: 图像生成
- **阶段**: 测试阶段
- **描述**: Seedream 4.5 是字节跳动最新推出的图像多模态模型，整合了文生图、图生图、组图输出等能力，融合常识和推理能力。相比前代4.0模型生成效果大幅提升，具备更好的编辑一致性和多图融合效果，能更精准的控制画面细节，小字、小人脸生成更自然。

### 技术规格
- **上下文窗口**: 未提供
- **最大输入长度**: 未提供
- **最大输出长度**: 未提供
- **类别**: 生图
- **功能**: image
- **支持格式**: openai.chat

### 限流配置
- **总 RPM 限制**: 0
- **总 TPM 限制**: 0
- **默认 RPM**: 0（最大可调整至 0）
- **默认 TPM**: 0（最大可调整至 0）

### 定价
- **推理输入**: ¥200000.000 / 百万tokens

### Python 示例
```python
import requests

url = "https://aigw-int.netease.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer {app_id}.{app_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "doubao-seedream-4-5",
    "messages": [
        {
            "role": "user",
            "content": "生成一张美丽的风景图片"
        }
    ],
    "max_tokens": 1000,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

### 官方文档
- https://aigw.doc.nie.netease.com/22_供应商指南/5_字节跳动/4_模型.html

---

## OpenCode 配置

### 配置文件位置
**macOS/Linux**: `~/.config/opencode/opencode.json`

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
        "gemini-3-pro-image": {
          "name": "Gemini 3 Pro Image (Google)",
          "description": "Google 图像生成模型",
          "limit": {"context": 1048000, "output": 66000}
        },
        "gemini-3-pro": {
          "name": "Gemini 3 Pro (Google)",
          "description": "Google 最先进的AI模型",
          "limit": {"context": 1048000, "output": 66000}
        },
        "doubao-seedream-4-5": {
          "name": "Doubao Seedream 4.5 (字节)",
          "description": "字节跳动图像生成模型",
          "limit": {"context": 0, "output": 0}
        }
      }
    }
  }
}
```

---

## 模型对比

| 模型 | 开发方 | 上下文 | 输入价格 | 输出价格 | 特点 |
|------|--------|--------|---------|---------|------|
| gemini-3-pro-image | Google | 1048K | ¥14.4/百万 | ¥86.4/百万 | 图像生成 |
| gemini-3-pro | Google | 1048K | ¥28.8/百万 | ¥129.6/百万 | 多模态推理 |
| doubao-seedream-4.5 | 字节 | - | ¥200000/百万 | - | 图像生成 |

---

## 相关资源

- **模型市场**: https://modelspace.netease.com/model_app
- **API 文档**: https://aigw.doc.nie.netease.com
- **控制台**: https://aigw.console.nie.netease.com

---

**版本**: 1.0  
**创建时间**: 2025年2月13日
