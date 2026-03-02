# ========================================
# 数据库连接管理
# ========================================
"""
数据库连接和会话管理

提供数据库引擎创建、会话工厂、依赖注入
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from app.config import get_config

# 创建 declarative base
Base = declarative_base()

# 引擎实例
_engine = None
_SessionLocal = None


def get_engine():
    """
    获取数据库引擎

    Returns:
        SQLAlchemy Engine
    """
    global _engine
    if _engine is None:
        config = get_config()
        _engine = create_engine(
            config.database.url,
            pool_size=config.database.pool_size,
            max_overflow=config.database.max_overflow,
            echo=config.database.echo,
            pool_pre_ping=True,  # 连接前检查连接有效性
        )
    return _engine


def get_session_factory():
    """
    获取会话工厂

    Returns:
        sessionmaker
    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    数据库会话依赖注入

    Usage:
        @router.get("/")
        async def endpoint(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: 数据库会话
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    上下文管理器方式的数据库会话

    Usage:
        with get_db_session() as db:
            db.add(user)
            db.commit()

    Yields:
        Session: 数据库会话
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    初始化数据库表

    创建所有继承Base的模型对应的表
    """
    from app.models.user import User  # 导入User模型以注册

    Base.metadata.create_all(bind=get_engine())


def drop_db():
    """
    删除所有数据库表

    WARNING: 此操作会删除所有数据，请谨慎使用
    """
    Base.metadata.drop_all(bind=get_engine())
