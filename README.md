# 🤖 yili-ai-learn

一个专注于人工智能学习的综合性项目，涵盖向量数据库、机器学习、深度学习等多个AI领域的学习资料和实践代码。

## 📁 项目结构

```
yili-ai-learn/
├── README.md                    # 项目说明文档
├── requirements.txt             # 项目依赖包
├── .gitignore                   # Git 忽略文件
├── setup.py                     # 项目安装配置（可选）
│
├── 向量数据库/                   # 向量数据库学习模块
│   └── milvus/                  # Milvus 向量数据库
│       ├── 01milvus介绍.md      # Milvus 基础介绍
│       ├── 02本地milvus的简单使用.md  # Milvus Lite 使用教程
│       └── demo/                # 演示代码
│           └── 02demo/          # Milvus Lite 演示
│               ├── 01_basic_usage.py
│               ├── 02_advanced_features.py
│               ├── 03_langchain_integration.py
│               ├── run_all_demos.py
│               └── README.md
│
├── 机器学习/                     # 机器学习学习模块（待扩展）
├── 深度学习/                     # 深度学习学习模块（待扩展）
├── 自然语言处理/                 # NLP 学习模块（待扩展）
├── 计算机视觉/                   # CV 学习模块（待扩展）
│
├── utils/                       # 通用工具模块
├── config/                      # 配置文件目录
└── tests/                       # 测试代码目录
```

## 🚀 快速开始

### 方法一：自动设置（推荐）

```bash
# 克隆项目
git clone https://github.com/your-username/yili-ai-learn.git
cd yili-ai-learn

# 运行自动设置脚本
python setup_dev.py
```

### 方法二：手动设置

```bash
# 1. 克隆项目
git clone https://github.com/your-username/yili-ai-learn.git
cd yili-ai-learn

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装开发依赖（可选）
pip install -e .[dev]

# 5. 设置pre-commit hooks（可选）
pre-commit install
```

### 3. 开始学习

```bash
# 使用 Makefile 命令（推荐）
make run-milvus-demo

# 或者直接运行
python -m 向量数据库.milvus.demo.02demo.run_all_demos

# 或者进入目录运行
cd 向量数据库/milvus/demo/02demo
python run_all_demos.py
```

## 📚 学习模块

### 🗄️ 向量数据库

- **Milvus**: 开源向量数据库的学习和实践
  - Milvus Lite 本地版本使用
  - 与 LangChain 框架集成
  - 性能优化和最佳实践

### 🤖 机器学习（规划中）

- 监督学习算法
- 无监督学习算法
- 强化学习基础
- 特征工程技巧

### 🧠 深度学习（规划中）

- 神经网络基础
- 卷积神经网络 (CNN)
- 循环神经网络 (RNN)
- Transformer 架构

### 📝 自然语言处理（规划中）

- 文本预处理
- 词嵌入技术
- 语言模型
- 文本分类和情感分析

### 👁️ 计算机视觉（规划中）

- 图像处理基础
- 目标检测
- 图像分类
- 图像生成

## 🛠️ 开发环境

### 系统要求

- **Python**: 3.8+ （推荐 3.9+）
- **操作系统**: macOS, Linux, Windows
- **内存**: 建议 8GB+
- **存储**: 建议 2GB+ 可用空间

### 推荐工具

- **IDE**: VS Code（已配置设置）, PyCharm
- **包管理**: pip, conda
- **版本控制**: Git
- **终端**: 支持 Make 命令

### 开发工具链

项目已配置完整的开发工具链：

- **代码格式化**: Black
- **导入排序**: isort  
- **代码检查**: flake8, mypy
- **测试框架**: pytest
- **Git hooks**: pre-commit
- **构建工具**: setuptools, wheel

### 常用命令

```bash
# 查看所有可用命令
make help

# 安装依赖
make install

# 代码格式化
make format

# 代码检查
make lint

# 运行测试
make test

# 清理临时文件
make clean

# 运行Milvus演示
make run-milvus-demo
```

### 核心依赖

- `pymilvus`: Milvus Python SDK
- `langchain-milvus`: LangChain Milvus 集成
- `numpy`, `pandas`: 数据处理
- `jupyter`: 交互式开发环境

## 📖 使用指南

### 向量数据库学习路径

1. **基础概念**: 阅读 `向量数据库/milvus/01milvus介绍.md`
2. **本地实践**: 学习 `向量数据库/milvus/02本地milvus的简单使用.md`
3. **代码实践**: 运行 `向量数据库/milvus/demo/02demo/` 中的演示代码
4. **进阶应用**: 尝试与 LangChain 集成的高级功能

### 代码规范

- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 编写清晰的文档字符串
- 添加适当的类型注解

## 🤝 贡献指南

欢迎贡献代码、文档或学习资料！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 项目维护者: [你的名字]
- 邮箱: [你的邮箱]
- 项目链接: [https://github.com/your-username/yili-ai-learn](https://github.com/your-username/yili-ai-learn)

## 🙏 致谢

感谢以下开源项目和社区：

- [Milvus](https://milvus.io/) - 开源向量数据库
- [LangChain](https://langchain.com/) - LLM 应用开发框架
- [NumPy](https://numpy.org/) - 科学计算库
- [Pandas](https://pandas.pydata.org/) - 数据分析库

---

⭐ 如果这个项目对你有帮助，请给它一个星标！