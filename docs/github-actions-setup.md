# GitHub Actions 自动部署配置指南

本文档说明如何配置 GitHub Actions 实现代码提交后自动构建 Docker 镜像并部署到服务器。

## 📋 前置条件

1. **GitHub 仓库**: 确保代码已推送到 GitHub
2. **服务器**: 需要一台运行 Docker 的服务器
3. **GitHub Secrets**: 需要在仓库中配置服务器连接信息

## 🔧 配置步骤

### 1. 配置 GitHub Secrets

在 GitHub 仓库中，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下 secrets：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `SERVER_HOST` | 服务器IP地址 | `192.168.1.100` |
| `SERVER_USERNAME` | SSH用户名 | `root` |
| `SERVER_SSH_KEY` | SSH私钥内容 | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `SERVER_PORT` | SSH端口 | `22` |

### 2. 生成 SSH 密钥对

如果还没有 SSH 密钥，请生成一对：

```bash
# 生成 SSH 密钥对
ssh-keygen -t ed25519 -C "github-actions@example.com"

# 将公钥添加到服务器
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@server-ip

# 将私钥内容复制到 GitHub Secrets
cat ~/.ssh/id_ed25519
```

### 3. 服务器准备

确保服务器已安装 Docker 和 Docker Compose：

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker
```

### 4. 创建部署目录

在服务器上创建部署目录：

```bash
mkdir -p /opt/myapi
cd /opt/myapi
```

## 🚀 工作流程

### 自动部署流程

1. **代码推送**: 向 `main` 分支推送代码
2. **触发构建**: GitHub Actions 自动触发构建流程
3. **构建镜像**: 构建 Docker 镜像并推送到 GitHub Container Registry
4. **部署到服务器**: 通过 SSH 连接到服务器并部署新镜像
5. **健康检查**: 验证服务是否正常启动

### 手动部署

如果需要手动部署，可以使用提供的部署脚本：

```bash
# 在服务器上运行
./scripts/deploy.sh [镜像标签]
```

## 📁 文件结构

```
.github/
└── workflows/
    ├── ci-cd.yml      # 完整的CI/CD流程（包含测试）
    └── deploy.yml     # 简化的自动部署流程

scripts/
└── deploy.sh         # 服务器端部署脚本

docs/
└── github-actions-setup.md  # 本文档
```

## 🔍 故障排除

### 常见问题

1. **SSH 连接失败**
   - 检查服务器 IP 和端口是否正确
   - 确认 SSH 密钥已正确配置
   - 检查服务器防火墙设置

2. **Docker 镜像拉取失败**
   - 确认 GitHub Container Registry 权限设置
   - 检查网络连接

3. **服务启动失败**
   - 查看容器日志：`docker-compose logs myapi`
   - 检查端口是否被占用
   - 确认环境变量配置正确

### 查看部署状态

```bash
# 查看容器状态
docker-compose ps

# 查看容器日志
docker-compose logs -f myapi

# 检查服务健康状态
curl -f http://localhost:5201/docs
```

## 📊 监控和日志

### GitHub Actions 日志

在 GitHub 仓库的 `Actions` 标签页可以查看：
- 构建状态
- 部署日志
- 错误信息

### 服务器监控

```bash
# 查看系统资源使用情况
docker stats

# 查看容器资源使用
docker stats myapi

# 查看磁盘使用情况
df -h
```

## 🔒 安全建议

1. **使用专用用户**: 不要使用 root 用户进行部署
2. **限制 SSH 访问**: 只允许必要的 IP 地址访问
3. **定期更新**: 定期更新 Docker 镜像和系统
4. **备份数据**: 定期备份重要数据
5. **监控日志**: 定期检查系统日志

## 📞 支持

如果遇到问题，请：

1. 查看 GitHub Actions 日志
2. 检查服务器容器日志
3. 确认所有配置是否正确
4. 联系技术支持 