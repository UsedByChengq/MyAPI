# MyAPI

一个基于FastAPI的通用API服务，支持多种功能模块。

🌐 **在线地址**: https://myapi.5845.cn

📚 **API文档**: https://myapi.5845.cn/docs

## 功能特性

- 🚀 基于FastAPI构建，性能优异
- 📝 支持获取微信公众号文章HTML内容
- 📄 支持转换为Markdown格式
- 🖼️ 自动下载并替换图片为本地URL
- 🔧 完整的配置管理
- 🧪 全面的测试覆盖
- 📚 自动生成API文档

## 项目结构

```
MyAPI/
├── app/                    # 应用主目录
│   ├── api/               # API路由
│   │   └── v1/           # API v1版本
│   │       └── endpoints/ # API端点
│   ├── core/              # 核心模块
│   │   ├── config.py     # 配置管理
│   │   └── exceptions.py # 自定义异常
│   ├── schemas/           # 数据模型
│   ├── services/          # 业务服务层
│   ├── utils/             # 工具模块
│   └── main.py           # 应用入口
├── tests/                 # 测试目录
├── static/               # 静态文件
├── pyproject.toml        # 项目配置
├── run.py               # 启动脚本
└── README.md            # 项目文档
```

## 快速开始

### 环境要求

- Python 3.11+
- uv (推荐) 或 pip

### 安装依赖

```bash
# 使用uv安装
uv sync

# 或使用pip安装
pip install -e .
```

### 配置环境变量

复制环境变量示例文件：

```bash
cp env.example .env
```

根据需要修改 `.env` 文件中的配置。

### 启动服务

```bash
# 使用启动脚本
python run.py

# 或直接使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 5201 --reload
```

### 访问API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:5201/docs
- ReDoc: http://localhost:5201/redoc

## API使用

### 获取文章内容（HTML格式）

```bash
GET /api/v1/wechat?url={微信公众号文章URL}
```

响应示例：

```json
{
  "title": "文章标题",
  "content": "<div>文章HTML内容</div>",
  "cover": "https://example.com/cover.jpg"
}
```

### 获取文章内容（Markdown格式）

```bash
GET /api/v1/wechat/markdown?url={微信公众号文章URL}
```

响应为Markdown格式的文本，图片会被下载到本地并替换URL。

## 开发指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_wechat_service.py

# 运行测试并显示覆盖率
pytest --cov=app
```

### 代码格式化

```bash
# 格式化代码
black app/ tests/

# 排序导入
isort app/ tests/

# 类型检查
mypy app/
```

### 添加新功能

1. 在 `app/schemas/` 中添加数据模型
2. 在 `app/services/` 中添加业务逻辑
3. 在 `app/api/v1/endpoints/` 中添加API端点
4. 在 `tests/` 中添加测试用例

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t myapi .

# 运行容器
docker run -p 5201:5201 myapi
```

### Docker Compose部署

```bash
docker-compose up -d
```

### GitHub Actions 自动部署

本项目配置了 GitHub Actions 实现自动部署。当代码推送到 `main` 分支时，会自动：

1. 构建 Docker 镜像
2. 推送到 [阿里云容器镜像服务](https://cr.console.aliyun.com/)
3. 部署到服务器

详细配置说明请查看 [GitHub Actions 配置指南](docs/github-actions-setup.md)。

## 配置说明

### 图片URL配置

项目使用独立的图片域名配置：

- **BASE_URL**: 应用主域名（如：https://myapi.5845.cn）
- **BASE_IMAGE_URL**: 图片访问域名（如：https://myapi.5845.cn/static/images/）

图片会保存在应用服务器的static/images目录中，通过应用域名访问。

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `APP_NAME` | 应用名称 | MyAPI |
| `APP_VERSION` | 应用版本 | 1.0.0 |
| `DEBUG` | 调试模式 | false |
| `BASE_URL` | 应用域名 | https://myapi.5845.cn |
| `BASE_IMAGE_URL` | 图片访问域名 | https://myapi.5845.cn/static/images/ |
| `CORS_ORIGINS` | CORS允许的源 | ["*"] |
| `STATIC_IMG_DIR` | 静态图片目录 | static/images |
| `REQUEST_TIMEOUT` | 请求超时时间 | 10 |
| `ALLOWED_DOMAINS` | 允许的域名 | ["mp.weixin.qq.com"] |

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持微信公众号文章抓取
- 支持HTML和Markdown格式输出
- 自动图片下载和替换功能
