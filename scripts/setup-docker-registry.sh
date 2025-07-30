#!/bin/bash

# Docker Registry 配置脚本
# 用于配置Docker使用不安全的Harbor registry

set -e

REGISTRY="harbor.5845.cn"

echo "🔧 配置Docker使用不安全的registry: ${REGISTRY}"

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用sudo运行此脚本"
    exit 1
fi

# 备份现有配置
if [ -f /etc/docker/daemon.json ]; then
    echo "📋 备份现有Docker配置..."
    cp /etc/docker/daemon.json /etc/docker/daemon.json.backup.$(date +%Y%m%d_%H%M%S)
fi

# 创建Docker配置目录
mkdir -p /etc/docker

# 配置insecure-registries
echo "📝 配置insecure-registries..."
cat > /etc/docker/daemon.json << EOF
{
  "insecure-registries": ["${REGISTRY}"]
}
EOF

# 重启Docker服务
echo "🔄 重启Docker服务..."
systemctl restart docker

# 等待Docker启动
echo "⏳ 等待Docker服务启动..."
sleep 5

# 验证配置
echo "🔍 验证Docker配置..."
if docker info | grep -q "Insecure Registries"; then
    echo "✅ Docker配置成功！"
    echo "📋 当前insecure-registries配置："
    docker info | grep -A 5 "Insecure Registries"
else
    echo "❌ Docker配置失败"
    exit 1
fi

echo "🎉 配置完成！现在可以正常使用Harbor registry了。" 