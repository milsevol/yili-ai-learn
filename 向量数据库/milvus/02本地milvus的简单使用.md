# Milvus Lite 本地版本使用教程

> 📚 **学习指南**: 本教程与 `demo/02demo/` 目录下的代码示例一一对应，建议边学习理论边运行代码实践。

## 📁 教程与代码对应关系

| 教程章节 | 对应代码文件 | 学习重点 |
|---------|-------------|----------|
| [基本使用](#基本使用) | `01_basic_usage.py` | 客户端连接、集合创建、数据插入、基础搜索 |
| [高级功能](#高级功能) | `02_advanced_features.py` | 批量操作、复杂查询、性能优化 |
| [LangChain 集成](#与-langchain-集成) | `03_langchain_integration.py` | 框架集成、文档向量化、RAG应用 |

> 💡 **运行建议**: 
> 1. 先阅读对应章节的理论知识
> 2. 运行相应的代码示例：`cd demo/02demo && python 文件名.py`
> 3. 对比代码输出与教程说明，加深理解

## 什么是 Milvus Lite？

Milvus Lite 是 Milvus 的轻量级版本，专为本地开发和小规模原型设计而设计。它提供了与 Milvus 相同的核心向量搜索功能，但无需复杂的部署配置，可以直接在本地环境中运行。

### 主要特点

- **轻量级**：无需 Docker 或 Kubernetes，直接在 Python 环境中运行
- **易于使用**：与 Milvus Standalone 和 Distributed 使用相同的 API
- **本地存储**：数据存储在本地文件中，便于开发和测试
- **快速启动**：几分钟内即可开始构建 AI 应用程序

### 适用场景

- Jupyter Notebook / Google Colab 开发
- 笔记本电脑本地开发
- 边缘设备部署
- 小规模原型验证（通常少于 100 万个向量）

### 系统要求

- **Linux**: Ubuntu >= 20.04 (x86_64 和 arm64)
- **macOS**: >= 11.0 (Apple Silicon M1/M2 和 x86_64)
- **Python**: >= 3.7
- **注意**: 目前不支持 Windows

## 安装

### 方法一：通过 pymilvus 安装（推荐）

```bash
pip install -U pymilvus
```

Milvus Lite 已包含在 pymilvus 2.4.2 及以上版本中，推荐使用此方法。

### 方法二：直接安装 milvus-lite

```bash
pip install -U milvus-lite
```

## 基本使用

> 🎯 **对应代码**: `01_basic_usage.py` - 完整的基础使用示例
> 
> 📝 **运行方式**: `cd demo/02demo && python 01_basic_usage.py`

### 1. 创建客户端连接

```python
from pymilvus import MilvusClient

# 指定本地文件名作为 uri 参数即可使用 Milvus Lite
client = MilvusClient("./milvus_demo.db")
```

**代码示例位置**: `01_basic_usage.py` 第 13-15 行

### 2. 创建集合

```python
# 创建集合
client.create_collection(
    collection_name="demo_collection",
    dimension=768,  # 向量维度
    metric_type="L2",  # 距离度量类型
    consistency_level="Strong"
)
```

**代码示例位置**: `01_basic_usage.py` 第 18-32 行
- 包含集合存在性检查
- 自动删除已存在的集合
- 创建新集合的完整流程

### 3. 插入数据

```python
import random

# 准备示例数据
data = []
for i in range(1000):
    vector = [random.random() for _ in range(768)]
    data.append({
        "id": i,
        "vector": vector,
        "text": f"这是第 {i} 条文本数据",
        "category": f"类别_{i % 5}"
    })

# 插入数据
client.insert(
    collection_name="demo_collection",
    data=data
)
```

**代码示例位置**: `01_basic_usage.py` 第 34-55 行
- 生成 1000 条示例数据
- 包含 id、vector、text、category、score 字段
- 展示数据插入的性能统计

### 4. 创建索引

```python
# 创建索引以提高搜索性能
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}

client.create_index(
    collection_name="demo_collection",
    field_name="vector",
    index_params=index_params
)
```

**代码示例位置**: `01_basic_usage.py` 第 57-61 行
- **注意**: 示例代码使用 Milvus Lite 的自动索引功能
- 无需手动创建索引，系统会在搜索时自动优化

### 5. 搜索向量

```python
# 准备查询向量
query_vector = [random.random() for _ in range(768)]

# 执行搜索
search_params = {
    "metric_type": "L2",
    "params": {"nprobe": 10}
}

results = client.search(
    collection_name="demo_collection",
    data=[query_vector],
    limit=5,
    search_params=search_params,
    output_fields=["text", "category"]
)

# 打印结果
for result in results[0]:
    print(f"ID: {result['id']}, 距离: {result['distance']}, 文本: {result['entity']['text']}")
```

**代码示例位置**: `01_basic_usage.py` 第 63-85 行
- 展示基础向量搜索功能
- 包含搜索性能统计
- 详细的结果输出格式

## 高级功能

> 🚀 **对应代码**: `02_advanced_features.py` - 高级功能完整示例
> 
> 📝 **运行方式**: `cd demo/02demo && python 02_advanced_features.py`

### 1. 混合搜索（向量 + 标量过滤）

```python
# 带过滤条件的搜索
results = client.search(
    collection_name="demo_collection",
    data=[query_vector],
    limit=5,
    search_params=search_params,
    filter="category == '类别_1'",  # 标量过滤条件
    output_fields=["text", "category"]
)
```

**代码示例位置**: 
- `01_basic_usage.py` 第 87-99 行 - 基础过滤搜索
- `02_advanced_features.py` 第 120-160 行 - 复杂过滤条件示例

### 2. 数据管理

```python
# 查询特定数据
query_results = client.query(
    collection_name="demo_collection",
    filter="id in [1, 2, 3]",
    output_fields=["text", "category"]
)

# 删除数据
client.delete(
    collection_name="demo_collection",
    filter="id in [1, 2, 3]"
)

# 获取集合统计信息
stats = client.get_collection_stats(collection_name="demo_collection")
print(f"集合中的实体数量: {stats['row_count']}")
```

**代码示例位置**: 
- `01_basic_usage.py` 第 101-115 行 - 基础查询操作
- `02_advanced_features.py` 第 162-200 行 - 高级数据管理功能

### 3. 集合管理

```python
# 列出所有集合
collections = client.list_collections()
print("所有集合:", collections)

# 检查集合是否存在
exists = client.has_collection(collection_name="demo_collection")
print(f"集合是否存在: {exists}")

# 删除集合
client.drop_collection(collection_name="demo_collection")
```

**代码示例位置**: `01_basic_usage.py` 第 117-125 行
- 集合统计信息获取
- 集合列表查看
- 完整的集合生命周期管理

## 性能优化

> 📊 **对应代码**: `02_advanced_features.py` - 性能优化和基准测试示例

### 1. 索引选择

Milvus Lite 会根据数据量自动选择索引：

- **数据量 < 100,000**: 自动使用 FLAT 索引以获得更好性能
- **数据量 ≥ 100,000**: 构建并使用 IVF_FLAT 索引

**代码示例位置**: `02_advanced_features.py` 第 35-50 行
- 展示了手动索引创建的方法
- 使用 COSINE 相似度和 IVF_FLAT 索引

### 2. 批量操作

```python
# 批量插入以提高性能
batch_size = 1000
for i in range(0, len(large_data), batch_size):
    batch = large_data[i:i + batch_size]
    client.insert(
        collection_name="demo_collection",
        data=batch
    )
```

**代码示例位置**: `02_advanced_features.py` 第 80-105 行
- 演示 5000 条数据的批量插入
- 包含性能统计和插入速度计算
- 展示批量操作的最佳实践

## 数据迁移

### 导出数据

```bash
# 安装必要的依赖
pip install -U "pymilvus[bulk_writer]"

# 导出数据到 JSON 文件
milvus-lite dump -d ./milvus_demo.db -c demo_collection -p ./data_dir
```

### 导入到其他 Milvus 部署

导出的数据可以轻松导入到：
- Docker 上的 Milvus Standalone
- Kubernetes 上的 Milvus Distributed  
- Zilliz Cloud 上的托管 Milvus

## 限制和注意事项

### 已知限制

- 不支持分区（partitions）
- 不支持用户/角色/RBAC
- 不支持别名（alias）
- 适用于小规模数据（< 100 万向量）

### 生产环境建议

对于大规模生产环境，建议使用：
- [Milvus Standalone](https://milvus.io/docs/install-overview.md#Milvus-Standalone)
- [Milvus Distributed](https://milvus.io/docs/install-overview.md#Milvus-Distributed)
- [Zilliz Cloud](https://zilliz.com/cloud)（完全托管的 Milvus）

## 与 LangChain 集成

> 🔗 **对应代码**: `03_langchain_integration.py` - LangChain 集成完整示例
> 
> 📝 **运行方式**: `cd demo/02demo && python 03_langchain_integration.py`

Milvus Lite 可以与 LangChain 无缝集成：

```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

# 使用 LangChain 的 Milvus 向量存储
embeddings = OpenAIEmbeddings()
vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"uri": "./milvus_demo.db"},
    collection_name="langchain_collection"
)

# 添加文档
texts = ["这是第一个文档", "这是第二个文档"]
vector_store.add_texts(texts)

# 相似性搜索
results = vector_store.similarity_search("文档", k=2)
```

**代码示例位置**: `03_langchain_integration.py`
- 第 20-40 行: 自定义嵌入模型实现
- 第 42-70 行: 示例文档创建
- 第 72-120 行: 基础 LangChain 集成演示
- 第 122-150 行: 检索器使用示例
- 第 152-180 行: 元数据过滤演示

**主要功能演示**:
- 文档向量化和存储
- 相似性搜索和带分数搜索
- MMR (最大边际相关性) 检索
- 元数据过滤查询
- 多种检索器配置

## 📚 完整学习路径

### 🎯 第一步：基础入门 (15-20分钟)
1. **阅读**: [基本使用](#基本使用) 章节
2. **实践**: 运行 `01_basic_usage.py`
3. **重点**: 理解客户端连接、集合创建、数据插入、基础搜索

```bash
cd demo/02demo
python 01_basic_usage.py
```

### 🚀 第二步：进阶学习 (20-25分钟)
1. **阅读**: [高级功能](#高级功能) 和 [性能优化](#性能优化) 章节
2. **实践**: 运行 `02_advanced_features.py`
3. **重点**: 批量操作、复杂查询、性能优化技巧

```bash
python 02_advanced_features.py
```

### 🔗 第三步：框架集成 (25-30分钟)
1. **阅读**: [与 LangChain 集成](#与-langchain-集成) 章节
2. **实践**: 运行 `03_langchain_integration.py`
3. **重点**: 文档向量化、检索器使用、RAG应用

```bash
python 03_langchain_integration.py
```

### 📊 学习成果检验
完成所有实践后，你应该能够：
- ✅ 独立创建和管理 Milvus 集合
- ✅ 实现高效的向量搜索和过滤
- ✅ 集成 LangChain 构建 RAG 应用
- ✅ 优化向量数据库性能
- ✅ 理解向量数据库的核心概念

## 总结

Milvus Lite 是学习和开发向量数据库应用的理想选择，它提供了：

1. **零配置启动**：无需复杂的部署设置
2. **完整功能**：支持向量搜索的核心功能
3. **API 一致性**：与其他 Milvus 部署方式保持一致
4. **易于迁移**：可以轻松迁移到生产环境

通过本教程和配套的代码示例，你可以快速掌握向量数据库的核心概念和实际应用，为后续的生产部署打下坚实基础。

> 💡 **下一步建议**: 
> - 尝试使用真实的嵌入模型（如 OpenAI Embeddings）
> - 构建自己的 RAG 应用
> - 探索 Milvus 的分布式部署方案