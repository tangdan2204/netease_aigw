# ========================================
# Pydantic数据模型
# ========================================
"""
数据验证模式

定义请求/响应的数据结构，用于数据验证和序列化
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, field_validator


class ResponseModel(BaseModel):
    """
    统一响应模型

    Attributes:
        code: 状态码，0表示成功
        msg: 消息描述
        data: 响应数据
    """

    code: int = 0
    msg: str = "success"
    data: Any = None

    class Config:
        json_schema_extra = {"example": {"code": 0, "msg": "success", "data": {}}}


class UserBase(BaseModel):
    """用户基础模型"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    phone: str | None = Field(None, description="手机号")


class UserCreate(UserBase):
    """
    用户注册请求

    Attributes:
        password: 密码，最小6位
        confirm_password: 确认密码
    """

    password: str = Field(..., min_length=6, max_length=100, description="密码")
    confirm_password: str = Field(..., description="确认密码")

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """验证两次密码是否一致"""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("两次密码不一致")
        return v


class UserLogin(BaseModel):
    """
    用户登录请求

    Attributes:
        username: 用户名或邮箱
        password: 密码
    """

    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """
    用户信息更新请求

    所有字段都是可选的
    """

    email: EmailStr | None = Field(None, description="邮箱地址")
    phone: str | None = Field(None, description="手机号")
    nickname: str | None = Field(None, min_length=1, max_length=50, description="昵称")
    avatar: str | None = Field(None, description="头像URL")


class UserResponse(BaseModel):
    """
    用户信息响应

    不包含敏感信息
    """

    id: int
    username: str
    email: str
    phone: str | None
    nickname: str | None
    avatar: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """登录响应"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PaginatedResponse(BaseModel):
    """分页响应模型"""

    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
