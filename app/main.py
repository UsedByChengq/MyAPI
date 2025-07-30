from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时的初始化操作
    print(f"启动 {settings.app_name} v{settings.app_version}")
    yield
    # 关闭时的清理操作
    print("应用正在关闭...")


def create_application() -> FastAPI:
    """应用工厂函数"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="MyAPI - 通用API服务",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # 挂载静态文件
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # 注册API路由
    app.include_router(api_router, prefix="/api")
    
    return app


# 创建应用实例
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5201,
        reload=settings.debug
    ) 