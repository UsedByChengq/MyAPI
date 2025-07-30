# Docker 权限配置指南

本指南将帮助您在服务器上配置Docker，让普通用户使用Docker时不需要加sudo。

## 🔧 方法一：添加用户到docker组（推荐）

### 1. 检查docker组是否存在

```bash
# 检查docker组是否存在
sudo getent group docker
```

如果输出类似 `docker:x:999:username`，说明组已存在。

### 2. 创建docker组（如果不存在）

```bash
# 创建docker组
sudo groupadd docker
```

### 3. 将当前用户添加到docker组

```bash
# 将当前用户添加到docker组
sudo usermod -aG docker $USER

# 或者指定特定用户
sudo usermod -aG docker your_username
```

### 4. 重新加载组权限

```bash
# 方法1：重新登录
exit
# 然后重新SSH登录到服务器

# 方法2：重新加载组权限（不需要重新登录）
newgrp docker
```

### 5. 验证配置

```bash
# 测试docker命令
docker --version
docker ps

# 测试构建镜像
docker build --help
```

## 🔧 方法二：修改Docker socket权限

### 1. 修改Docker socket权限

```bash
# 修改Docker socket权限
sudo chmod 666 /var/run/docker.sock
```

### 2. 设置开机自动修改权限

```bash
# 创建systemd服务文件
sudo tee /etc/systemd/system/docker-socket-permissions.service > /dev/null <<EOF
[Unit]
Description=Set Docker socket permissions
After=docker.socket

[Service]
Type=oneshot
ExecStart=/bin/chmod 666 /var/run/docker.sock
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
sudo systemctl enable docker-socket-permissions.service
sudo systemctl start docker-socket-permissions.service
```

## 🔧 方法三：使用Docker Desktop（如果适用）

如果您使用的是支持Docker Desktop的系统：

```bash
# 安装Docker Desktop
# 然后Docker会自动配置权限
```

## 🔍 验证配置

### 1. 基本验证

```bash
# 检查用户是否在docker组中
groups $USER

# 检查docker socket权限
ls -la /var/run/docker.sock

# 测试docker命令
docker info
```

### 2. 完整测试

```bash
# 测试构建镜像
docker build -t test-image .

# 测试运行容器
docker run --rm hello-world

# 测试拉取镜像
docker pull nginx:alpine
```

## 🚨 安全注意事项

### 1. 权限风险

将用户添加到docker组等同于给予该用户root权限，因为：
- Docker容器可以挂载主机文件系统
- 可以访问主机网络
- 可以修改主机配置

### 2. 安全建议

```bash
# 只给需要的用户添加docker权限
sudo usermod -aG docker deploy_user

# 定期检查docker组用户
getent group docker

# 监控Docker使用情况
docker system df
docker ps -a
```

## 🔧 故障排除

### 1. 权限被拒绝

```bash
# 错误：Got permission denied while trying to connect to the Docker daemon socket

# 解决方案：
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Docker服务未启动

```bash
# 检查Docker服务状态
sudo systemctl status docker

# 启动Docker服务
sudo systemctl start docker

# 设置开机自启
sudo systemctl enable docker
```

### 3. 组权限未生效

```bash
# 重新加载组权限
newgrp docker

# 或者重新登录
exit
# 重新SSH登录
```

## 📋 完整配置脚本

创建一个自动化配置脚本：

```bash
#!/bin/bash
# docker-setup.sh

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
    echo "📋 用户信息："
    groups $USER
    echo "🔍 Docker信息："
    docker --version
else
    echo "❌ Docker权限配置失败"
    exit 1
fi

echo "💡 提示：如果仍有问题，请重新登录服务器"
```

使用方法：

```bash
# 给脚本执行权限
chmod +x docker-setup.sh

# 运行脚本
./docker-setup.sh
```

## 📞 常见问题

### Q: 为什么需要重新登录？
A: 用户组权限的更改需要重新登录才能生效，或者使用 `newgrp docker` 命令。

### Q: 修改socket权限安全吗？
A: 修改socket权限会降低安全性，建议使用用户组方法。

### Q: 如何撤销权限？
A: 使用 `sudo gpasswd -d $USER docker` 将用户从docker组中移除。

### Q: 生产环境如何处理？
A: 在生产环境中，建议：
- 只给部署用户添加docker权限
- 使用CI/CD工具进行部署
- 定期审计Docker使用情况 