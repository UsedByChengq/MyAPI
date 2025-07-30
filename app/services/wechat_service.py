from typing import Tuple, Optional
from urllib.parse import urlparse
import hashlib
import os
from pathlib import Path
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from app.core.config import settings
from app.core.exceptions import (
    InvalidURLException,
    NetworkRequestException,
    ContentParseException,
    ImageDownloadException
)


class WeChatService:
    """微信公众号文章抓取服务"""
    
    def __init__(self):
        self.headers = {"User-Agent": settings.user_agent}
        self.static_img_dir = Path(settings.static_img_dir)
        self.static_img_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_url(self, url: str) -> bool:
        """验证URL是否为有效的微信公众号文章链接"""
        try:
            parsed = urlparse(url)
            return any(domain in parsed.netloc for domain in settings.allowed_domains)
        except Exception:
            return False
    
    def fetch_article_html(self, url: str) -> Tuple[str, str, Optional[str]]:
        """获取微信公众号文章HTML内容"""
        if not self.validate_url(url):
            raise InvalidURLException("只允许抓取微信公众号文章")
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=settings.request_timeout)
            resp.encoding = 'utf-8'
            resp.raise_for_status()
        except RequestException as e:
            raise NetworkRequestException(f"网络请求失败: {str(e)}")
        
        try:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 提取标题
            title_tag = soup.find('meta', property='og:title')
            title = title_tag['content'] if title_tag else soup.title.string
            if not title:
                title = "无标题"
            
            # 提取内容
            content_div = soup.find("div", class_="rich_media_content") or soup.find("div", id="js_content")
            if not content_div:
                raise ContentParseException("无法找到文章内容")
            content_html = str(content_div)
            
            # 提取封面图
            cover_tag = soup.find('meta', property='og:image')
            cover = cover_tag['content'] if cover_tag else None
            
            return title.strip(), content_html, cover
            
        except Exception as e:
            raise ContentParseException(f"内容解析失败: {str(e)}")
    
    def download_and_replace_images(self, html: str) -> str:
        """下载图片并替换为本地URL"""
        soup = BeautifulSoup(html, "html.parser")
        
        for img in soup.find_all("img"):
            src = img.get("data-src") or img.get("src")
            if not src or not src.startswith("http"):
                continue
            
            try:
                # 生成文件名
                ext = os.path.splitext(urlparse(src).path)[-1] or ".jpg"
                filename = hashlib.md5(src.encode("utf-8")).hexdigest() + ext
                local_path = self.static_img_dir / filename
                new_url = settings.base_image_url + filename
                
                # 下载图片
                if not local_path.exists():
                    r = requests.get(src, headers=self.headers, timeout=settings.request_timeout)
                    r.raise_for_status()
                    with open(local_path, "wb") as f:
                        f.write(r.content)
                
                # 替换图片URL
                img["src"] = new_url
                
            except Exception as e:
                # 图片下载失败时记录日志但不中断流程
                print(f"图片下载失败: {src} - {e}")
                continue
        
        return str(soup)
    
    def convert_to_markdown(self, html: str) -> str:
        """将HTML转换为Markdown格式"""
        try:
            return md(
                html,
                heading_style="ATX",
                bullets="*",
                strip=["script", "style"]
            )
        except Exception as e:
            raise ContentParseException(f"Markdown转换失败: {str(e)}")
    
    def get_article_data(self, url: str) -> dict:
        """获取文章数据（HTML格式）"""
        title, content_html, cover = self.fetch_article_html(url)
        return {
            "title": title,
            "content": content_html,
            "cover": cover
        }
    
    def get_article_markdown(self, url: str) -> str:
        """获取文章数据（Markdown格式）"""
        title, content_html, _ = self.fetch_article_html(url)
        html_with_local_images = self.download_and_replace_images(content_html)
        content_md = self.convert_to_markdown(html_with_local_images)
        return f"# {title}\n\n{content_md}"


# 服务实例
wechat_service = WeChatService() 