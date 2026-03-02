#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易 AIGW API 客户端

提供网易 AI Gateway 的 Python 调用接口，支持多种 AI 模型。

功能特性:
- 多模型支持: Claude、DeepSeek、GPT 等
- 流式响应: SSE 流式输出
- 错误处理: 自动重试机制
- 成本追踪: 积分使用量查询
"""

import json
import time
import logging
from typing import Optional, Dict, List, Any, Generator, Union
from dataclasses import dataclass
from pathlib import Path

import requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelInfo:
    """模型信息"""

    name: str
    description: str
    context_length: int
    capabilities: List[str]


# 支持的模型列表
SUPPORTED_MODELS = {
    # Claude 系列
    "claude-opus-4-6": ModelInfo(
        name="claude-opus-4-6",
        description="Claude Opus 4.6 - 最强性能模型",
        context_length=200000,
        capabilities=["对话", "代码生成", "复杂推理", "长文本分析"],
    ),
    "claude-sonnet-4-6": ModelInfo(
        name="claude-sonnet-4-6",
        description="Claude Sonnet 4.6 - 平衡性能与速度",
        context_length=200000,
        capabilities=["对话", "代码生成", "日常任务"],
    ),
    "claude-haiku-4-6": ModelInfo(
        name="claude-haiku-4-6",
        description="Claude Haiku 4.6 - 快速响应模型",
        context_length=200000,
        capabilities=["快速对话", "简单任务", "轻量应用"],
    ),
    # DeepSeek 系列
    "deepseek-chat": ModelInfo(
        name="deepseek-chat",
        description="DeepSeek Chat - 对话模型",
        context_length=64000,
        capabilities=["中文对话", "代码生成", "推理分析"],
    ),
    "deepseek-reasoner": ModelInfo(
        name="deepseek-reasoner",
        description="DeepSeek Reasoner - 推理模型",
        context_length=64000,
        capabilities=["深度推理", "复杂分析", "数学计算"],
    ),
    # GPT 系列
    "gpt-4o": ModelInfo(
        name="gpt-4o",
        description="GPT-4o - OpenAI 多模态模型",
        context_length=128000,
        capabilities=["多模态", "对话", "代码生成"],
    ),
    "gpt-4o-mini": ModelInfo(
        name="gpt-4o-mini",
        description="GPT-4o-mini - 轻量快速模型",
        context_length=128000,
        capabilities=["快速响应", "简单任务"],
    ),
}


class AIGWError(Exception):
    """AIGW 基础异常类"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(AIGWError):
    """认证异常"""

    pass


class RateLimitError(AIGWError):
    """速率限制异常"""

    pass


class ModelNotFoundError(AIGWError):
    """模型不存在异常"""

    pass


class NeteaseAIGWClient:
    """
    网易 AIGW API 客户端

    初始化示例:
        client = NeteaseAIGWClient(
            app_id="your_app_id",
            app_key="your_app_key",
            base_url="https://aigw.netease.com"
        )

    使用示例:
        # 简单对话
        response = client.chat(
            model="claude-opus-4-6",
            messages=[{"role": "user", "content": "你好"}]
        )

        # 流式对话
        for chunk in client.chat_stream(
            model="claude-sonnet-4-6",
            messages=[{"role": "user", "content": "讲个故事"}]
        ):
            print(chunk, end="", flush=True)
    """

    # API 版本
    API_VERSION = "v1"

    # 重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 0.5

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        base_url: str = "https://aigw.netease.com",
        auth_token: Optional[str] = None,
        app_code: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 0.5,
    ):
        """
        初始化客户端

        Args:
            app_id: APP ID (APP 账号认证方式)
            app_key: APP Key (APP 账号认证方式)
            base_url: API 基础 URL
            auth_token: Auth Token (Auth 体系认证方式)
            app_code: APP Code (Auth 体系认证方式)
            timeout: 请求超时时间(秒)
            max_retries: 最大重试次数
            retry_delay: 重试间隔(秒)
        """
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.app_code = app_code
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # 设置认证头
        self.headers = {"Content-Type": "application/json"}
        self._setup_auth_headers()

        logger.info(f"AIGW 客户端初始化完成，Base URL: {self.base_url}")

    def _setup_auth_headers(self) -> None:
        """设置认证头"""
        if self.app_id and self.app_key:
            # APP 账号认证
            authorization = f"Bearer {self.app_id}.{self.app_key}"
            self.headers["Authorization"] = authorization
            logger.info("使用 APP 账号认证")
        elif self.auth_token and self.app_code:
            # Auth 体系认证
            self.headers["X-Access-Token"] = self.auth_token
            self.headers["X-AIGW-APP"] = self.app_code
            logger.info("使用 Auth 体系认证")
        else:
            raise ValueError(
                "必须提供认证信息: "
                "APP 账号认证 (app_id + app_key) 或 "
                "Auth 体系认证 (auth_token + app_code)"
            )

    @property
    def chat_completions_url(self) -> str:
        """获取聊天补全 API URL"""
        return f"{self.base_url}/{self.API_VERSION}/chat/completions"

    @property
    def models_url(self) -> str:
        """获取模型列表 API URL"""
        return f"{self.base_url}/{self.API_VERSION}/models"

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        发起 HTTP 请求(带重试机制)

        Args:
            method: HTTP 方法
            url: 请求 URL
            **kwargs: 其他请求参数

        Returns:
            Response 对象
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    timeout=self.timeout,
                    **kwargs,
                )

                # 处理特定状态码
                if response.status_code == 401:
                    raise AuthenticationError(
                        "认证失败，请检查 app_id 和 app_key 是否正确",
                        status_code=401,
                        response_body=response.text,
                    )
                elif response.status_code == 404:
                    raise ModelNotFoundError(
                        f"模型不存在: {url}",
                        status_code=404,
                        response_body=response.text,
                    )
                elif response.status_code == 429:
                    # 速率限制，等待后重试
                    wait_time = (attempt + 1) * self.retry_delay
                    logger.warning(f"触发速率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                elif response.status_code >= 500:
                    # 服务器错误，等待后重试
                    wait_time = (attempt + 1) * self.retry_delay
                    logger.warning(
                        f"服务器错误 ({response.status_code})，等待 {wait_time} 秒后重试..."
                    )
                    time.sleep(wait_time)
                    continue
                elif response.status_code != 200:
                    raise AIGWError(
                        f"请求失败: {response.status_code}",
                        status_code=response.status_code,
                        response_body=response.text,
                    )

                return response

            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = (attempt + 1) * self.retry_delay
                    logger.warning(f"请求异常: {e}，{wait_time} 秒后重试...")
                    time.sleep(wait_time)
                continue

        raise AIGWError(f"请求失败，已重试 {self.max_retries} 次: {last_exception}")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stream: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        发送聊天请求(非流式)

        Args:
            model: 模型名称
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            max_tokens: 最大生成 token 数
            temperature: 温度参数(0.0-1.0)
            stream: 是否使用流式响应
            **kwargs: 其他参数

        Returns:
            API 响应字典

        Raises:
            AIGWError: 请求失败时抛出

        使用示例:
            response = client.chat(
                model="claude-opus-4-6",
                messages=[
                    {"role": "system", "content": "你是一个有用的助手"},
                    {"role": "user", "content": "你好，请介绍一下自己"}
                ],
                max_tokens=1000,
                temperature=0.7
            )
        """
        # 构建请求体
        body = {"model": model, "messages": messages}

        # 可选参数
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if temperature is not None:
            body["temperature"] = temperature
        if stream:
            body["stream"] = True

        # 添加其他参数
        body.update(kwargs)

        logger.info(f"发送请求到模型: {model}")

        # 发送请求
        response = self._make_request(
            method="POST", url=self.chat_completions_url, json=body
        )

        return response.json()

    def chat_stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        发送聊天请求(流式)

        Args:
            model: 模型名称
            messages: 消息列表
            max_tokens: 最大生成 token 数
            temperature: 温度参数
            **kwargs: 其他参数

        Yields:
            每个响应片段的字典

        使用示例:
            for chunk in client.chat_stream(
                model="claude-sonnet-4-6",
                messages=[{"role": "user", "content": "讲个故事"}]
            ):
                if chunk.get("choices"):
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    print(content, end="", flush=True)
        """
        # 构建请求体
        body = {"model": model, "messages": messages, "stream": True}

        # 可选参数
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if temperature is not None:
            body["temperature"] = temperature

        # 添加其他参数
        body.update(kwargs)

        logger.info(f"发送流式请求到模型: {model}")

        # 发送请求
        response = self._make_request(
            method="POST", url=self.chat_completions_url, json=body, stream=True
        )

        # 解析 SSE 流
        for line in response.iter_lines(decode_unicode=True):
            if line:
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        yield chunk
                    except json.JSONDecodeError:
                        logger.warning(f"无法解析 SSE 数据: {data}")

    def get_models(self) -> Dict[str, Any]:
        """
        获取可用模型列表

        Returns:
            模型列表响应

        使用示例:
            models = client.get_models()
            for model in models.get("data", []):
                print(model["id"])
        """
        response = self._make_request(method="GET", url=self.models_url)
        return response.json()

    def list_supported_models(self) -> List[ModelInfo]:
        """
        获取支持的模型列表(本地缓存)

        Returns:
            ModelInfo 列表

        使用示例:
            models = client.list_supported_models()
            for model in models:
                print(f"{model.name}: {model.description}")
        """
        return list(SUPPORTED_MODELS.values())

    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        """
        获取特定模型信息

        Args:
            model_name: 模型名称

        Returns:
            ModelInfo 或 None

        使用示例:
            info = client.get_model_info("claude-opus-4-6")
            if info:
                print(f"模型: {info.name}")
                print(f"描述: {info.description}")
                print(f"上下文长度: {info.context_length}")
        """
        return SUPPORTED_MODELS.get(model_name)

    def estimate_cost(
        self, model: str, input_tokens: int, output_tokens: int
    ) -> Dict[str, Any]:
        """
        估算请求成本(基于 AIGW 定价)

        Args:
            model: 模型名称
            input_tokens: 输入 token 数
            output_tokens: 输出 token 数

        Returns:
            成本估算字典

        Note:
            实际价格请参考 AIGW 官网定价页面
        """
        # 定价(示例，实际价格请以官网为准)
        pricing = {
            "claude-opus-4-6": {"input": 30.0, "output": 150.0},  # 元/百万 token
            "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
            "claude-haiku-4-6": {"input": 0.25, "output": 1.25},
            "deepseek-chat": {"input": 1.0, "output": 2.0},
            "deepseek-reasoner": {"input": 8.0, "output": 16.0},
        }

        model_pricing = pricing.get(model, {"input": 10.0, "output": 50.0})

        input_cost = (input_tokens / 1_000_000) * model_pricing["input"]
        output_cost = (output_tokens / 1_000_000) * model_pricing["output"]
        total_cost = input_cost + output_cost

        return {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6),
            "currency": "CNY",
            "unit": "元",
        }

    def chat_with_context(
        self,
        model: str,
        context: List[Dict[str, str]],
        user_message: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        带上下文的对话(简化版)

        Args:
            model: 模型名称
            context: 历史消息列表
            user_message: 用户新消息
            system_prompt: 系统提示(可选)
            **kwargs: 其他参数

        Returns:
            API 响应

        使用示例:
            history = [
                {"role": "user", "content": "我叫小明"},
                {"role": "assistant", "content": "你好小明！"}
            ]
            response = client.chat_with_context(
                model="claude-sonnet-4-6",
                context=history,
                user_message="我叫什么名字？"
            )
        """
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(context)
        messages.append({"role": "user", "content": user_message})

        return self.chat(model=model, messages=messages, **kwargs)


def create_client_from_env(prefix: str = "NETEASE_AIGW_") -> NeteaseAIGWClient:
    """
    从环境变量创建客户端

    环境变量:
        {prefix}APP_ID: APP ID
        {prefix}APP_KEY: APP Key
        {prefix}BASE_URL: API 基础 URL(可选，默认 https://aigw.netease.com)
        {prefix}AUTH_TOKEN: Auth Token(可选)
        {prefix}APP_CODE: APP Code(可选)

    Returns:
        NeteaseAIGWClient 实例

    使用示例:
        import os
        os.environ["NETEASE_AIGW_APP_ID"] = "your_app_id"
        os.environ["NETEASE_AIGW_APP_KEY"] = "your_app_key"

        client = create_client_from_env()
    """
    import os

    app_id = os.getenv(f"{prefix}APP_ID")
    app_key = os.getenv(f"{prefix}APP_KEY")
    base_url = os.getenv(f"{prefix}BASE_URL", "https://aigw.netease.com")
    auth_token = os.getenv(f"{prefix}AUTH_TOKEN")
    app_code = os.getenv(f"{prefix}APP_CODE")

    return NeteaseAIGWClient(
        app_id=app_id,
        app_key=app_key,
        base_url=base_url,
        auth_token=auth_token,
        app_code=app_code,
    )


# CLI 入口点
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="网易 AIGW API 客户端")
    parser.add_argument("--app-id", required=True, help="APP ID")
    parser.add_argument("--app-key", required=True, help="APP Key")
    parser.add_argument("--model", default="claude-opus-4-6", help="模型名称")
    parser.add_argument("--message", default="你好", help="消息内容")
    parser.add_argument("--stream", action="store_true", help="使用流式输出")

    args = parser.parse_args()

    # 创建客户端
    client = NeteaseAIGWClient(app_id=args.app_id, app_key=args.app_key)

    print(f"使用模型: {args.model}")
    print("-" * 50)

    if args.stream:
        print("回复: ", end="", flush=True)
        for chunk in client.chat_stream(
            model=args.model,
            messages=[{"role": "user", "content": args.message}],
            max_tokens=500,
        ):
            if chunk.get("choices"):
                delta = chunk["choices"][0].get("delta", {})
                content = delta.get("content", "")
                print(content, end="", flush=True)
        print()
    else:
        response = client.chat(
            model=args.model,
            messages=[{"role": "user", "content": args.message}],
            max_tokens=500,
        )
        print("回复:", response["choices"][0]["message"]["content"])
