# ========================================
# 用户路由
# ========================================
"""
用户API接口

提供用户注册、登录、信息查询等RESTful API
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import (
    AuthenticationException,
    BaseException,
    ErrorCode,
    ParameterException,
    UserException,
)
from app.schemas import (
    ResponseModel,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


@router.post(
    "/register",
    response_model=ResponseModel,
    summary="用户注册",
    description="创建新用户账号",
)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> ResponseModel:
    """
    用户注册接口

    Args:
        user_data: 注册数据
        db: 数据库会话

    Returns:
        ResponseModel: 统一响应格式

    Raises:
        ParameterException: 参数验证失败
        UserException: 用户已存在
    """
    service = UserService(db)

    try:
        user = service.register(user_data)

        return ResponseModel(
            code=ErrorCode.SUCCESS.value,
            msg="注册成功",
            data={"id": user.id, "username": user.username, "email": user.email},
        )
    except UserException as e:
        return ResponseModel(code=e.code, msg=e.message, data=None)


@router.post(
    "/login",
    response_model=ResponseModel,
    summary="用户登录",
    description="用户登录并获取访问令牌",
)
def login(login_data: UserLogin, db: Session = Depends(get_db)) -> ResponseModel:
    """
    用户登录接口

    Args:
        login_data: 登录数据
        db: 数据库会话

    Returns:
        ResponseModel: 包含用户信息和token

    Raises:
        AuthenticationException: 认证失败
    """
    service = UserService(db)

    try:
        result = service.login(login_data)
        user = result["user"]

        return ResponseModel(
            code=ErrorCode.SUCCESS.value,
            msg="登录成功",
            data={
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "nickname": user.nickname,
                    "is_active": user.is_active,
                },
                "message": result["message"],
            },
        )
    except (UserException, AuthenticationException) as e:
        return ResponseModel(code=e.code, msg=e.message, data=None)


@router.get(
    "/{user_id}",
    response_model=ResponseModel,
    summary="获取用户信息",
    description="根据用户ID获取用户详细信息",
)
def get_user(user_id: int, db: Session = Depends(get_db)) -> ResponseModel:
    """
    获取用户信息接口

    Args:
        user_id: 用户ID
        db: 数据库会话

    Returns:
        ResponseModel: 用户信息
    """
    service = UserService(db)

    try:
        user = service.get_user_by_id(user_id)

        return ResponseModel(
            code=ErrorCode.SUCCESS.value,
            msg="获取成功",
            data=UserResponse.model_validate(user).model_dump(),
        )
    except UserException as e:
        return ResponseModel(code=e.code, msg=e.message, data=None)


@router.put(
    "/{user_id}",
    response_model=ResponseModel,
    summary="更新用户信息",
    description="更新用户的邮箱、手机号等非敏感信息",
)
def update_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)
) -> ResponseModel:
    """
    更新用户信息接口

    Args:
        user_id: 用户ID
        user_data: 更新数据
        db: 数据库会话

    Returns:
        ResponseModel: 更新后的用户信息
    """
    service = UserService(db)

    try:
        user = service.update_user(user_id, user_data)

        return ResponseModel(
            code=ErrorCode.SUCCESS.value,
            msg="更新成功",
            data=UserResponse.model_validate(user).model_dump(),
        )
    except UserException as e:
        return ResponseModel(code=e.code, msg=e.message, data=None)


@router.post(
    "/{user_id}/deactivate",
    response_model=ResponseModel,
    summary="禁用用户",
    description="禁用指定用户账号",
)
def deactivate_user(user_id: int, db: Session = Depends(get_db)) -> ResponseModel:
    """
    禁用用户接口

    Args:
        user_id: 用户ID
        db: 数据库会话

    Returns:
        ResponseModel: 操作结果
    """
    service = UserService(db)

    try:
        user = service.deactivate_user(user_id)

        return ResponseModel(
            code=ErrorCode.SUCCESS.value,
            msg="用户已禁用",
            data={"id": user.id, "is_active": user.is_active},
        )
    except UserException as e:
        return ResponseModel(code=e.code, msg=e.message, data=None)


@router.post(
    "/{user_id}/activate",
    response_model=ResponseModel,
    summary="启用用户",
    description="启用指定用户账号",
)
def activate_user(user_id: int, db: Session = Depends(get_db)) -> ResponseModel:
    """
    启用用户接口

    Args:
        user_id: 用户ID
        db: 数据库会话

    Returns:
        ResponseModel: 操作结果
    """
    service = UserService(db)

    try:
        user = service.activate_user(user_id)

        return ResponseModel(
            code=ErrorCode.SUCCESS.value,
            msg="用户已启用",
            data={"id": user.id, "is_active": user.is_active},
        )
    except UserException as e:
        return ResponseModel(code=e.code, msg=e.message, data=None)


@router.get(
    "/check/username/{username}",
    response_model=ResponseModel,
    summary="检查用户名",
    description="检查用户名是否已被注册",
)
def check_username(username: str, db: Session = Depends(get_db)) -> ResponseModel:
    """
    检查用户名是否可用

    Args:
        username: 用户名
        db: 数据库会话

    Returns:
        ResponseModel: 检查结果
    """
    service = UserService(db)
    exists = service.check_username_exists(username)

    return ResponseModel(
        code=ErrorCode.SUCCESS.value,
        msg="查询成功",
        data={"exists": exists, "username": username},
    )


@router.get(
    "/check/email/{email}",
    response_model=ResponseModel,
    summary="检查邮箱",
    description="检查邮箱是否已被注册",
)
def check_email(email: str, db: Session = Depends(get_db)) -> ResponseModel:
    """
    检查邮箱是否可用

    Args:
        email: 邮箱
        db: 数据库会话

    Returns:
        ResponseModel: 检查结果
    """
    service = UserService(db)
    exists = service.check_email_exists(email)

    return ResponseModel(
        code=ErrorCode.SUCCESS.value,
        msg="查询成功",
        data={"exists": exists, "email": email},
    )
