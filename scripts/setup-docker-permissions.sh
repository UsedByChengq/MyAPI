#!/bin/bash

# Docker 权限配置脚本
# 用于配置普通用户使用Docker时不需要sudo

set -e

echo "🔧 配置Docker权限..."

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo "❌ 请不要使用root用户运行此脚本"
    exit 1
fi

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker服务状态
if ! sudo systemctl is-active --quiet docker; then
    echo "⚠️ Docker服务未运行，正在启动..."
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# 创建docker组（如果不存在）
if ! getent group docker > /dev/null 2>&1; then
    echo "📝 创建docker组..."
    sudo groupadd docker
fi

# 将用户添加到docker组
echo "👤 将用户添加到docker组..."
sudo usermod -aG docker $USER

# 修改Docker socket权限
echo "🔐 修改Docker socket权限..."
sudo chmod 666 /var/run/docker.sock

# 重新加载组权限
echo "🔄 重新加载组权限..."
newgrp docker

# 验证配置
echo "✅ 验证配置..."
if docker info > /dev/null 2>&1; then
    echo "🎉 Docker权限配置成功！"
    echo ""
    echo "📋 用户信息："
    groups $USER
    echo ""
    echo "🔍 Docker信息："
    docker --version
    echo ""
    echo "💡 提示：如果仍有问题，请重新登录服务器"
else
    echo "❌ Docker权限配置失败"
    echo "🔍 请检查以下内容："
    echo "1. Docker服务是否正常运行"
    echo "2. 用户是否已添加到docker组"
    echo "3. Docker socket权限是否正确"
    exit 1
fi 