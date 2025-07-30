#!/usr/bin/env python3
"""
微信公众号文章抓取API服务启动脚本
"""

import uvicorn
from app.core.config import settings


def main():
    """启动应用"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5201,
        reload=settings.debug,
        log_level="info"
    )


if __name__ == "__main__":
    main() 