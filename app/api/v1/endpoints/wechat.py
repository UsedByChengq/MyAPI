from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import Response
from typing import Optional

from app.schemas.wechat import WeChatArticleResponse, ErrorResponse
from app.services.wechat_service import wechat_service
from app.core.exceptions import WeChatScraperException

router = APIRouter()


def get_wechat_service():
    """依赖注入：获取微信公众号服务实例"""
    return wechat_service


@router.get(
    "/wechat",
    response_model=WeChatArticleResponse,
    responses={
        400: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="获取微信公众号文章",
    description="抓取微信公众号文章并返回HTML格式的内容"
)
async def get_wechat_article(
    url: str = Query(..., description="微信公众号文章链接"),
    service: wechat_service = Depends(get_wechat_service)
) -> WeChatArticleResponse:
    """
    获取微信公众号文章内容
    
    - **url**: 微信公众号文章的完整URL
    
    返回:
    - **title**: 文章标题
    - **content**: 文章HTML内容
    - **cover**: 文章封面图片URL（可选）
    """
    try:
        result = service.get_article_data(url)
        return WeChatArticleResponse(**result)
    except WeChatScraperException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务内部错误: {str(e)}")


@router.get(
    "/wechat/markdown",
    response_class=Response,
    responses={
        400: {"description": "无效的URL"},
        502: {"description": "网络请求失败"},
        500: {"description": "服务内部错误"}
    },
    summary="获取微信公众号文章（Markdown格式）",
    description="抓取微信公众号文章并返回Markdown格式的内容，同时下载并替换图片为本地URL"
)
async def get_wechat_article_markdown(
    url: str = Query(..., description="微信公众号文章链接"),
    service: wechat_service = Depends(get_wechat_service)
) -> Response:
    """
    获取微信公众号文章内容（Markdown格式）
    
    - **url**: 微信公众号文章的完整URL
    
    返回Markdown格式的文章内容，图片会被下载到本地并替换URL
    """
    try:
        markdown_content = service.get_article_markdown(url)
        return Response(
            content=markdown_content,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=article.md"}
        )
    except WeChatScraperException as e:
        return Response(
            content=f"错误: {e.detail}",
            status_code=e.status_code,
            media_type="text/plain"
        )
    except Exception as e:
        return Response(
            content=f"服务内部错误: {str(e)}",
            status_code=500,
            media_type="text/plain"
        ) 