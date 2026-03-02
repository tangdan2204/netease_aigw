# ========================================
# 用户服务层
# ========================================
"""
用户业务逻辑

处理用户注册、登录、信息查询等业务逻辑
"""

from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_config
from app.exceptions import (
    AuthenticationException,
    DatabaseException,
    ErrorCode,
    ParameterException,
    UserException,
)
from app.models.user import User
from app.schemas import UserCreate, UserLogin, UserUpdate


# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    用户服务类

    提供用户相关的业务逻辑操作
    """

    def __init__(self, db: Session):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db
        self.config = get_config()

    def _get_bcrypt_rounds(self) -> int:
        """获取bcrypt加密轮数"""
        return self.config.security.bcrypt_rounds

    def hash_password(self, password: str) -> str:
        """
        加密密码

        Args:
            password: 原始密码

        Returns:
            str: 加密后的密码
        """
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码

        Args:
            plain_password: 原始密码
            hashed_password: 加密后的密码

        Returns:
            bool: 密码是否匹配
        """
        return pwd_context.verify(plain_password, hashed_password)

    def register(self, user_data: UserCreate) -> User:
        """
        用户注册

        Args:
            user_data: 用户注册数据

        Returns:
            User: 创建的用户对象

        Raises:
            UserException: 用户已存在
            DatabaseException: 数据库操作失败
        """
        try:
            # 检查用户名是否已存在
            existing_user = (
                self.db.query(User).filter(User.username == user_data.username).first()
            )
            if existing_user:
                raise UserException(
                    message="用户名已存在", details={"field": "username"}
                )

            # 检查邮箱是否已存在
            existing_email = (
                self.db.query(User).filter(User.email == user_data.email).first()
            )
            if existing_email:
                raise UserException(message="邮箱已被注册", details={"field": "email"})

            # 检查手机号是否已存在（如果提供了手机号）
            if user_data.phone:
                existing_phone = (
                    self.db.query(User).filter(User.phone == user_data.phone).first()
                )
                if existing_phone:
                    raise UserException(
                        message="手机号已被注册", details={"field": "phone"}
                    )

            # 创建用户
            user = User(
                username=user_data.username,
                email=user_data.email,
                phone=user_data.phone,
                password_hash=self.hash_password(user_data.password),
                nickname=user_data.username,  # 默认昵称为用户名
            )

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user

        except UserException:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(message="注册失败，请稍后重试", details=str(e))

    def login(self, login_data: UserLogin) -> dict:
        """
        用户登录

        Args:
            login_data: 登录数据

        Returns:
            dict: 包含用户信息和token

        Raises:
            AuthenticationException: 认证失败
            UserException: 用户不存在或被禁用
        """
        try:
            # 根据用户名或邮箱查找用户
            user = (
                self.db.query(User)
                .filter(
                    and_(User.username == login_data.username, User.is_active == True)
                )
                .first()
            )

            if not user:
                # 尝试用邮箱查找
                user = (
                    self.db.query(User)
                    .filter(
                        and_(User.email == login_data.username, User.is_active == True)
                    )
                    .first()
                )

            if not user:
                raise UserException(message="用户不存在", details={"field": "username"})

            if not user.is_active:
                raise UserException(message="用户已被禁用", details={"field": "status"})

            # 验证密码
            if not self.verify_password(login_data.password, user.password_hash):
                raise AuthenticationException(
                    code=ErrorCode.PASSWORD_WRONG, message="密码错误"
                )

            # 更新最后登录时间
            user.updated_at = datetime.utcnow()
            self.db.commit()

            return {"user": user, "message": "登录成功"}

        except (UserException, AuthenticationException):
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(message="登录失败，请稍后重试", details=str(e))

    def get_user_by_id(self, user_id: int) -> User:
        """
        根据ID获取用户

        Args:
            user_id: 用户ID

        Returns:
            User: 用户对象

        Raises:
            UserException: 用户不存在
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise UserException(
                message="用户不存在", details={"field": "id", "value": user_id}
            )

        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        根据用户名获取用户

        Args:
            username: 用户名

        Returns:
            User | None: 用户对象，不存在返回None
        """
        return self.db.query(User).filter(User.username == username).first()

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            user_data: 更新数据

        Returns:
            User: 更新后的用户

        Raises:
            UserException: 用户不存在
            DatabaseException: 数据库操作失败
        """
        try:
            user = self.get_user_by_id(user_id)

            # 更新字段
            update_data = user_data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(user, field, value)

            user.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(user)

            return user

        except UserException:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(message="更新失败，请稍后重试", details=str(e))

    def deactivate_user(self, user_id: int) -> User:
        """
        禁用用户

        Args:
            user_id: 用户ID

        Returns:
            User: 更新后的用户
        """
        user = self.get_user_by_id(user_id)
        user.is_active = False
        user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        return user

    def activate_user(self, user_id: int) -> User:
        """
        启用用户

        Args:
            user_id: 用户ID

        Returns:
            User: 更新后的用户
        """
        user = self.get_user_by_id(user_id)
        user.is_active = True
        user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(user)

        return user

    def check_username_exists(self, username: str) -> bool:
        """
        检查用户名是否存在

        Args:
            username: 用户名

        Returns:
            bool: 是否存在
        """
        return self.db.query(User).filter(User.username == username).first() is not None

    def check_email_exists(self, email: str) -> bool:
        """
        检查邮箱是否存在

        Args:
            email: 邮箱

        Returns:
            bool: 是否存在
        """
        return self.db.query(User).filter(User.email == email).first() is not None
