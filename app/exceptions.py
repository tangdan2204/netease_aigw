# ========================================
# 自定义异常类
# ========================================
"""
异常定义模块

定义业务异常和HTTP异常，支持分类捕获
"""

from enum import Enum
from typing import Any


class ErrorCode(Enum):
    """异常码枚举"""

    # 成功
    SUCCESS = 0

    # 参数异常 (1001-1999)
    PARAM_INVALID = 1001
    PARAM_MISSING = 1002
    PARAM_FORMAT_ERROR = 1003

    # 用户异常 (2001-2999)
    USER_NOT_FOUND = 2001
    USER_EXISTS = 2002
    USER_DISABLED = 2003
    USER_UNAUTHORIZED = 2004

    # 认证异常 (3001-3999)
    PASSWORD_WRONG = 3001
    TOKEN_INVALID = 3002
    TOKEN_EXPIRED = 3003

    # 数据库异常 (4001-4999)
    DB_ERROR = 4001
    DB_CONNECTION_FAILED = 4002

    # 权限异常 (5001-5999)
    PERMISSION_DENIED = 5001


class BaseException(Exception):
    """
    基础异常类

    Attributes:
        code: 异常码
        message: 异常消息
        details: 详细信息（可选）
    """

    def __init__(self, code: int | ErrorCode, message: str, details: Any = None):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class ParameterException(BaseException):
    """
    参数异常

    用于参数校验失败的场景
    """

    def __init__(self, message: str = "参数错误", details: Any = None):
        super().__init__(
            code=ErrorCode.PARAM_INVALID.value, message=message, details=details
        )


class UserException(BaseException):
    """
    用户异常

    用于用户相关业务逻辑失败
    """

    def __init__(self, message: str = "用户错误", details: Any = None):
        super().__init__(
            code=ErrorCode.USER_NOT_FOUND.value, message=message, details=details
        )


class AuthenticationException(BaseException):
    """
    认证异常

    用于登录验证、Token验证失败
    """

    def __init__(
        self,
        code: int | ErrorCode = ErrorCode.TOKEN_INVALID,
        message: str = "认证失败",
        details: Any = None,
    ):
        super().__init__(
            code=code.value if isinstance(code, ErrorCode) else code,
            message=message,
            details=details,
        )


class DatabaseException(BaseException):
    """
    数据库异常

    用于数据库操作失败的场景
    """

    def __init__(self, message: str = "数据库错误", details: Any = None):
        super().__init__(
            code=ErrorCode.DB_ERROR.value, message=message, details=details
        )


class PermissionException(BaseException):
    """
    权限异常

    用于权限验证失败的场景
    """

    def __init__(self, message: str = "权限不足", details: Any = None):
        super().__init__(
            code=ErrorCode.PERMISSION_DENIED.value, message=message, details=details
        )


def get_error_message(code: int) -> str:
    """
    根据异常码获取默认错误消息

    Args:
        code: 异常码

    Returns:
        错误消息
    """
    error_messages = {
        0: "成功",
        1001: "参数无效",
        1002: "缺少必要参数",
        1003: "参数格式错误",
        2001: "用户不存在",
        2002: "用户已存在",
        2003: "用户已被禁用",
        2004: "用户未登录",
        3001: "密码错误",
        3002: "Token无效",
        3003: "Token已过期",
        4001: "数据库操作失败",
        4002: "数据库连接失败",
        5001: "权限不足",
    }
    return error_messages.get(code, "未知错误")
