from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
import os
import hashlib
from pathlib import Path

app = FastAPI()

# CORS（可根据实际域名进行调整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
}

STATIC_IMG_DIR = Path("static/images")
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)
BASE_IMAGE_URL = "https://yourdomain.com/static/images/"

def is_valid_wechat_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("mp.weixin.qq.com")

def fetch_wechat_article_html(url: str):
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    title_tag = soup.find('meta', property='og:title')
    title = title_tag['content'] if title_tag else soup.title.string

    content_div = soup.find("div", class_="rich_media_content") or soup.find("div", id="js_content")
    content_html = str(content_div) if content_div else ''

    cover_tag = soup.find('meta', property='og:image')
    cover = cover_tag['content'] if cover_tag else ''

    return title.strip(), content_html, cover

def download_and_replace_images(html: str):
    soup = BeautifulSoup(html, "html.parser")
    for img in soup.find_all("img"):
        src = img.get("data-src") or img.get("src")
        if not src or not src.startswith("http"):
            continue

        ext = os.path.splitext(urlparse(src).path)[-1] or ".jpg"
        filename = hashlib.md5(src.encode("utf-8")).hexdigest() + ext
        local_path = STATIC_IMG_DIR / filename
        new_url = BASE_IMAGE_URL + filename

        try:
            if not local_path.exists():
                r = requests.get(src, headers=headers, timeout=10)
                with open(local_path, "wb") as f:
                    f.write(r.content)
            img["src"] = new_url
        except Exception as e:
            print(f"图片下载失败: {src} - {e}")
            continue

    return str(soup)

@app.get("/api/wechat")
def get_wechat_article(url: str = Query(..., description="微信公众号文章链接")):
    if not is_valid_wechat_url(url):
        return JSONResponse(status_code=400, content={"error": "只允许抓取微信公众号文章"})

    try:
        title, content_html, cover = fetch_wechat_article_html(url)
        return {
            "title": title,
            "content": content_html,
            "cover": cover
        }
    except RequestException as e:
        return JSONResponse(status_code=502, content={"error": f"网络请求失败: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"服务内部错误: {str(e)}"})

@app.get("/api/wechat_markdown", response_class=Response)
def get_wechat_article_markdown(url: str = Query(..., description="微信公众号文章链接")):
    if not is_valid_wechat_url(url):
        return Response(content="错误：只允许抓取微信公众号文章", status_code=400, media_type="text/plain")

    try:
        title, content_html, _ = fetch_wechat_article_html(url)
        html_with_local_images = download_and_replace_images(content_html)
        content_md = md(
            html_with_local_images,
            heading_style="ATX",
            bullets="*",
            strip=["script", "style"]
        )
        full_md = f"# {title}\n\n{content_md}"
        return Response(content=full_md, media_type="text/markdown")

    except RequestException as e:
        return Response(content=f"网络请求失败: {str(e)}", media_type="text/plain", status_code=502)
    except Exception as e:
        return Response(content=f"服务内部错误: {str(e)}", media_type="text/plain", status_code=500)
