from fastapi import APIRouter

from app.api.v1.api import api_router as api_v1_router

api_router = APIRouter()

# 注册v1版本API路由
api_router.include_router(api_v1_router, prefix="/v1") 