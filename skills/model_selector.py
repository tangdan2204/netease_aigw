#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetEase AIGW 模型选择器
在 OpenCode 中快速选择和测试不同模型
"""

from scripts.netease_aigw_client import NetEaseAIGWClient, create_default_client

# 可用模型列表
AIGW_MODELS = {
    "1": {
        "id": "claude-opus-4-6",
        "name": "Claude Opus 4",
        "desc": "高级推理、复杂任务、代码生成",
        "type": "Anthropic"
    },
    "2": {
        "id": "claude-sonnet-4-6", 
        "name": "Claude Sonnet 4",
        "desc": "平衡型对话、日常任务",
        "type": "Anthropic"
    },
    "3": {
        "id": "gpt-5.2-codex-2026-01-14",
        "name": "GPT-5 Codex",
        "desc": "代码生成、代码重构",
        "type": "OpenAI"
    },
    "4": {
        "id": "gpt-4.5-2024-01-27",
        "name": "GPT-4.5",
        "desc": "通用对话、知识问答",
        "type": "OpenAI"
    },
}

def list_models():
    """列出所有可用模型"""
    print("\n" + "=" * 60)
    print("📋 NetEase AIGW 可用模型列表")
    print("=" * 60)
    print()
    
    for num, model in AIGW_MODELS.items():
        print(f"  [{num}] {model['name']}")
        print(f"      ID: {model['id']}")
        print(f"      类型: {model['type']}")
        print(f"      用途: {model['desc']}")
        print()
    
    print("=" * 60)
    print("\n💡 使用方法:")
    print("   选择模型: 输入序号，如: 1")
    print("   快速测试: 输入 t+序号，如: t1")
    print("   对话模式: 输入 chat+序号，如: chat1\n")

def quick_test(model_num):
    """快速测试单个模型"""
    if model_num not in AIGW_MODELS:
        print(f"❌ 无效序号: {model_num}")
        return
    
    model_info = AIGW_MODELS[model_num]
    model_id = model_info["id"]
    
    print(f"\n🧪 快速测试: {model_info['name']}")
    print("-" * 40)
    print("输入你的问题（直接回车使用默认问题）:", end=" ")
    
    user_input = input().strip()
    if not user_input:
        user_input = "请用一句话介绍你自己"
    
    client = create_default_client()
    
    try:
        response = client.chat(
            model=model_id,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=200
        )
        result = response["choices"][0]["message"]["content"]
        print(f"\n🤖 {model_info['name']} 回复:")
        print(f"   {result}")
        print()
    except Exception as e:
        print(f"\n❌ 调用失败: {e}\n")

def interactive_chat(model_num):
    """交互式对话"""
    if model_num not in AIGW_MODELS:
        print(f"❌ 无效序号: {model_num}")
        return
    
    model_info = AIGW_MODELS[model_num]
    model_id = model_info["id"]
    
    print(f"\n💬 开始与 {model_info['name']} 对话")
    print("-" * 40)
    print("输入你的问题，输入 /quit 退出对话\n")
    
    client = create_default_client()
    messages = []
    
    while True:
        user_input = input("你: ").strip()
        
        if user_input == "/quit":
            print("👋 对话结束")
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat(
                model=model_id,
                messages=messages,
                max_tokens=500
            )
            reply = response["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            
            print(f"\n🤖 {model_info['name']}:")
            print(f"   {reply}\n")
            
        except Exception as e:
            print(f"\n❌ 调用失败: {e}\n")

def get_client(model_id):
    """获取指定模型的客户端"""
    return create_default_client()

def main():
    """主函数"""
    import sys
    
    # 如果有参数，直接执行
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "list":
            list_models()
        elif arg.startswith("t") and arg[1:].isdigit():
            quick_test(arg[1:])
        elif arg.startswith("chat") and arg[4:].isdigit():
            interactive_chat(arg[4:])
        elif arg.isdigit() and arg in AIGW_MODELS:
            quick_test(arg)
        else:
            print("❌ 无效参数")
            print("\n💡 用法:")
            print("   python model_selector.py list    - 列出所有模型")
            print("   python model_selector.py t1      - 快速测试模型1")
            print("   python model_selector.py chat1  - 与模型1对话")
        return
    
    # 交互模式
    list_models()
    
    print("请选择操作: ", end="")
    choice = input().strip()
    
    if choice.isdigit() and choice in AIGW_MODELS:
        quick_test(choice)
    elif choice.startswith("t") and choice[1:].isdigit():
        quick_test(choice[1:])
    elif choice.startswith("chat") and choice[4:].isdigit():
        interactive_chat(choice[4:])
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main()
