from fastapi import APIRouter

from app.api.v1.endpoints import wechat

api_router = APIRouter()

# 注册微信公众号相关路由
api_router.include_router(wechat.router, tags=["wechat"]) 