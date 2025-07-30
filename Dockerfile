# 使用轻量级 Python 镜像
FROM python:3.11-slim

# 安装依赖
RUN pip install --no-cache-dir fastapi uvicorn beautifulsoup4 markdownify requests

# 创建目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY pyproject.toml uv.lock README.md ./
COPY app/ ./app/
COPY static/ ./static/
COPY run.py ./

# 安装Python依赖
RUN pip install --no-cache-dir fastapi uvicorn pydantic-settings beautifulsoup4 markdownify requests

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# 创建static/images目录并设置权限
RUN mkdir -p /app/static/images && \
    chown -R app:app /app/static

USER app

# 暴露端口
EXPOSE 5201

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5201/docs || exit 1

# 启动命令
CMD ["python", "run.py"]
