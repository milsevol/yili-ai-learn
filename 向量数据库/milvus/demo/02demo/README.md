# 🚀 Milvus Lite 演示代码

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Milvus](https://img.shields.io/badge/Milvus-Lite-green.svg)](https://milvus.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-orange.svg)](https://langchain.com/)

本演示项目提供了 **Milvus Lite** 的完整学习路径，从基础操作到高级应用，帮助你快速掌握向量数据库的核心概念和实际应用。

## ✨ 特性亮点

- 🎯 **零配置启动**: 无需复杂安装，开箱即用
- 📚 **渐进式学习**: 从基础到高级，循序渐进
- 🔗 **框架集成**: 深度集成 LangChain 生态
- 📊 **性能分析**: 内置性能测试和优化建议
- 🛠️ **生产就绪**: 提供生产环境迁移指南

## 📁 项目结构

```
02demo/
├── 📄 01_basic_usage.py          # 🎯 基础入门 - 从这里开始
├── 📄 02_advanced_features.py    # 🚀 进阶功能 - 深入学习
├── 📄 03_langchain_integration.py # 🔗 框架集成 - 实战应用
├── 📄 run_all_demos.py           # 🎮 交互式运行器
├── 📄 __init__.py                # 📦 模块初始化
└── 📄 README.md                  # 📖 本说明文件
```

### 🎯 学习路径

| 阶段 | 文件 | 学习内容 | 预计时间 |
|------|------|----------|----------|
| **入门** | `01_basic_usage.py` | 客户端连接、集合管理、基础CRUD | 15分钟 |
| **进阶** | `02_advanced_features.py` | 批量操作、性能优化、复杂查询 | 20分钟 |
| **实战** | `03_langchain_integration.py` | LangChain集成、RAG应用 | 25分钟 |

### 📋 功能清单

#### 🎯 基础功能 (`01_basic_usage.py`)
- ✅ 客户端连接与配置
- ✅ 集合创建与Schema定义
- ✅ 数据插入与批量操作
- ✅ 索引创建与管理
- ✅ 向量相似性搜索
- ✅ 条件过滤查询
- ✅ 数据更新与删除

#### 🚀 高级功能 (`02_advanced_features.py`)
- ✅ 大规模数据批量处理
- ✅ 复杂搜索条件组合
- ✅ 性能基准测试
- ✅ 内存使用优化
- ✅ 数据统计分析
- ✅ 数据导出与备份

#### 🔗 框架集成 (`03_langchain_integration.py`)
- ✅ LangChain VectorStore集成
- ✅ 文档向量化与存储
- ✅ 多种检索器实现
- ✅ 元数据过滤与管理
- ✅ RAG应用场景演示
- ✅ 性能对比分析

> 💡 **提示**: 项目依赖位于根目录 `requirements.txt`，支持一键安装。

## 🚀 快速开始

### 方式一：交互式运行（推荐新手）

```bash
# 1. 进入项目根目录
cd /Users/cuixueyong/code/github/yili-ai-learn

# 2. 安装依赖（如果还没安装）
pip install -r requirements.txt

# 3. 进入演示目录
cd 向量数据库/milvus/demo/02demo

# 4. 运行交互式演示
python run_all_demos.py
```

### 方式二：单独运行（适合有经验的用户）

```bash
# 进入演示目录
cd 向量数据库/milvus/demo/02demo

# 按学习路径依次运行
python 01_basic_usage.py      # 🎯 基础入门
python 02_advanced_features.py # 🚀 进阶功能  
python 03_langchain_integration.py # 🔗 框架集成
```

### 方式三：使用 Make 命令（项目根目录）

```bash
# 在项目根目录执行
make run-milvus-demo
```

## 📊 演示内容预览

### 🎯 基础演示 (`01_basic_usage.py`)
```
🔄 正在创建 Milvus Lite 客户端...
✅ 客户端连接成功
🔄 正在创建集合 'demo_collection'...
✅ 集合创建成功，Schema: [id, vector, text, category, score]
🔄 正在插入 1000 条示例数据...
✅ 数据插入完成，耗时: 0.85s
🔄 正在创建向量索引...
✅ 索引创建成功，类型: FLAT
🔄 正在执行向量搜索...
✅ 搜索完成，找到 5 个相似结果，耗时: 0.003s
```

### 🚀 高级演示 (`02_advanced_features.py`)
```
🔄 正在批量插入 5000 条数据...
✅ 批量插入完成，平均速度: 3200 条/秒
🔄 正在执行性能基准测试...
✅ 搜索性能: 平均 0.002s/查询
📊 内存使用: 45.2MB
📈 索引效率: 98.5%
```

### 🔗 LangChain 集成演示 (`03_langchain_integration.py`)
```
🔄 正在初始化 LangChain VectorStore...
✅ VectorStore 创建成功
🔄 正在向量化文档...
✅ 文档向量化完成，共 50 个文档
🔄 正在执行相似性搜索...
✅ 找到最相关文档: "向量数据库基础概念"
🎯 相似度得分: 0.92
```

## 📋 数据结构说明

### 🎯 基础演示数据 (`01_basic_usage.py`)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `id` | `int` | 唯一标识符 | `1001` |
| `vector` | `List[float]` | 128维向量 | `[0.1, 0.2, ...]` |
| `text` | `str` | 文本内容 | `"机器学习基础概念"` |
| `category` | `str` | 分类标签 | `"AI", "ML", "DL"` |
| `score` | `int` | 评分 (1-100) | `85` |

```python
# 示例数据
{
    "id": 1001,
    "vector": [0.12, -0.34, 0.56, ...],  # 128维
    "text": "深度学习是机器学习的一个分支",
    "category": "AI",
    "score": 92
}
```

### 🚀 高级演示数据 (`02_advanced_features.py`)

| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| `id` | `int` | 唯一标识符 | 主键 |
| `vector` | `List[float]` | 归一化向量 | L2范数=1 |
| `title` | `str` | 文档标题 | 长度≤200 |
| `content` | `str` | 文档内容 | 长度≤2000 |
| `category` | `str` | 内容分类 | 预定义类别 |
| `source` | `str` | 数据来源 | URL或标识 |
| `publish_year` | `int` | 发布年份 | 2000-2024 |
| `view_count` | `int` | 浏览次数 | ≥0 |
| `rating` | `float` | 用户评分 | 0.0-5.0 |

### 🔗 LangChain 文档结构 (`03_langchain_integration.py`)

```python
from langchain.schema import Document

# 标准文档结构
Document(
    page_content="向量数据库是一种专门存储和检索向量数据的数据库...",
    metadata={
        "category": "database",      # 文档类别
        "source": "tutorial",        # 数据来源
        "difficulty": "beginner",    # 难度等级
        "year": 2024,               # 发布年份
        "tags": ["vector", "db"],   # 标签列表
        "author": "AI Expert"       # 作者信息
    }
)
```

### 📊 数据生成规则

- **向量维度**: 统一使用 128 维
- **向量范围**: [-1.0, 1.0] 之间的浮点数
- **文本长度**: 中文 10-100 字符，英文 20-200 字符
- **类别分布**: AI(40%), ML(30%), DL(20%), 其他(10%)
- **评分分布**: 正态分布，均值 75，标准差 15

## 生成的数据库文件

运行演示后，会在当前目录生成以下数据库文件：

- `milvus_basic_demo.db` - 基础演示数据库
- `milvus_advanced_demo.db` - 高级功能演示数据库
- `langchain_milvus_demo.db` - LangChain 集成演示数据库
- `small_dim_demo.db` - 小维度性能测试数据库
- `large_dim_demo.db` - 大维度性能测试数据库

## 性能特点

### Milvus Lite 自动优化
- **数据量 < 100,000**: 自动使用 FLAT 索引
- **数据量 ≥ 100,000**: 自动使用 IVF_FLAT 索引

### 演示性能指标
- **插入性能**: ~1000-5000 条/秒（取决于向量维度）
- **搜索性能**: ~0.001-0.01 秒/查询（取决于数据量和索引类型）
- **批量搜索**: 比单次搜索提升 3-5 倍性能

## 注意事项

1. **系统要求**
   - macOS >= 11.0 或 Ubuntu >= 20.04
   - Python >= 3.7
   - 暂不支持 Windows

2. **数据规模限制**
   - 适用于小规模原型（< 100 万向量）
   - 生产环境建议使用 Milvus Standalone 或 Distributed

3. **功能限制**
   - 不支持分区（partitions）
   - 不支持用户/角色管理
   - 不支持别名功能

## 故障排除

### 常见问题

1. **导入错误**
   ```bash
   # 确保安装了正确的依赖
   pip install -U pymilvus
   pip install langchain-milvus
   ```

2. **数据库文件权限问题**
   ```bash
   # 确保当前目录有写权限
   chmod 755 .
   ```

3. **内存不足**
   - 减少批量插入的数据量
   - 降低向量维度
   - 使用更小的索引参数

## 扩展学习

### 进阶主题
1. **自定义嵌入模型**: 集成 OpenAI、Sentence Transformers 等
2. **生产部署**: 迁移到 Milvus Standalone 或 Zilliz Cloud
3. **性能优化**: 索引选择、搜索参数调优
4. **数据迁移**: 使用 `milvus-lite dump` 命令导出数据

### 相关资源
- [Milvus 官方文档](https://milvus.io/docs)
- [LangChain Milvus 集成文档](https://python.langchain.com/docs/integrations/vectorstores/milvus)
- [Milvus Lite GitHub](https://github.com/milvus-io/milvus-lite)

## 联系和反馈

如果在使用过程中遇到问题或有改进建议，欢迎：
- 查阅 [Milvus 官方文档](https://milvus.io/docs)
- 访问 [Milvus 社区](https://milvus.io/community)
- 提交 [GitHub Issues](https://github.com/milvus-io/milvus-lite/issues)