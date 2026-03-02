#!/usr/bin/env python3
"""
NetEase AI Gateway API Client
简化 API 调用，提供便捷的接口在 OpenCode 中使用
"""

import requests
import json
from typing import List, Dict, Generator, Optional


class NetEaseAIGWClient:
    """NetEase AI Gateway API 客户端"""

    def __init__(
        self,
        app_id: str = "a3qanjtg0juk4juz",
        app_key: str = "68ip3dor15ojfusqph4z5nz907q5l2zr",
        base_url: str = "https://aigw.netease.com",
        timeout: int = 60
    ):
        """
        初始化客户端

        参数说明：
            app_id：网易 AIGW 的 App ID
            app_key：网易 AIGW 的 App Key
            base_url：API 基础 URL
            timeout：请求超时时间（秒）
        """
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = base_url
        self.timeout = timeout
        self.auth_token = f"Bearer {app_id}.{app_key}"
        self.headers = {
            "Authorization": self.auth_token,
            "Content-Type": "application/json"
        }

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        stream: bool = False,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        """
        发送聊天请求

        参数说明：
            model：模型名称（如 "claude-opus-4-6"）
            messages：消息列表
            max_tokens：最大生成 token 数
            stream：是否使用流式响应
            temperature：温度参数（0.0-1.0）
            **kwargs：其他 API 参数

        返回值：
            API 响应数据

        异常：
            Exception：当请求失败时抛出
        """
        url = f"{self.base_url}/v1/chat/completions"

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": stream,
            "temperature": temperature,
            **kwargs
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(
                    f"API 请求失败：{response.status_code}\n"
                    f"错误信息：{response.text}"
                )

        except requests.exceptions.Timeout:
            raise Exception(f"请求超时（{self.timeout}秒）")
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"连接错误：{e}")
        except Exception as e:
            raise Exception(f"未知错误：{e}")

    def chat_stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        发送流式聊天请求

        参数说明：
            model：模型名称
            messages：消息列表
            max_tokens：最大 token 数
            temperature：温度参数
            **kwargs：其他 API 参数

        返回值：
            Generator：逐个 yield 响应片段
        """
        url = f"{self.base_url}/v1/chat/completions"

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
            "temperature": temperature,
            **kwargs
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=self.timeout,
                stream=True
            )

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data_str)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            pass

        except requests.exceptions.Timeout:
            raise Exception(f"请求超时（{self.timeout}秒）")
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"连接错误：{e}")
        except Exception as e:
            raise Exception(f"未知错误：{e}")

    def generate_code(
        self,
        prompt: str,
        model: str = "gpt-5.2-codex-2026-01-14",
        max_tokens: int = 1000,
        temperature: float = 0.3
    ) -> str:
        """
        生成代码（便捷方法）

        参数说明：
            prompt：代码生成提示
            model：代码生成模型
            max_tokens：最大 token 数
            temperature：温度参数（较低值更稳定）

        返回值：
            生成的代码文本
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(model, messages, max_tokens, temperature=temperature)
        return response["choices"][0]["message"]["content"]

    def review_code(
        self,
        code: str,
        model: str = "claude-opus-4-6",
        max_tokens: int = 1000
    ) -> str:
        """
        代码审查（便捷方法）

        参数说明：
            code：待审查的代码
            model：审查模型
            max_tokens：最大 token 数

        返回值：
            审查意见
        """
        prompt = f"请审查以下代码，指出潜在问题和改进建议：\n\n```\n{code}\n```"
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(model, messages, max_tokens)
        return response["choices"][0]["message"]["content"]

    def explain_code(
        self,
        code: str,
        model: str = "claude-opus-4-6",
        max_tokens: int = 1000
    ) -> str:
        """
        代码解释（便捷方法）

        参数说明：
            code：待解释的代码
            model：解释模型
            max_tokens：最大 token 数

        返回值：
            代码解释
        """
        prompt = f"请解释以下代码的功能和实现原理：\n\n```\n{code}\n```"
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(model, messages, max_tokens)
        return response["choices"][0]["message"]["content"]


def create_default_client() -> NetEaseAIGWClient:
    """
    创建使用默认凭证的客户端

    返回值：
        NetEaseAIGWClient：已配置的客户端实例
    """
    return NetEaseAIGWClient(
        app_id="a3qanjtg0juk4juz",
        app_key="68ip3dor15ojfusqph4z5nz907q5l2zr"
    )


# 使用示例
if __name__ == "__main__":
    # 创建客户端
    client = create_default_client()

    print("=== 简单对话示例 ===")
    response = client.chat(
        model="claude-opus-4-6",
        messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
        max_tokens=100
    )
    print(response["choices"][0]["message"]["content"])

    print("\n=== 代码生成示例 ===")
    code = client.generate_code(
        prompt="写一个 Python 快速排序函数",
        max_tokens=300
    )
    print(code)

    print("\n=== 代码审查示例 ===")
    test_code = """
def add(a, b):
    return a + b
"""
    review = client.review_code(test_code, max_tokens=200)
    print(review)
