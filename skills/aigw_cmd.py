#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NetEase AIGW 命令行工具
在 OpenCode 中使用类似 /model 的命令切换模型
"""

import sys
import re

# 可用模型（基于 AIGW 官方支持的模型）
MODELS = {
    # Claude 系列（推荐）
    "claude-opus": {
        "id": "claude-opus-4-6",
        "name": "Claude Opus 4.6",
        "category": "Claude",
    },
    "opus": {"id": "claude-opus-4-6", "name": "Claude Opus 4.6", "category": "Claude"},
    "claude": {
        "id": "claude-opus-4-6",
        "name": "Claude Opus 4.6",
        "category": "Claude",
    },
    "claude-sonnet": {
        "id": "claude-sonnet-4-6",
        "name": "Claude Sonnet 4.6",
        "category": "Claude",
    },
    "sonnet": {
        "id": "claude-sonnet-4-6",
        "name": "Claude Sonnet 4.6",
        "category": "Claude",
    },
    "claude-haiku": {
        "id": "claude-haiku-4-6",
        "name": "Claude Haiku 4.6",
        "category": "Claude",
    },
    "haiku": {
        "id": "claude-haiku-4-6",
        "name": "Claude Haiku 4.6",
        "category": "Claude",
    },
    # DeepSeek 系列
    "deepseek": {
        "id": "deepseek-chat",
        "name": "DeepSeek Chat",
        "category": "DeepSeek",
    },
    "deepseek-chat": {
        "id": "deepseek-chat",
        "name": "DeepSeek Chat",
        "category": "DeepSeek",
    },
    "deepseek-reasoner": {
        "id": "deepseek-reasoner",
        "name": "DeepSeek Reasoner",
        "category": "DeepSeek",
    },
    "reasoner": {
        "id": "deepseek-reasoner",
        "name": "DeepSeek Reasoner",
        "category": "DeepSeek",
    },
    # GPT 系列
    "gpt-4o": {"id": "gpt-4o", "name": "GPT-4o", "category": "OpenAI"},
    "gpt4o": {"id": "gpt-4o", "name": "GPT-4o", "category": "OpenAI"},
    "gpt-4o-mini": {"id": "gpt-4o-mini", "name": "GPT-4o-mini", "category": "OpenAI"},
    "gpt4o-mini": {"id": "gpt-4o-mini", "name": "GPT-4o-mini", "category": "OpenAI"},
}

# 当前选中的模型（全局状态）
_current_model = "claude"


def _get_current_model():
    """获取当前模型"""
    return MODELS[_current_model]["id"]


def _set_current_model(model_name):
    """设置当前模型"""
    global _current_model
    model_key = model_name.lower()
    if model_key in MODELS:
        _current_model = model_key
        return True
    return False


def print_help():
    """打印帮助信息"""
    help_text = """
NetEase AIGW 模型切换命令

用法:
  /model                   - 显示当前模型
  /model list             - 列出所有可用模型
  /model <模型名>          - 切换到指定模型

可用模型:
  claude, opus         -> Claude Opus 4 (默认，高级推理)
  sonnet               -> Claude Sonnet 4 (平衡对话)
  gpt-code, codex     -> GPT-5 Codex (代码生成)
  gpt4, gpt           -> GPT-4.5 (通用对话)

示例:
  /model list
  /model claude
  /model gpt-code

注意: 当前状态仅在本次会话有效
"""
    print(help_text)


def print_models():
    """列出所有模型"""
    print("\n[可用模型列表]")
    print("-" * 40)

    categories = {
        "Claude 系列": ["claude", "opus", "sonnet"],
        "GPT 系列": ["gpt-code", "codex", "gpt4", "gpt"],
    }

    for category, aliases in categories.items():
        print(f"\n{category}:")
        shown = set()
        for alias in aliases:
            if alias not in shown:
                model = MODELS[alias]
                print(f"  . {alias:12} -> {model['id']}")
                shown.add(alias)


def print_current():
    """显示当前模型"""
    model = MODELS[_current_model]
    print(f"\n[当前模型: {model['name']} ({model['id']})]")


def parse_command(cmd):
    """
    解析命令

    支持:
      /model
      /model list
      /model <模型名>
    """
    cmd = cmd.strip()

    if not cmd.startswith("/model"):
        return False, "未知命令。使用 /model 查看帮助"

    parts = cmd.split()

    if len(parts) == 1:
        # /model
        print_current()
        return True, None

    elif len(parts) == 2:
        arg = parts[1].lower()

        if arg == "list":
            print_models()
            return True, None
        elif arg in ["help", "-h", "--help"]:
            print_help()
            return True, None
        else:
            # /model <模型名>
            if _set_current_model(arg):
                print_current()
                return True, None
            else:
                return False, f"未知的模型: {arg}\n使用 /model list 查看可用模型"
    else:
        return False, "命令格式错误。使用 /model 查看帮助"


def get_current_model_id():
    """获取当前模型ID（供外部调用）"""
    return _get_current_model()


# 主函数
def main():
    """命令行入口"""
    if len(sys.argv) == 1:
        print_help()
    elif len(sys.argv) == 2:
        cmd = sys.argv[1]
        parse_command(cmd)
    else:
        print('❌ 参数错误。使用: python aigw_cmd.py "/model <选项>"')


if __name__ == "__main__":
    main()
