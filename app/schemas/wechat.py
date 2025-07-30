from pydantic import BaseModel, HttpUrl, validator
from typing import Optional


class WeChatArticleRequest(BaseModel):
    """微信公众号文章请求模型"""
    url: HttpUrl
    
    @validator('url')
    def validate_wechat_url(cls, v):
        """验证是否为微信公众号URL"""
        url_str = str(v)
        if not any(domain in url_str for domain in ['mp.weixin.qq.com']):
            raise ValueError('只允许抓取微信公众号文章')
        return v


class WeChatArticleResponse(BaseModel):
    """微信公众号文章响应模型"""
    title: str
    content: str
    cover: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "文章标题",
                "content": "<div>文章内容HTML</div>",
                "cover": "https://example.com/cover.jpg"
            }
        }


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "错误信息",
                "detail": "详细错误描述"
            }
        } 