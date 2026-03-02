#!/usr/bin/env python3
"""测试 AIGW 连接"""

import requests

# 测试多个可能的 URL
urls = [
    "https://aigw-int.nie.netease.com",
    "https://aigw.nie.netease.com",
    "https://aigw-int.netease.com",
]

headers = {
    "Authorization": "Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr",
    "Content-Type": "application/json"
}

data = {
    "model": "claude-oplus-4-6",
    "messages": [{"role": "user", "content": "hi"}],
    "max_tokens": 10
}

for url in urls:
    print(f"\n{'='*50}")
    print(f"测试: {url}")
    print(f"{'='*50}")

    try:
        response = requests.post(
            f"{url}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print("❌ 连接超时 (10秒)")
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")

print("\n" + "="*50)
print("测试完成")
print("="*50)
