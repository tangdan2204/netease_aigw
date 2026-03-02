#!/usr/bin/env python3
"""测试 AIGW 连接 - 使用正确的模型名称"""

import requests

url = "https://aigw.netease.com/v1/chat/completions"

headers = {
    "Authorization": "Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr",
    "Content-Type": "application/json"
}

# 测试不同的模型名称
models_to_test = [
    "claude-opus-4-6",      # 根据 URL
    "claude-3-opus-2024-05", # Anthropic 官方格式
    "claude-opus-4",        # 简化版
    "gpt-4-1106-preview",   # 文档示例
]

for model in models_to_test:
    print(f"\n测试模型: {model}")
    print("-" * 40)

    data = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 10
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"错误: {e}")
