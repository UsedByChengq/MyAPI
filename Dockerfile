# 使用轻量级 Python 镜像
FROM python:3.11-slim

# 安装依赖
RUN pip install --no-cache-dir fastapi uvicorn beautifulsoup4 markdownify requests

# 创建目录
WORKDIR /app
COPY . /app

# 创建图片目录（用于静态资源）
RUN mkdir -p /app/static/images

# 暴露端口
EXPOSE 5201

# 启动 FastAPI 应用（监听端口 5201）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5201"]
