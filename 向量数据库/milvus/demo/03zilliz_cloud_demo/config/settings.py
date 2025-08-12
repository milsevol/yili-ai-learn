"""
Zilliz Cloud 配置文件

使用环境变量来配置连接信息，确保安全性
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ZillizCloudConfig:
    """Zilliz Cloud 配置类"""
    
    # 连接配置
    URI = os.getenv("ZILLIZ_CLOUD_URI", "")
    TOKEN = os.getenv("ZILLIZ_CLOUD_TOKEN", "")
    
    # API 配置
    API_KEY = os.getenv("ZILLIZ_API_KEY", "")
    CLUSTER_ID = os.getenv("ZILLIZ_CLUSTER_ID", "")
    
    # 连接池配置
    POOL_SIZE = int(os.getenv("ZILLIZ_POOL_SIZE", "5"))
    CONNECTION_TIMEOUT = int(os.getenv("ZILLIZ_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("ZILLIZ_MAX_RETRIES", "3"))
    
    # 性能监控配置
    MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", "60"))  # 秒
    MONITOR_DURATION = int(os.getenv("MONITOR_DURATION", "3600"))  # 秒
    
    # 成本管理配置
    COST_ALERT_THRESHOLD = float(os.getenv("COST_ALERT_THRESHOLD", "100.0"))  # 美元
    DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "90"))
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "zilliz_cloud.log")
    
    # 测试数据配置
    TEST_COLLECTION_NAME = os.getenv("TEST_COLLECTION_NAME", "test_collection")
    TEST_VECTOR_DIM = int(os.getenv("TEST_VECTOR_DIM", "128"))
    TEST_DATA_SIZE = int(os.getenv("TEST_DATA_SIZE", "1000"))
    
    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        required_fields = ["URI", "TOKEN"]
        missing_fields = []
        
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"缺少必要的配置项: {', '.join(missing_fields)}")
        
        return True
    
    @classmethod
    def get_connection_config(cls):
        """获取连接配置"""
        cls.validate()
        return {
            "uri": cls.URI,
            "token": cls.TOKEN,
            "timeout": cls.CONNECTION_TIMEOUT
        }
    
    @classmethod
    def get_api_config(cls):
        """获取API配置"""
        return {
            "api_key": cls.API_KEY,
            "cluster_id": cls.CLUSTER_ID
        }
    
    @classmethod
    def print_config(cls):
        """打印配置信息（隐藏敏感信息）"""
        print("=== Zilliz Cloud 配置信息 ===")
        print(f"URI: {cls.URI[:30]}..." if cls.URI else "URI: 未设置")
        print(f"TOKEN: {'*' * 20}" if cls.TOKEN else "TOKEN: 未设置")
        print(f"API_KEY: {'*' * 20}" if cls.API_KEY else "API_KEY: 未设置")
        print(f"CLUSTER_ID: {cls.CLUSTER_ID}")
        print(f"连接池大小: {cls.POOL_SIZE}")
        print(f"连接超时: {cls.CONNECTION_TIMEOUT}秒")
        print(f"最大重试次数: {cls.MAX_RETRIES}")
        print(f"监控间隔: {cls.MONITOR_INTERVAL}秒")
        print(f"测试集合名: {cls.TEST_COLLECTION_NAME}")
        print(f"测试向量维度: {cls.TEST_VECTOR_DIM}")
        print("=" * 30)

# 创建全局配置实例
config = ZillizCloudConfig()

# 示例环境变量文件内容（.env）
ENV_EXAMPLE = """
# Zilliz Cloud 连接配置
ZILLIZ_CLOUD_URI=https://your-cluster-endpoint.zillizcloud.com:19530
ZILLIZ_CLOUD_TOKEN=your-api-token

# Zilliz Cloud API 配置
ZILLIZ_API_KEY=your-api-key
ZILLIZ_CLUSTER_ID=your-cluster-id

# 连接池配置
ZILLIZ_POOL_SIZE=5
ZILLIZ_TIMEOUT=30
ZILLIZ_MAX_RETRIES=3

# 监控配置
MONITOR_INTERVAL=60
MONITOR_DURATION=3600

# 成本管理配置
COST_ALERT_THRESHOLD=100.0
DATA_RETENTION_DAYS=90

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=zilliz_cloud.log

# 测试配置
TEST_COLLECTION_NAME=test_collection
TEST_VECTOR_DIM=128
TEST_DATA_SIZE=1000
"""

if __name__ == "__main__":
    # 打印配置信息
    config.print_config()
    
    # 创建示例环境变量文件
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(ENV_EXAMPLE)
    
    print("\n已创建 .env.example 文件，请复制为 .env 并填入实际配置")