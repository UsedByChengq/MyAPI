import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)


@pytest.fixture
def sample_wechat_url():
    """示例微信公众号文章URL"""
    return "https://mp.weixin.qq.com/s/example" 