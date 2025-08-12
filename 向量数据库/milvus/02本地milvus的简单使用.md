# Milvus Lite 本地版本使用教程

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

### 1. 创建客户端连接

```python
from pymilvus import MilvusClient

# 指定本地文件名作为 uri 参数即可使用 Milvus Lite
client = MilvusClient("./milvus_demo.db")
```

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

## 高级功能

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

## 性能优化

### 1. 索引选择

Milvus Lite 会根据数据量自动选择索引：

- **数据量 < 100,000**: 自动使用 FLAT 索引以获得更好性能
- **数据量 ≥ 100,000**: 构建并使用 IVF_FLAT 索引

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

## 总结

Milvus Lite 是学习和开发向量数据库应用的理想选择，它提供了：

1. **零配置启动**：无需复杂的部署设置
2. **完整功能**：支持向量搜索的核心功能
3. **API 一致性**：与其他 Milvus 部署方式保持一致
4. **易于迁移**：可以轻松迁移到生产环境

通过 Milvus Lite，你可以快速开始向量数据库的学习和开发，为后续的生产部署打下坚实基础。