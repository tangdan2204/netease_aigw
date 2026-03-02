# ========================================
# 配置加载器
# ========================================
"""
配置管理模块

从config.yaml加载配置，支持环境变量覆盖
"""

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    """数据库配置"""

    host: str = "localhost"
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"
    name: str = "ecommerce"
    pool_size: int = 5
    max_overflow: int = 10
    echo: bool = False

    @property
    def url(self) -> str:
        """获取数据库连接URL"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppConfig(BaseModel):
    """应用配置"""

    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = True
    title: str = "电商用户服务 API"
    version: str = "1.0.0"


class JWTConfig(BaseModel):
    """JWT配置"""

    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class SecurityConfig(BaseModel):
    """安全配置"""

    bcrypt_rounds: int = 12


class ErrorCodesConfig(BaseModel):
    """异常码配置"""

    SUCCESS: int = 0
    PARAM_INVALID: int = 1001
    PARAM_MISSING: int = 1002
    PARAM_FORMAT_ERROR: int = 1003
    USER_NOT_FOUND: int = 2001
    USER_EXISTS: int = 2002
    USER_DISABLED: int = 2003
    USER_UNAUTHORIZED: int = 2004
    PASSWORD_WRONG: int = 3001
    TOKEN_INVALID: int = 3002
    TOKEN_EXPIRED: int = 3003
    DB_ERROR: int = 4001
    DB_CONNECTION_FAILED: int = 4002
    PERMISSION_DENIED: int = 5001


class Config(BaseModel):
    """全局配置"""

    database: DatabaseConfig = DatabaseConfig()
    app: AppConfig = AppConfig()
    jwt: JWTConfig = JWTConfig()
    security: SecurityConfig = SecurityConfig()
    error_codes: ErrorCodesConfig = ErrorCodesConfig()


def load_config(config_path: str | None = None) -> Config:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径，默认为项目根目录的config.yaml

    Returns:
        Config对象

    Raises:
        FileNotFoundError: 配置文件不存在
        ValueError: 配置文件格式错误
    """
    if config_path is None:
        # 默认从项目根目录加载
        config_path = Path(__file__).parent.parent / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)

    if config_dict is None:
        raise ValueError("配置文件为空")

    # 环境变量覆盖
    config_dict = _apply_env_overrides(config_dict)

    return Config(**config_dict)


def _apply_env_overrides(config_dict: dict[str, Any]) -> dict[str, Any]:
    """
    应用环境变量覆盖

    支持的环境变量：
    - DATABASE_HOST: 数据库主机
    - DATABASE_PORT: 数据库端口
    - DATABASE_USERNAME: 数据库用户名
    - DATABASE_PASSWORD: 数据库密码
    - DATABASE_NAME: 数据库名称
    - JWT_SECRET_KEY: JWT密钥
    - APP_DEBUG: 调试模式
    """
    env_mappings = {
        "DATABASE_HOST": ("database", "host"),
        "DATABASE_PORT": ("database", "port"),
        "DATABASE_USERNAME": ("database", "username"),
        "DATABASE_PASSWORD": ("database", "password"),
        "DATABASE_NAME": ("database", "name"),
        "JWT_SECRET_KEY": ("jwt", "secret_key"),
    }

    for env_key, path in env_mappings.items():
        env_value = os.environ.get(env_key)
        if env_value is not None:
            section, key = path
            if section not in config_dict:
                config_dict[section] = {}
            # 类型转换
            if key == "port":
                env_value = int(env_value)
            config_dict[section][key] = env_value

    return config_dict


# 全局配置实例
_config: Config | None = None


def get_config() -> Config:
    """
    获取全局配置实例（单例模式）

    Returns:
        Config对象
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config
