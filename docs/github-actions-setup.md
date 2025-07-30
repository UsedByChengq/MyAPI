# GitHub Actions 自动部署配置指南

本指南将帮助您配置 GitHub Actions 实现 MyAPI 的自动部署到服务器。

## 前置条件

### 1. 服务器准备
- 服务器已安装 Docker 和 Docker Compose
- 服务器可以通过 SSH 访问
- 服务器有足够的磁盘空间和内存

### 2. 阿里云容器镜像服务
- 已创建阿里云容器镜像服务实例
- 已创建命名空间和仓库
- 已获取访问凭证

### 3. GitHub 仓库
- 代码已推送到 GitHub 仓库
- 仓库已启用 GitHub Actions

## 配置步骤

### 1. 配置 GitHub Secrets

在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加以下 secrets：

#### 服务器配置
- `SERVER_HOST`: 服务器IP地址或域名
- `SERVER_USERNAME`: SSH用户名
- `SERVER_PORT`: SSH端口（通常是22）
- `SERVER_SSH_KEY`: SSH私钥内容

#### 阿里云容器镜像服务配置
- `ALIYUN_USERNAME`: 阿里云账号用户名（通常是邮箱）
- `ALIYUN_PASSWORD`: 阿里云容器镜像服务密码

### 2. 获取 SSH 私钥

在本地生成 SSH 密钥对（如果还没有）：

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

将公钥添加到服务器的 `~/.ssh/authorized_keys`：

```bash
ssh-copy-id username@server_ip
```

将私钥内容复制到 GitHub Secrets 的 `SERVER_SSH_KEY` 中：

```bash
cat ~/.ssh/id_rsa
```

### 3. 配置阿里云容器镜像服务

1. 登录阿里云控制台
2. 进入容器镜像服务
3. 创建命名空间（如：docker_for_chengq）
4. 创建仓库（如：myapi）
5. 获取登录凭证

### 4. 验证配置

推送代码到 `main` 分支，GitHub Actions 将自动：

1. 运行测试
2. 构建 Docker 镜像
3. 推送到阿里云容器镜像服务
4. 部署到服务器

## 工作流程说明

### 测试阶段
- 安装 Python 依赖
- 运行 pytest 测试
- 生成覆盖率报告

### 构建阶段
- 构建 Docker 镜像
- 登录阿里云容器镜像服务
- 推送镜像到仓库

### 部署阶段
- 连接到服务器
- 登录阿里云容器镜像服务
- 拉取最新镜像
- 启动服务

## 故障排除

### 1. SSH 连接失败
- 检查服务器IP和端口
- 验证SSH密钥是否正确
- 确认服务器防火墙设置

### 2. 镜像推送失败
- 检查阿里云账号和密码
- 确认仓库权限设置
- 验证网络连接

### 3. 服务启动失败
- 检查服务器Docker状态
- 查看容器日志
- 确认端口是否被占用

## 手动部署

如果需要手动部署，可以使用部署脚本：

```bash
# 设置环境变量
export ALIYUN_USERNAME="your_username"
export ALIYUN_PASSWORD="your_password"

# 运行部署脚本
./scripts/deploy.sh
```

## 监控和维护

### 1. 查看服务状态
```bash
docker-compose ps
docker-compose logs
```

### 2. 更新服务
```bash
docker-compose pull
docker-compose up -d
```

### 3. 回滚服务
```bash
docker-compose down
docker-compose up -d
```

## 安全建议

1. 定期更新 SSH 密钥
2. 使用强密码
3. 限制服务器访问权限
4. 监控服务日志
5. 定期备份数据 