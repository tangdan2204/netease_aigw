#!/usr/bin/env python3
"""
NetEase AIGW 技能使用示例
在 OpenCode 中使用网易 AI 模型的各种场景
"""

from scripts.netease_aigw_client import NetEaseAIGWClient, create_default_client


def example_1_basic_chat():
    """示例 1：基础对话"""
    print("=" * 50)
    print("示例 1：基础对话")
    print("=" * 50)

    client = create_default_client()

    response = client.chat(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
        max_tokens=100,
    )

    print("AI 回复：", response["choices"][0]["message"]["content"])
    print()


def example_2_code_generation():
    """示例 2：代码生成"""
    print("=" * 50)
    print("示例 2：代码生成")
    print("=" * 50)

    client = create_default_client()

    # 使用 Claude 生成代码
    code_prompt = """请写一个 Python 快速排序函数，包含详细注释。
要求：
1. 函数有完整的类型注解
2. 包含 docstring
3. 代码简洁易读"""

    response = client.chat(
        model="claude-opus-4-6",
        messages=[
            {"role": "system", "content": "你是一个专业的 Python 开发者"},
            {"role": "user", "content": code_prompt},
        ],
        max_tokens=500,
        temperature=0.3,  # 代码生成建议使用较低温度
    )

    print("生成的代码：")
    print(response["choices"][0]["message"]["content"])
    print()


def example_3_code_review():
    """示例 3：代码审查"""
    print("=" * 50)
    print("示例 3：代码审查")
    print("=" * 50)

    client = create_default_client()

    test_code = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total / len(numbers)
"""

    # 使用 Claude 进行代码审查
    review_prompt = f"""请审查以下 Python 代码，指出潜在问题和改进建议：

```python
{test_code}
```

请从以下方面分析：
1. 潜在 bug
2. 代码风格问题
3. 性能优化建议
4. 安全性问题"""

    response = client.chat(
        model="claude-opus-4-6",
        messages=[
            {"role": "system", "content": "你是一个资深代码审查专家"},
            {"role": "user", "content": review_prompt},
        ],
        max_tokens=800,
    )

    print("待审查代码：")
    print(test_code)
    print("\n审查意见：")
    print(response["choices"][0]["message"]["content"])
    print()


def example_4_code_explanation():
    """示例 4：代码解释"""
    print("=" * 50)
    print("示例 4：代码解释")
    print("=" * 50)

    client = create_default_client()

    code = """
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
"""

    # 使用 Claude 解释代码
    explain_prompt = f"""请详细解释以下 Python 代码的工作原理：

```python
{code}
```

请包含：
1. 代码整体功能
2. 关键步骤说明
3. 时间复杂度分析
4. 使用示例"""

    response = client.chat(
        model="claude-opus-4-6",
        messages=[
            {"role": "system", "content": "你是一个编程教育专家"},
            {"role": "user", "content": explain_prompt},
        ],
        max_tokens=600,
    )

    print("待解释代码：")
    print(code)
    print("\n代码解释：")
    print(response["choices"][0]["message"]["content"])
    print()


def example_5_streaming():
    """示例 5：流式输出"""
    print("=" * 50)
    print("示例 5：流式输出")
    print("=" * 50)

    client = create_default_client()

    print("AI 回复（实时流式输出）：")
    print("-" * 50)
    for chunk in client.chat_stream(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": "请用 3 点解释什么是递归"}],
        max_tokens=300,
    ):
        print(chunk, end="", flush=True)
    print("\n")


def example_6_conversation():
    """示例 6：多轮对话"""
    print("=" * 50)
    print("示例 6：多轮对话")
    print("=" * 50)

    client = create_default_client()

    messages = []

    # 第一轮
    messages.append({"role": "user", "content": "什么是 Python 装饰器？"})
    response1 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)
    messages.append(
        {"role": "assistant", "content": response1["choices"][0]["message"]["content"]}
    )

    print("Q1：什么是 Python 装饰器？")
    print("A1：", response1["choices"][0]["message"]["content"][:100] + "...")

    # 第二轮
    messages.append({"role": "user", "content": "能给我一个简单的例子吗？"})
    response2 = client.chat(model="claude-opus-4-6", messages=messages, max_tokens=500)

    print("\nQ2：能给我一个简单的例子吗？")
    print("A2：", response2["choices"][0]["message"]["content"])
    print()


def example_7_different_models():
    """示例 7：使用不同模型"""
    print("=" * 50)
    print("示例 7：使用不同模型")
    print("=" * 50)

    client = create_default_client()
    prompt = "用一行代码输出 Hello World"

    models = [
        "claude-opus-4-6",  # Claude Opus - 最佳性能
        "claude-sonnet-4-6",  # Claude Sonnet - 平衡之选
        "deepseek-chat",  # DeepSeek - 性价比
    ]

    for model in models:
        response = client.chat(
            model=model, messages=[{"role": "user", "content": prompt}], max_tokens=100
        )
        print(f"{model}：")
        print(response["choices"][0]["message"]["content"])
        print()


def example_8_error_handling():
    """示例 8：错误处理"""
    print("=" * 50)
    print("示例 8：错误处理")
    print("=" * 50)

    client = create_default_client()

    try:
        response = client.chat(
            model="claude-opus-4-6",
            messages=[{"role": "user", "content": "测试"}],
            max_tokens=100,
        )
        print("成功：", response["choices"][0]["message"]["content"])

    except Exception as e:
        print(f"错误：{e}")
        # 这里可以添加重试逻辑或降级处理
        print("可以在这里添加重试逻辑……")
    print()


def example_9_temperature():
    """示例 9：温度参数对比"""
    print("=" * 50)
    print("示例 9：温度参数对比")
    print("=" * 50)

    client = create_default_client()
    prompt = "写一首关于春天的短诗"

    temperatures = [0.2, 0.7, 0.9]

    for temp in temperatures:
        response = client.chat(
            model="claude-opus-4-6",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=temp,
        )
        print(f"\n温度 {temp} 的输出：")
        print("-" * 30)
        print(response["choices"][0]["message"]["content"])
    print()


def example_10_max_tokens():
    """示例 10：max_tokens 参数对比"""
    print("=" * 50)
    print("示例 10：max_tokens 参数对比")
    print("=" * 50)

    client = create_default_client()

    max_tokens_list = [50, 200, 500]

    for max_tok in max_tokens_list:
        response = client.chat(
            model="claude-opus-4-6",
            messages=[{"role": "user", "content": "详细解释一下什么是机器学习"}],
            max_tokens=max_tok,
        )
        content = response["choices"][0]["message"]["content"]
        print(f"\nmax_tokens={max_tok} 的输出：")
        print("-" * 30)
        print(content[:300] + "..." if len(content) > 300 else content)
        print(f"（实际 token 数约 {response['usage']['completion_tokens']}）")
    print()


def main():
    """运行所有示例"""
    examples = [
        ("基础对话", example_1_basic_chat),
        ("代码生成", example_2_code_generation),
        ("代码审查", example_3_code_review),
        ("代码解释", example_4_code_explanation),
        ("流式输出", example_5_streaming),
        ("多轮对话", example_6_conversation),
        ("不同模型", example_7_different_models),
        ("错误处理", example_8_error_handling),
        ("温度对比", example_9_temperature),
        ("长度对比", example_10_max_tokens),
    ]

    print("\n" + "=" * 50)
    print("NetEase AIGW 技能使用示例")
    print("=" * 50)
    print("\n选择一个示例运行：\n")

    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    print(f"{len(examples) + 1}. 运行所有示例")
    print(f"{len(examples) + 2}. 退出")

    choice = input("\n请选择：")

    try:
        choice = int(choice)
        if 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        elif choice == len(examples) + 1:
            for name, func in examples:
                func()
                input("\n按 Enter 继续……")
        elif choice == len(examples) + 2:
            print("退出")
        else:
            print("无效选择")
    except ValueError:
        print("请输入数字")


if __name__ == "__main__":
    main()
