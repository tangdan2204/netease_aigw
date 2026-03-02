# ========================================
# FastAPI应用入口
# ========================================
"""
主应用文件

电商用户服务入口，配置路由、中间件、异常处理等
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import get_config
from app.database import init_db
from app.exceptions import (
    BaseException,
    ErrorCode,
    get_error_message,
)
from app.routers import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    启动时初始化数据库，关闭时清理资源
    """
    # 启动时执行
    config = get_config()
    print(f"🚀 启动电商用户服务 v{config.app.version}")
    print(f"📡 服务地址: http://{config.app.host}:{config.app.port}")

    # 初始化数据库表
    init_db()
    print("✅ 数据库表初始化完成")

    yield

    # 关闭时执行
    print("👋 正在关闭服务...")


def create_app() -> FastAPI:
    """
    创建FastAPI应用

    Returns:
        FastAPI: 配置好的应用实例
    """
    config = get_config()

    app = FastAPI(
        title=config.app.title,
        version=config.app.version,
        description="电商系统用户模块，提供用户注册、登录、信息查询等功能",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 注册路由
    app.include_router(user_router)

    # 根路由
    @app.get("/", tags=["健康检查"])
    async def root():
        """健康检查接口"""
        return {
            "service": config.app.title,
            "version": config.app.version,
            "status": "running",
        }

    # 全局异常处理
    @app.exception_handler(BaseException)
    async def base_exception_handler(request: Request, exc: BaseException):
        """业务异常处理器"""
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": exc.code, "msg": exc.message, "data": exc.details},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """参数验证异常处理器"""
        errors = exc.errors()
        error_messages = []

        for error in errors:
            loc = " -> ".join(str(l) for l in error["loc"])
            error_messages.append(f"{loc}: {error['msg']}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": ErrorCode.PARAM_INVALID.value,
                "msg": "参数验证失败",
                "data": {"errors": error_messages},
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """通用异常处理器"""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": ErrorCode.DB_ERROR.value,
                "msg": "服务器内部错误",
                "data": None,
            },
        )

    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    config = get_config()
    uvicorn.run(
        "app.main:app",
        host=config.app.host,
        port=config.app.port,
        reload=config.app.debug,
    )
