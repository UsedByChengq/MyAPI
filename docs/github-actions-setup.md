# GitHub Actions 自动部署配置指南

本文档说明如何配置 GitHub Actions 实现代码提交后自动构建 Docker 镜像并部署到服务器。

## 📋 前置条件

1. **GitHub 仓库**: 确保代码已推送到 GitHub
2. **Harbor 私有仓库**: 使用 [Harbor](http://harbor.5845.cn/) 作为私有镜像仓库
3. **服务器**: 需要一台运行 Docker 的服务器
4. **GitHub Secrets**: 需要在仓库中配置服务器连接信息和Harbor认证信息

## 🔧 配置步骤

### 1. 配置 GitHub Secrets

在 GitHub 仓库中，进入 `Settings` → `Secrets and variables` → `Actions`，添加以下 secrets：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `HARBOR_USERNAME` | Harbor用户名 | `admin` |
| `HARBOR_PASSWORD` | Harbor密码 | `your-password` |
| `SERVER_HOST` | 服务器IP地址 | `192.168.1.100` |
| `SERVER_USERNAME` | SSH用户名 | `root` |
| `SERVER_SSH_KEY` | SSH私钥内容 | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `SERVER_PORT` | SSH端口 | `22` |

### 2. Harbor 仓库配置

确保在 Harbor 中已创建项目：
- **项目名称**: `myapi`
- **访问级别**: 私有
- **镜像名称**: `myapi`
- **完整镜像路径**: `harbor.5845.cn/myapi/myapi`

### 3. 生成 SSH 密钥对

如果还没有 SSH 密钥，请生成一对：

```bash
# 生成 SSH 密钥对
ssh-keygen -t ed25519 -C "github-actions@example.com"

# 将公钥添加到服务器
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@server-ip

# 将私钥内容复制到 GitHub Secrets
cat ~/.ssh/id_ed25519
```

### 4. 服务器准备

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

### 5. 创建部署目录

在服务器上创建部署目录：

```bash
mkdir -p /opt/myapi
cd /opt/myapi
```

## 🚀 工作流程

### 自动部署流程

1. **代码推送**: 向 `main` 分支推送代码
2. **触发构建**: GitHub Actions 自动触发构建流程
3. **构建镜像**: 构建 Docker 镜像并推送到 Harbor 私有仓库
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

1. **Harbor 认证失败**
   - 检查 Harbor 用户名和密码是否正确
   - 确认用户有推送镜像到 `myapi` 项目的权限
   - 检查 Harbor 服务是否正常运行

2. **SSH 连接失败**
   - 检查服务器 IP 和端口是否正确
   - 确认 SSH 密钥已正确配置
   - 检查服务器防火墙设置

3. **Docker 镜像拉取失败**
   - 确认服务器可以访问 Harbor 仓库
   - 检查网络连接和DNS解析
   - 确认服务器已登录到 Harbor

4. **服务启动失败**
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

### Harbor 镜像管理

在 [Harbor 控制台](http://harbor.5845.cn/) 可以：
- 查看镜像版本
- 管理镜像标签
- 设置镜像扫描策略
- 配置镜像复制规则

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

1. **Harbor 安全**:
   - 使用强密码
   - 定期更新 Harbor 版本
   - 配置镜像扫描
   - 设置访问控制策略

2. **服务器安全**:
   - 使用专用用户进行部署
   - 限制 SSH 访问
   - 定期更新系统
   - 监控系统日志

3. **镜像安全**:
   - 定期更新基础镜像
   - 扫描镜像漏洞
   - 使用最小化基础镜像
   - 定期清理旧镜像

## 📞 支持

如果遇到问题，请：

1. 查看 GitHub Actions 日志
2. 检查 Harbor 镜像仓库状态
3. 查看服务器容器日志
4. 确认所有配置是否正确
5. 联系技术支持 