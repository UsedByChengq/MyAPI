from fastapi import HTTPException
from typing import Any, Dict, Optional


class WeChatScraperException(HTTPException):
    """微信公众号抓取器基础异常"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class InvalidURLException(WeChatScraperException):
    """无效URL异常"""
    
    def __init__(self, detail: str = "无效的URL"):
        super().__init__(status_code=400, detail=detail)


class NetworkRequestException(WeChatScraperException):
    """网络请求异常"""
    
    def __init__(self, detail: str = "网络请求失败"):
        super().__init__(status_code=502, detail=detail)


class ContentParseException(WeChatScraperException):
    """内容解析异常"""
    
    def __init__(self, detail: str = "内容解析失败"):
        super().__init__(status_code=500, detail=detail)


class ImageDownloadException(WeChatScraperException):
    """图片下载异常"""
    
    def __init__(self, detail: str = "图片下载失败"):
        super().__init__(status_code=500, detail=detail) 