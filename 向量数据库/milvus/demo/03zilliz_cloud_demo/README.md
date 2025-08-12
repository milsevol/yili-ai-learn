# Zilliz Cloud 云端向量数据库实战代码示例

本目录包含 Zilliz Cloud 学习文档的配套代码示例，帮助你快速上手云端向量数据库的使用。

## 📁 文件结构

```
03zilliz_cloud_demo/
├── README.md                          # 本文件
├── requirements.txt                   # 依赖包列表
├── config/
│   ├── __init__.py
│   ├── settings.py                    # 配置文件
│   └── connection.py                  # 连接管理
├── 01_cluster_management.py           # 集群创建与管理
├── 02_connection_auth.py              # 连接配置与认证
├── 03_cloud_features.py               # 云端特有功能
├── 04_performance_monitoring.py       # 性能优化与监控
├── 05_cost_management.py              # 成本管理与计费
├── 06_enterprise_features.py          # 企业级应用实战
├── utils/
│   ├── __init__.py
│   ├── data_generator.py              # 测试数据生成
│   ├── performance_monitor.py         # 性能监控工具
│   └── cost_analyzer.py               # 成本分析工具
└── run_all_demos.py                   # 运行所有示例
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export ZILLIZ_CLOUD_URI="https://your-cluster-endpoint.zillizcloud.com:19530"
export ZILLIZ_CLOUD_TOKEN="your-api-token"
export ZILLIZ_API_KEY="your-api-key"
export ZILLIZ_CLUSTER_ID="your-cluster-id"
```

### 2. 配置文件

复制 `config/settings.py.example` 为 `config/settings.py` 并填入你的配置信息。

### 3. 运行示例

```bash
# 运行单个示例
python 01_cluster_management.py

# 运行所有示例
python run_all_demos.py
```

## 📚 学习路径

### 第一步：基础连接 (必须)
- `02_connection_auth.py` - 学习如何连接 Zilliz Cloud

### 第二步：集群管理
- `01_cluster_management.py` - 集群创建、配置和监控

### 第三步：云端功能
- `03_cloud_features.py` - 自动扩缩容、备份恢复等

### 第四步：性能优化
- `04_performance_monitoring.py` - 性能监控和查询优化

### 第五步：成本控制
- `05_cost_management.py` - 成本分析和优化建议

### 第六步：企业应用
- `06_enterprise_features.py` - 高可用、数据治理、安全管理

## 🔧 工具说明

### 性能监控工具
```python
from utils.performance_monitor import ZillizPerformanceMonitor

monitor = ZillizPerformanceMonitor(client)
monitor.monitor_continuous("my_collection", interval=30, duration=1800)
```

### 成本分析工具
```python
from utils.cost_analyzer import CostAnalyzer

analyzer = CostAnalyzer("your-api-key")
report = analyzer.generate_cost_report("your-cluster-id", "2024-12")
```

## 📖 对应文档

本代码示例对应学习文档：
- 📄 [03Zilliz Cloud云端向量数据库实战.md](../../03Zilliz%20Cloud云端向量数据库实战.md)

## ⚠️ 注意事项

1. **成本控制**: Zilliz Cloud 按使用量计费，请注意控制测试规模
2. **数据安全**: 不要在代码中硬编码敏感信息，使用环境变量
3. **资源清理**: 测试完成后及时清理不需要的集合和数据
4. **网络连接**: 确保网络连接稳定，云端操作可能需要较长时间

## 🆘 常见问题

### Q: 连接失败怎么办？
A: 检查 URI 和 Token 是否正确，确认集群状态是否正常

### Q: 如何控制成本？
A: 使用小规模数据测试，及时清理资源，启用自动扩缩容

### Q: 性能不佳怎么优化？
A: 参考性能监控工具的建议，优化索引和查询参数

## 📞 技术支持

- [Zilliz Cloud 官方文档](https://docs.zilliz.com/)
- [技术论坛](https://discuss.milvus.io/)
- [GitHub Issues](https://github.com/zilliztech/zilliz-cloud-python)