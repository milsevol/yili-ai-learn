# Milvus Lite 演示代码

本文件夹包含了 Milvus Lite 的完整演示代码，展示了如何在本地环境中使用 Milvus Lite 进行向量数据库操作。

## 文件说明

### 核心演示文件

1. **`01_basic_usage.py`** - Milvus Lite 基础使用演示
   - 客户端连接
   - 集合创建和管理
   - 数据插入和索引创建
   - 基础向量搜索
   - 带过滤条件的搜索
   - 数据查询和删除

2. **`02_advanced_features.py`** - 高级功能演示
   - 批量数据操作
   - 复杂搜索条件
   - 性能分析和优化
   - 数据管理和统计
   - 数据导出功能

3. **`03_langchain_integration.py`** - LangChain 集成演示
   - 与 LangChain 框架集成
   - 文档向量化和存储
   - 检索器使用
   - 元数据过滤
   - 性能对比

### 配置文件

4. **`README.md`** - 本说明文件

**注意**: 项目依赖包列表位于项目根目录的 `requirements.txt` 文件中。

## 快速开始

### 1. 安装依赖

```bash
# 进入项目根目录
cd /Users/cuixueyong/code/github/yili-ai-learn

# 安装项目依赖包
pip install -r requirements.txt

# 或者直接安装项目（开发模式）
pip install -e .
```

### 2. 运行基础演示

```bash
# 运行基础使用演示
python 01_basic_usage.py
```

这将演示：
- 创建 Milvus Lite 客户端
- 创建集合并插入 1000 条示例数据
- 执行向量搜索和过滤搜索
- 数据查询和管理操作

### 3. 运行高级功能演示

```bash
# 运行高级功能演示
python 02_advanced_features.py
```

这将演示：
- 批量插入 5000 条数据
- 复杂的搜索和过滤条件
- 性能分析和优化建议
- 数据统计和管理

### 4. 运行 LangChain 集成演示

```bash
# 运行 LangChain 集成演示
python 03_langchain_integration.py
```

这将演示：
- 与 LangChain 框架的集成
- 文档向量化和相似性搜索
- 不同类型的检索器使用
- 元数据过滤和文档管理

## 演示数据说明

### 基础演示数据结构
```python
{
    "id": int,           # 唯一标识符
    "vector": List[float], # 向量数据
    "text": str,         # 文本内容
    "category": str,     # 类别
    "score": int         # 评分
}
```

### 高级演示数据结构
```python
{
    "id": int,              # 唯一标识符
    "vector": List[float],  # 归一化向量
    "title": str,           # 标题
    "content": str,         # 内容
    "category": str,        # 类别
    "source": str,          # 来源
    "publish_year": int,    # 发布年份
    "view_count": int,      # 浏览量
    "rating": float         # 评分
}
```

### LangChain 文档结构
```python
Document(
    page_content=str,       # 文档内容
    metadata={              # 元数据
        "category": str,    # 类别
        "source": str,      # 来源
        "difficulty": str,  # 难度级别
        "year": int         # 年份（可选）
    }
)
```

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