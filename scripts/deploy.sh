#!/bin/bash

# MyAPI 部署脚本
# 使用方法: ./deploy.sh [镜像标签]

set -e

# 配置变量
REGISTRY="harbor.5845.cn"
PROJECT="myapi"
IMAGE_NAME="${REGISTRY}/${PROJECT}/myapi"
TAG=${1:-main}
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "🚀 开始部署 MyAPI..."
echo "📦 镜像: ${FULL_IMAGE_NAME}"

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 配置Docker使用不安全的registry（解决TLS证书问题）
echo "🔧 配置Docker registry设置..."
sudo mkdir -p /etc/docker
echo "{\"insecure-registries\": [\"${REGISTRY}\"]}" | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
sleep 5

# 停止并删除旧容器
echo "🛑 停止旧容器..."
docker-compose down || true

# 清理旧镜像
echo "🧹 清理旧镜像..."
docker system prune -f

# 拉取最新镜像
echo "📥 拉取最新镜像..."
docker pull ${FULL_IMAGE_NAME}

# 创建docker-compose.yml文件
echo "📝 创建 docker-compose.yml..."
cat > docker-compose.yml << EOF
version: '3.8'

services:
  myapi:
    image: ${FULL_IMAGE_NAME}
    ports:
      - "5201:5201"
    environment:
      - APP_NAME=MyAPI
      - APP_VERSION=1.0.0
      - DEBUG=false
    volumes:
      - ./static:/app/static
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5201/docs"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# 启动新容器
echo "🚀 启动新容器..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 15

# 检查服务健康状态
echo "🔍 检查服务健康状态..."
if curl -f http://localhost:5201/docs > /dev/null 2>&1; then
    echo "✅ 部署成功！"
    echo "🌐 服务地址: http://localhost:5201"
    echo "📚 API文档: http://localhost:5201/docs"
else
    echo "❌ 部署失败，服务未正常启动"
    docker-compose logs myapi
    exit 1
fi 