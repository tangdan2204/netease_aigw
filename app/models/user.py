# ========================================
# User数据模型
# ========================================
"""
用户模型定义

包含用户实体结构和关联关系
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)

from app.database import Base


class User(Base):
    """
    用户模型

    Attributes:
        id: 主键ID
        username: 用户名，唯一
        email: 邮箱，唯一
        phone: 手机号，可为空
        password_hash: 加密后的密码
        nickname: 昵称，可为空
        avatar: 头像URL，可为空
        is_active: 是否激活
        is_admin: 是否管理员
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "users"

    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")

    # 基本信息
    username = Column(
        String(50), unique=True, index=True, nullable=False, comment="用户名"
    )
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    password_hash = Column(String(255), nullable=False, comment="加密后的密码")

    # 扩展信息
    nickname = Column(String(50), nullable=True, comment="昵称")
    avatar = Column(Text, nullable=True, comment="头像URL")

    # 状态标记
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_admin = Column(Boolean, default=False, comment="是否管理员")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"

    @property
    def to_dict(self) -> dict:
        """
        转换为字典（排除敏感信息）

        Returns:
            dict: 用户信息字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
