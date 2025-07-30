import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


class TestWeChatAPI:
    """微信公众号API测试类"""
    
    def test_get_wechat_article_invalid_url(self, client: TestClient):
        """测试无效URL的API调用"""
        response = client.get("/api/v1/wechat", params={"url": "https://example.com/article"})
        assert response.status_code == 400
        assert "只允许抓取微信公众号文章" in response.json()["detail"]
    
    def test_get_wechat_article_missing_url(self, client: TestClient):
        """测试缺少URL参数的API调用"""
        response = client.get("/api/v1/wechat")
        assert response.status_code == 422  # 验证错误
    
    @patch('app.services.wechat_service.wechat_service.get_article_data')
    def test_get_wechat_article_success(self, mock_get_data, client: TestClient):
        """测试成功获取文章"""
        mock_data = {
            "title": "测试文章",
            "content": "<p>文章内容</p>",
            "cover": "https://example.com/cover.jpg"
        }
        mock_get_data.return_value = mock_data
        
        response = client.get("/api/v1/wechat", params={"url": "https://mp.weixin.qq.com/s/example"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试文章"
        assert data["content"] == "<p>文章内容</p>"
        assert data["cover"] == "https://example.com/cover.jpg"
    
    @patch('app.services.wechat_service.wechat_service.get_article_markdown')
    def test_get_wechat_article_markdown_success(self, mock_get_markdown, client: TestClient):
        """测试成功获取Markdown格式文章"""
        mock_markdown = "# 测试文章\n\n这是文章内容"
        mock_get_markdown.return_value = mock_markdown
        
        response = client.get("/api/v1/wechat/markdown", params={"url": "https://mp.weixin.qq.com/s/example"})
        
        assert response.status_code == 200
        assert "text/markdown" in response.headers["content-type"]
        assert "# 测试文章" in response.text
    
    def test_api_docs_available(self, client: TestClient):
        """测试API文档是否可用"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200 