#!/usr/bin/env python3
"""
网易 AIGW Claude 模型调用测试脚本
"""

import requests
import json
import sys

# AIGW 配置
AIGW_BASE_URL = "https://aigw-int.netease.com"
AUTH_HEADER = "Bearer a3qanjtg0juk4juz.68ip3dor15ojfusqph4z5nz907q5l2zr"


def test_claude_connection():
    """测试 Claude 模型连接"""
    print("=" * 60)
    print("网易 AIGW Claude 模型连接测试")
    print("=" * 60)
    print()

    # 测试 1: 基础连接测试
    print("[1/3] 测试基础连接...")
    try:
        response = requests.get(AIGW_BASE_URL, timeout=10)
        print(f"    状态码: {response.status_code}")
        print(f"    ✓ 基础连接成功")
    except requests.exceptions.RequestException as e:
        print(f"    ✗ 基础连接失败: {e}")
        return False

    # 测试 2: Claude Opus-4-6 对话测试
    print()
    print("[2/3] 测试 Claude Opus-4-6 模型...")
    try:
        headers = {"Authorization": AUTH_HEADER, "Content-Type": "application/json"}

        data = {
            "model": "claude-opus-4-6",
            "messages": [{"role": "user", "content": "请用一句话介绍你自己"}],
            "max_tokens": 100,
            "temperature": 0.5,
        }

        response = requests.post(
            f"{AIGW_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"    响应: {content}")
            print(f"    ✓ Claude Opus-4-6 调用成功")
        else:
            print(f"    ✗ 调用失败: {response.status_code}")
            print(f"    响应: {response.text}")
            return False

    except Exception as e:
        print(f"    ✗ 调用异常: {e}")
        return False

    # 测试 3: 多轮对话测试
    print()
    print("[3/3] 测试多轮对话...")
    try:
        messages = [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！我是 Claude，一个 AI 助手。"},
            {"role": "user", "content": "你能做什么？"},
        ]

        data = {
            "model": "claude-opus-4-6",
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.7,
        }

        response = requests.post(
            f"{AIGW_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"    响应: {content}")
            print(f"    ✓ 多轮对话测试成功")
        else:
            print(f"    ✗ 调用失败: {response.status_code}")
            return False

    except Exception as e:
        print(f"    ✗ 调用异常: {e}")
        return False

    print()
    print("=" * 60)
    print("所有测试通过！✓")
    print("=" * 60)
    return True


def quick_chat(message: str, model: str = "claude-opus-4-6"):
    """快速对话接口"""
    headers = {"Authorization": AUTH_HEADER, "Content-Type": "application/json"}

    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    response = requests.post(
        f"{AIGW_BASE_URL}/v1/chat/completions", headers=headers, json=data, timeout=30
    )

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"请求失败: {response.status_code} - {response.text}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果提供了消息，直接进行快速对话
        message = " ".join(sys.argv[1:])
        print(f"发送消息: {message}")
        print()
        try:
            response = quick_chat(message)
            print(f"AI 回复: {response}")
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(1)
    else:
        # 运行完整测试
        test_claude_connection()
