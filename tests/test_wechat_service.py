import pytest
from unittest.mock import Mock, patch
from app.services.wechat_service import WeChatService
from app.core.exceptions import InvalidURLException, NetworkRequestException


class TestWeChatService:
    """微信公众号服务测试类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.service = WeChatService()
    
    def test_validate_url_valid(self):
        """测试有效URL验证"""
        valid_url = "https://mp.weixin.qq.com/s/example"
        assert self.service.validate_url(valid_url) is True
    
    def test_validate_url_invalid(self):
        """测试无效URL验证"""
        invalid_urls = [
            "https://example.com/article",
            "https://weibo.com/status/123",
            "not_a_url"
        ]
        for url in invalid_urls:
            assert self.service.validate_url(url) is False
    
    @patch('requests.get')
    def test_fetch_article_html_success(self, mock_get):
        """测试成功获取文章HTML"""
        # 模拟响应
        mock_response = Mock()
        mock_response.text = """
        <html>
            <head>
                <title>测试文章</title>
                <meta property="og:title" content="测试文章标题">
                <meta property="og:image" content="https://example.com/cover.jpg">
            </head>
            <body>
                <div class="rich_media_content">
                    <p>文章内容</p>
                </div>
            </body>
        </html>
        """
        mock_response.encoding = 'utf-8'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        title, content, cover = self.service.fetch_article_html("https://mp.weixin.qq.com/s/example")
        
        assert title == "测试文章标题"
        assert "文章内容" in content
        assert cover == "https://example.com/cover.jpg"
    
    def test_fetch_article_html_invalid_url(self):
        """测试无效URL获取文章"""
        with pytest.raises(InvalidURLException):
            self.service.fetch_article_html("https://example.com/article")
    
    @patch('requests.get')
    def test_fetch_article_html_network_error(self, mock_get):
        """测试网络错误"""
        mock_get.side_effect = Exception("网络错误")
        
        with pytest.raises(NetworkRequestException):
            self.service.fetch_article_html("https://mp.weixin.qq.com/s/example")
    
    def test_convert_to_markdown(self):
        """测试HTML转Markdown"""
        html = "<h1>标题</h1><p>段落内容</p>"
        markdown = self.service.convert_to_markdown(html)
        
        assert "# 标题" in markdown
        assert "段落内容" in markdown 