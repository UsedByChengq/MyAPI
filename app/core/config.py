from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    app_name: str = "MyAPI"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # CORS配置
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # 静态文件配置
    static_img_dir: str = "static/images"
    base_image_url: str = "https://yourdomain.com/static/images/"
    
    # 网络请求配置
    request_timeout: int = 10
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    
    # 允许的域名
    allowed_domains: List[str] = ["mp.weixin.qq.com"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings() 