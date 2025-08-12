"""
Zilliz Cloud 连接管理模块

提供连接池、重连机制、健康检查等功能
"""

import time
import threading
from queue import Queue, Empty
from datetime import datetime
from pymilvus import MilvusClient
from loguru import logger
from .settings import config


class ZillizCloudConnector:
    """Zilliz Cloud 连接器"""
    
    def __init__(self, uri=None, token=None, timeout=None, retry_times=None):
        self.uri = uri or config.URI
        self.token = token or config.TOKEN
        self.timeout = timeout or config.CONNECTION_TIMEOUT
        self.retry_times = retry_times or config.MAX_RETRIES
        self.client = None
        self._lock = threading.Lock()
    
    def connect(self):
        """建立连接"""
        with self._lock:
            for attempt in range(self.retry_times):
                try:
                    logger.info(f"尝试连接 Zilliz Cloud (第 {attempt + 1}/{self.retry_times} 次)")
                    
                    self.client = MilvusClient(
                        uri=self.uri,
                        token=self.token,
                        timeout=self.timeout
                    )
                    
                    # 验证连接
                    self.client.list_collections()
                    logger.success(f"连接成功 (尝试 {attempt + 1}/{self.retry_times})")
                    return True
                    
                except Exception as e:
                    logger.warning(f"连接失败 (尝试 {attempt + 1}/{self.retry_times}): {e}")
                    if attempt == self.retry_times - 1:
                        logger.error("所有连接尝试都失败了")
                        raise e
                    time.sleep(2 ** attempt)  # 指数退避
            
            return False
    
    def get_client(self):
        """获取客户端"""
        if self.client is None:
            self.connect()
        return self.client
    
    def health_check(self):
        """健康检查"""
        try:
            if self.client:
                collections = self.client.list_collections()
                return {
                    "status": "healthy",
                    "collections_count": len(collections),
                    "timestamp": datetime.now().isoformat(),
                    "uri": self.uri[:50] + "..." if len(self.uri) > 50 else self.uri
                }
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "uri": self.uri[:50] + "..." if len(self.uri) > 50 else self.uri
            }
    
    def reconnect(self):
        """重新连接"""
        logger.info("尝试重新连接...")
        self.client = None
        return self.connect()


class ConnectionPool:
    """Zilliz Cloud 连接池"""
    
    def __init__(self, uri=None, token=None, pool_size=None, max_retries=None):
        self.uri = uri or config.URI
        self.token = token or config.TOKEN
        self.pool_size = pool_size or config.POOL_SIZE
        self.max_retries = max_retries or config.MAX_RETRIES
        self.pool = Queue(maxsize=self.pool_size)
        self.lock = threading.Lock()
        self.created_connections = 0
        
        logger.info(f"初始化连接池，大小: {self.pool_size}")
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化连接池"""
        for i in range(self.pool_size):
            try:
                client = MilvusClient(uri=self.uri, token=self.token)
                # 测试连接
                client.list_collections()
                self.pool.put(client)
                self.created_connections += 1
                logger.debug(f"创建连接 {i + 1}/{self.pool_size}")
            except Exception as e:
                logger.error(f"创建连接失败: {e}")
        
        logger.info(f"连接池初始化完成，成功创建 {self.created_connections} 个连接")
    
    def get_connection(self, timeout=30):
        """获取连接"""
        try:
            # 尝试从池中获取连接
            client = self.pool.get(timeout=timeout)
            
            # 验证连接是否有效
            try:
                client.list_collections()
                return client
            except Exception:
                # 连接无效，创建新连接
                logger.warning("连接无效，创建新连接")
                return self._create_new_connection()
                
        except Empty:
            # 池中没有可用连接，创建新连接
            logger.warning("连接池为空，创建新连接")
            return self._create_new_connection()
    
    def _create_new_connection(self):
        """创建新连接"""
        for attempt in range(self.max_retries):
            try:
                client = MilvusClient(uri=self.uri, token=self.token)
                client.list_collections()  # 验证连接
                logger.debug("创建新连接成功")
                return client
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"创建新连接失败: {e}")
                    raise e
                time.sleep(2 ** attempt)
    
    def return_connection(self, client):
        """归还连接"""
        try:
            # 验证连接是否仍然有效
            client.list_collections()
            self.pool.put_nowait(client)
            logger.debug("连接已归还到池中")
        except Exception as e:
            # 连接无效，不归还到池中
            logger.warning(f"连接无效，不归还到池中: {e}")
    
    def get_pool_status(self):
        """获取连接池状态"""
        return {
            "pool_size": self.pool_size,
            "available_connections": self.pool.qsize(),
            "created_connections": self.created_connections,
            "timestamp": datetime.now().isoformat()
        }
    
    def close_all(self):
        """关闭所有连接"""
        logger.info("关闭连接池中的所有连接")
        closed_count = 0
        while not self.pool.empty():
            try:
                client = self.pool.get_nowait()
                # Milvus 客户端通常不需要显式关闭
                del client
                closed_count += 1
            except Empty:
                break
        
        logger.info(f"已关闭 {closed_count} 个连接")


class PooledConnection:
    """连接池上下文管理器"""
    
    def __init__(self, pool):
        self.pool = pool
        self.client = None
    
    def __enter__(self):
        self.client = self.pool.get_connection()
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.pool.return_connection(self.client)


# 全局连接实例
_global_connector = None
_global_pool = None


def get_connector():
    """获取全局连接器"""
    global _global_connector
    if _global_connector is None:
        _global_connector = ZillizCloudConnector()
    return _global_connector


def get_pool():
    """获取全局连接池"""
    global _global_pool
    if _global_pool is None:
        _global_pool = ConnectionPool()
    return _global_pool


def get_client():
    """获取客户端（使用全局连接器）"""
    connector = get_connector()
    return connector.get_client()


def test_connection():
    """测试连接"""
    try:
        connector = get_connector()
        health = connector.health_check()
        
        print("=== 连接测试结果 ===")
        print(f"状态: {health['status']}")
        print(f"时间: {health['timestamp']}")
        print(f"URI: {health['uri']}")
        
        if health['status'] == 'healthy':
            print(f"集合数量: {health['collections_count']}")
            print("✅ 连接测试成功")
        else:
            print(f"错误: {health.get('error', '未知错误')}")
            print("❌ 连接测试失败")
        
        return health['status'] == 'healthy'
        
    except Exception as e:
        print(f"❌ 连接测试异常: {e}")
        return False


if __name__ == "__main__":
    # 测试连接
    test_connection()
    
    # 测试连接池
    print("\n=== 连接池测试 ===")
    pool = get_pool()
    status = pool.get_pool_status()
    print(f"连接池状态: {status}")
    
    # 使用连接池
    with PooledConnection(pool) as client:
        collections = client.list_collections()
        print(f"集合列表: {collections}")
    
    print("✅ 连接池测试完成")