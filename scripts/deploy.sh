#!/bin/bash

# MyAPI 自动部署脚本
# 用于在服务器上部署 MyAPI 服务

set -e

# 配置变量
REGISTRY="registry.cn-shanghai.aliyuncs.com"
NAMESPACE="docker_for_chengq"
PROJECT="myapi"
IMAGE_NAME="${REGISTRY}/${NAMESPACE}/${PROJECT}"
TAG=${1:-main}
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "🚀 开始部署 MyAPI..."
echo "📦 镜像: ${FULL_IMAGE_NAME}"

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 登录到阿里云容器镜像服务
echo "🔐 登录到阿里云容器镜像服务..."
if [ -z "$ALIYUN_USERNAME" ] || [ -z "$ALIYUN_PASSWORD" ]; then
    echo "❌ 请设置环境变量 ALIYUN_USERNAME 和 ALIYUN_PASSWORD"
    echo "示例: export ALIYUN_USERNAME=your_username"
    echo "示例: export ALIYUN_PASSWORD=your_password"
    exit 1
fi

echo "$ALIYUN_PASSWORD" | docker login $REGISTRY -u $ALIYUN_USERNAME --password-stdin

# 停止并删除旧容器
echo "🛑 停止旧容器..."
docker-compose down || true

# 清理旧镜像
echo "🧹 清理旧镜像..."
docker system prune -f

# 拉取最新镜像
echo "📥 拉取最新镜像..."
docker pull $FULL_IMAGE_NAME

# 创建docker-compose.yml文件
echo "📝 创建docker-compose.yml..."
cat > docker-compose.yml << EOF
version: '3.8'

services:
  myapi:
    image: $FULL_IMAGE_NAME
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

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo "✅ MyAPI部署成功！"
    echo "🌐 服务地址: http://localhost:5201"
    echo "📚 API文档: http://localhost:5201/docs"
    echo "📦 镜像来源: 阿里云容器镜像服务"
else
    echo "❌ 服务启动失败"
    docker-compose logs
    exit 1
fi 