#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 NetEase AIGW API 连接
验证技能是否正常工作

用法:
    cd /Users/tangdan/Desktop/netease_aigw
    python skills/test_connection.py
"""

from scripts.netease_aigw_client import NetEaseAIGWClient


def test_connection():
    """测试 API 连接"""
    print("=" * 60)
    print("🚀 NetEase AIGW API 连接测试")
    print("=" * 60)
    print()

    # 创建客户端 - 使用环境变量或默认值
    import os

    app_id = os.environ.get("NETEASE_APP_ID", "a3qanjtg0juk4juz")
    app_key = os.environ.get("NETEASE_APP_KEY", "68ip3dor15ojfusqph4z5nz907q5l2zr")

    client = NetEaseAIGWClient(app_id=app_id, app_key=app_key)

    # 测试 1：列出可用模型
    print("📋 测试 1：获取可用模型列表")
    print("-" * 60)
    try:
        # 获取 API 模型列表
        api_models = client.get_models()
        print(f"[OK] API 模型列表: {len(api_models.get('data', []))} 个")

        # 获取本地支持的模型列表
        supported = client.list_supported_models()
        print(f"[OK] 本地支持模型数量: {len(supported)}")
        for model in supported[:5]:  # 只显示前5个
            print(f"   - {model.name}: {model.description}")
        if len(supported) > 5:
            print(f"   ... 共 {len(supported)} 个模型")
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 测试 2：基础对话 - Claude Opus
    print("💬 测试 2：Claude Opus 4.6 对话测试")
    print("-" * 60)
    try:
        response = client.chat(
            model="claude-opus-4-6",
            messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
            max_tokens=100,
        )
        content = response["choices"][0]["message"]["content"]
        print(f"[OK] 回复: {content}")
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 测试 3：Claude Sonnet
    print("🧠 测试 3：Claude Sonnet 4.6 对话测试")
    print("-" * 60)
    try:
        response = client.chat(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "什么是人工智能？请用一句话回答"}],
            max_tokens=100,
        )
        content = response["choices"][0]["message"]["content"]
        print(f"[OK] 回复: {content}")
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 测试 4：DeepSeek 对话
    print("🔍 测试 4：DeepSeek Chat 对话测试")
    print("-" * 60)
    try:
        response = client.chat(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "请解释什么是大语言模型"}],
            max_tokens=150,
        )
        content = response["choices"][0]["message"]["content"]
        print(f"[OK] 回复: {content}")
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 测试 5：代码生成（使用 Claude）
    print("💻 测试 5：Claude 代码生成测试")
    print("-" * 60)
    try:
        response = client.chat(
            model="claude-opus-4-6",
            messages=[
                {
                    "role": "user",
                    "content": "写一个 Python 快速排序函数，只返回代码，不需要解释",
                }
            ],
            max_tokens=200,
            temperature=0.3,  # 代码生成建议使用较低温度
        )
        code = response["choices"][0]["message"]["content"]
        print("[OK] 生成的代码：")
        print(code)
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 测试 6：多轮对话（上下文保留）
    print("🔄 测试 6：多轮对话（上下文保留）")
    print("-" * 60)
    try:
        messages = [{"role": "user", "content": "My name is ZhangSan"}]
        response1 = client.chat(
            model="claude-opus-4-6", messages=messages, max_tokens=100
        )
        answer1 = response1["choices"][0]["message"]["content"]
        print(f"[OK] Q1: {messages[0]['content']}")
        print(f"    A1: {answer1}")

        # 保留上下文继续对话
        messages.append({"role": "assistant", "content": answer1})
        messages.append({"role": "user", "content": "What is my name?"})

        response2 = client.chat(
            model="claude-opus-4-6", messages=messages, max_tokens=100
        )
        answer2 = response2["choices"][0]["message"]["content"]
        print(f"    Q2: {messages[2]['content']}")
        print(f"    A2: {answer2}")
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 测试 7：获取模型详细信息
    print("📊 测试 7：获取模型信息")
    print("-" * 60)
    try:
        model_info = client.get_model_info("claude-opus-4-6")
        print(f"[OK] Claude Opus 4.6 信息:")
        print(f"    ID: {model_info.get('id', 'N/A')}")
        if "pricing" in model_info:
            print(f"    定价: {model_info['pricing']}")
    except Exception as e:
        print(f"[FAIL] {e}")
    print()

    # 总结
    print("=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
    print()
    print("💡 使用提示：")
    print("   - 设置环境变量以保护凭证:")
    print("     export NETEASE_APP_ID='your_app_id'")
    print("     export NETEASE_APP_KEY='your_app_key'")
    print()
    print("   - 查看更多示例: python skills/examples.py")
    print("   - 查看模型列表: python skills/aigw_cmd.py list")
    print()


if __name__ == "__main__":
    test_connection()
