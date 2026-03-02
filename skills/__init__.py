#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetEase AIGW 快速调用工具
在 OpenCode 中直接使用，无需记忆模型ID
"""

from scripts.netease_aigw_client import create_default_client

# 简化的模型名称映射
MODEL_ALIASES = {
    "claude": "claude-opus-4-6",
    "opus": "claude-opus-4-6",
    "sonnet": "claude-sonnet-4-6",
    "gpt-code": "gpt-5.2-codex-2026-01-14",
    "codex": "gpt-5.2-codex-2026-01-14",
    "gpt4": "gpt-4.5-2024-01-27",
    "gpt": "gpt-4.5-2024-01-27",
}

# 便捷的默认客户端
_client = None

def _get_client():
    """获取默认客户端"""
    global _client
    if _client is None:
        _client = create_default_client()
    return _client

def chat(prompt, model=None, max_tokens=1000):
    """
    快速对话
    
    用法:
        chat("你好")  # 使用默认 Claude Opus
        chat("写代码", model="gpt-code")  # 指定模型
        chat("帮我写排序", model="codex")  # 使用别名
    
    模型别名:
        claude, opus -> claude-opus-4-6
        sonnet -> claude-sonnet-4-6
        gpt-code, codex -> gpt-5.2-codex-2026-01-14
        gpt, gpt4 -> gpt-4.5-2024-01-27
    """
    client = _get_client()
    
    # 解析模型
    actual_model = "claude-opus-4-6"  # 默认
    if model:
        model_str = model.lower().strip()
        actual_model = MODEL_ALIASES.get(model_str, model)
    
    response = client.chat(
        model=actual_model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    
    return response["choices"][0]["message"]["content"]

def code(prompt, max_tokens=500):
    """
    代码生成（使用 GPT Codex）
    
    用法:
        code("写一个快速排序")
    """
    client = _get_client()
    
    response = client.chat(
        model="gpt-5.2-codex-2026-01-14",
        messages=[{"role": "user", "content": f"请生成以下代码:\n{prompt}"}],
        max_tokens=max_tokens,
        temperature=0.3
    )
    
    return response["choices"][0]["message"]["content"]

def review(code_text, max_tokens=1000):
    """
    代码审查（使用 Claude）
    
    用法:
        review("def add(a,b): return a+b")
    """
    client = _get_client()
    
    response = client.chat(
        model="claude-opus-4-6",
        messages=[{
            "role": "user", 
            "content": f"请审查以下代码，指出问题和改进建议:\n\n{code_text}"
        }],
        max_tokens=max_tokens
    )
    
    return response["choices"][0]["message"]["content"]

def explain(code_text, max_tokens=1000):
    """
    代码解释
    
    用法:
        explain("你的代码")
    """
    client = _get_client()
    
    response = client.chat(
        model="claude-opus-4-6",
        messages=[{
            "role": "user", 
            "content": f"请解释以下代码的功能:\n\n{code_text}"
        }],
        max_tokens=max_tokens
    )
    
    return response["choices"][0]["message"]["content"]

def ask(question, model="claude", max_tokens=1000):
    """
    智能问答
    
    用法:
        ask("什么是装饰器")  # 默认 Claude
        ask("Python 技巧", model="sonnet")  # 使用 Sonnet
    """
    client = _get_client()
    
    # 解析模型
    model_str = model.lower().strip()
    actual_model = MODEL_ALIASES.get(model_str, "claude-opus-4-6")
    
    response = client.chat(
        model=actual_model,
        messages=[{"role": "user", "content": question}],
        max_tokens=max_tokens
    )
    
    return response["choices"][0]["message"]["content"]

# 显示可用模型
def show_models():
    """显示所有可用模型"""
    models = """
NetEase AIGW 可用模型

  [默认模型]
     claude / opus -> Claude Opus 4 (高级推理)

  [Claude 系列]
     claude, opus -> claude-oplus-4-6 (高级)
     sonnet -> claude-sonnet-4-6 (平衡)

  [GPT 系列]
     gpt-code, codex -> gpt-5.2-codex-2026-01-14 (代码)
     gpt, gpt4 -> gpt-4.5-2024-01-27 (通用)

[快速使用]:
   from scripts.netease_aigw import chat, code, review, ask
   
   chat("帮我写代码")                    # 默认 Claude
   chat("写代码", model="gpt-code")    # 指定 GPT Codex
   code("快速排序函数")                  # 代码生成
   review("我的代码")                    # 代码审查
   ask("什么是闭包")                    # 智能问答
"""
    print(models)
    return models

# 测试函数
def test():
    """测试连接"""
    print("[测试 NetEase AIGW 连接...]\n")
    
    try:
        result = chat("hi", max_tokens=10)
        print(f"[OK] 连接成功! 测试回复: {result}")
        return True
    except Exception as e:
        print(f"[FAIL] 连接失败: {e}")
        return False
