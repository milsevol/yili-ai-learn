# Zilliz Cloud 云端向量数据库实战

## 目录
1. [Zilliz Cloud 简介](#zilliz-cloud-简介)
2. [环境准备与账户设置](#环境准备与账户设置)
3. [云端集群创建与管理](#云端集群创建与管理)
4. [连接配置与认证](#连接配置与认证)
5. [云端特有功能](#云端特有功能)
6. [性能优化与监控](#性能优化与监控)
7. [成本管理与计费](#成本管理与计费)
8. [企业级功能](#企业级功能)
9. [迁移指南](#迁移指南)
10. [最佳实践](#最佳实践)
11. [故障排除](#故障排除)
12. [学习路径总结](#学习路径总结)

---

## Zilliz Cloud 简介

### 什么是 Zilliz Cloud？

Zilliz Cloud 是 Milvus 的官方云服务，提供完全托管的向量数据库解决方案。它基于开源的 Milvus 构建，但提供了更多企业级功能和云原生特性。

### 核心优势

#### 1. 完全托管
- **自动化运维**：无需管理基础设施
- **自动扩缩容**：根据负载自动调整资源
- **高可用性**：内置故障转移和备份机制
- **安全保障**：企业级安全和合规性

#### 2. 性能优化
- **分布式架构**：支持大规模数据处理
- **智能索引**：自动选择最优索引策略
- **缓存优化**：多层缓存提升查询性能
- **网络优化**：全球CDN加速

#### 3. 企业功能
- **多租户支持**：资源隔离和权限管理
- **监控告警**：实时性能监控和告警
- **数据治理**：数据血缘和质量管理
- **API网关**：统一接口管理

### 与本地 Milvus 的对比

| 特性 | 本地 Milvus | Zilliz Cloud |
|------|-------------|--------------|
| 部署方式 | 自行部署 | 完全托管 |
| 运维成本 | 需要专业运维 | 零运维 |
| 扩展性 | 手动扩展 | 自动扩缩容 |
| 高可用 | 需要自建 | 内置高可用 |
| 安全性 | 自行配置 | 企业级安全 |
| 监控 | 需要自建 | 内置监控 |
| 成本 | 硬件+人力 | 按需付费 |

---

## 环境准备与账户设置

### 1. 注册 Zilliz Cloud 账户

#### 访问官网
```
https://cloud.zilliz.com/
```

#### 注册流程
1. **创建账户**
   - 使用邮箱注册
   - 验证邮箱地址
   - 设置强密码

2. **完善信息**
   - 填写基本信息
   - 选择使用场景
   - 配置计费信息

3. **获取免费额度**
   - 新用户免费额度
   - 试用期限制
   - 升级选项

### 2. 安装客户端工具

#### Python SDK
```bash
# 安装 Zilliz Cloud 专用 SDK
pip install pymilvus[cloud]

# 或者使用标准 pymilvus
pip install pymilvus>=2.3.0
```

#### 其他语言 SDK
```bash
# Node.js
npm install @zilliz/milvus2-sdk-node

# Java
# 在 pom.xml 中添加依赖
<dependency>
    <groupId>io.milvus</groupId>
    <artifactId>milvus-sdk-java</artifactId>
    <version>2.3.0</version>
</dependency>

# Go
go get github.com/milvus-io/milvus-sdk-go/v2
```

### 3. 环境配置

#### 创建配置文件
```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class ZillizConfig:
    """Zilliz Cloud 配置"""
    # 连接信息
    uri: str = os.getenv('ZILLIZ_URI', '')
    token: str = os.getenv('ZILLIZ_TOKEN', '')
    
    # 集群信息
    cluster_id: str = os.getenv('ZILLIZ_CLUSTER_ID', '')
    region: str = os.getenv('ZILLIZ_REGION', 'aws-us-west-2')
    
    # 安全配置
    secure: bool = True
    timeout: int = 30
    
    # 性能配置
    pool_size: int = 10
    retry_times: int = 3

# 环境变量配置示例
# export ZILLIZ_URI="https://your-cluster.zillizcloud.com:19530"
# export ZILLIZ_TOKEN="your-api-token"
# export ZILLIZ_CLUSTER_ID="your-cluster-id"
```

---

## 云端集群创建与管理

### 1. 创建集群

#### 通过 Web 控制台
1. **登录控制台**
   - 访问 Zilliz Cloud 控制台
   - 使用账户登录

2. **创建集群**
   - 点击"Create Cluster"
   - 选择集群类型
   - 配置规格参数

3. **配置选项**
   ```yaml
   集群配置:
     名称: my-vector-cluster
     区域: aws-us-west-2
     规格: 
       - Starter: 1 CU (适合开发测试)
       - Standard: 2-8 CU (适合生产环境)
       - Enterprise: 8+ CU (适合大规模应用)
     存储: 
       - 类型: SSD
       - 大小: 100GB - 10TB
     网络:
       - VPC: 默认或自定义
       - 安全组: 自动配置
   ```

#### 通过 API 创建
```python
import requests
import json

def create_cluster_via_api(api_key, cluster_config):
    """通过 API 创建集群"""
    url = "https://controller.api.zillizcloud.com/v1/clusters"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "clusterName": cluster_config["name"],
        "region": cluster_config["region"],
        "plan": cluster_config["plan"],
        "cuSize": cluster_config["cu_size"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        cluster_info = response.json()
        print(f"集群创建成功: {cluster_info['clusterId']}")
        return cluster_info
    else:
        print(f"集群创建失败: {response.text}")
        return None

# 使用示例
cluster_config = {
    "name": "my-vector-cluster",
    "region": "aws-us-west-2",
    "plan": "Standard",
    "cu_size": 2
}

# cluster_info = create_cluster_via_api("your-api-key", cluster_config)
```

### 2. 集群管理

#### 集群状态监控
```python
from pymilvus import connections, utility
from datetime import datetime
import time

class ZillizClusterManager:
    """Zilliz Cloud 集群管理器"""
    
    def __init__(self, config):
        self.config = config
        self.connection_name = "zilliz_cloud"
    
    def connect(self):
        """连接到 Zilliz Cloud"""
        try:
            connections.connect(
                alias=self.connection_name,
                uri=self.config.uri,
                token=self.config.token,
                secure=self.config.secure,
                timeout=self.config.timeout
            )
            print("✅ 成功连接到 Zilliz Cloud")
            return True
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def get_cluster_info(self):
        """获取集群信息"""
        try:
            # 获取版本信息
            version = utility.get_server_version(using=self.connection_name)
            
            # 获取集合列表
            collections = utility.list_collections(using=self.connection_name)
            
            cluster_info = {
                "timestamp": datetime.now().isoformat(),
                "version": version,
                "collections_count": len(collections),
                "collections": collections,
                "status": "healthy"
            }
            
            return cluster_info
            
        except Exception as e:
            print(f"获取集群信息失败: {e}")
            return None
    
    def monitor_cluster(self, interval=60):
        """监控集群状态"""
        print("开始监控集群状态...")
        
        while True:
            try:
                info = self.get_cluster_info()
                if info:
                    print(f"[{info['timestamp']}] 集群状态: {info['status']}")
                    print(f"  版本: {info['version']}")
                    print(f"  集合数量: {info['collections_count']}")
                else:
                    print(f"[{datetime.now()}] 集群状态检查失败")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("停止监控")
                break
            except Exception as e:
                print(f"监控异常: {e}")
                time.sleep(interval)

# 使用示例
# config = ZillizConfig()
# manager = ZillizClusterManager(config)
# if manager.connect():
#     info = manager.get_cluster_info()
#     print(json.dumps(info, indent=2, ensure_ascii=False))
```

#### 集群扩缩容
```python
def scale_cluster(cluster_id, new_cu_size, api_key):
    """集群扩缩容"""
    url = f"https://controller.api.zillizcloud.com/v1/clusters/{cluster_id}/scale"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "cuSize": new_cu_size
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(f"集群扩缩容成功，新规格: {new_cu_size} CU")
        return True
    else:
        print(f"扩缩容失败: {response.text}")
        return False

# 使用示例
# scale_cluster("your-cluster-id", 4, "your-api-key")
```

---

## 连接配置与认证

### 1. 连接方式

#### 基础连接配置
```python
from pymilvus import MilvusClient
import os

# 方式1: 直接配置连接参数
client = MilvusClient(
    uri="https://your-cluster-endpoint.zillizcloud.com:19530",
    token="your-api-token"
)

# 方式2: 使用环境变量
os.environ["ZILLIZ_CLOUD_URI"] = "https://your-cluster-endpoint.zillizcloud.com:19530"
os.environ["ZILLIZ_CLOUD_TOKEN"] = "your-api-token"

client = MilvusClient(
    uri=os.getenv("ZILLIZ_CLOUD_URI"),
    token=os.getenv("ZILLIZ_CLOUD_TOKEN")
)

# 测试连接
try:
    collections = client.list_collections()
    print(f"连接成功！当前集合: {collections}")
except Exception as e:
    print(f"连接失败: {e}")
```

#### 高级连接配置
```python
class ZillizCloudConnector:
    """Zilliz Cloud 连接器"""
    
    def __init__(self, uri, token, timeout=30, retry_times=3):
        self.uri = uri
        self.token = token
        self.timeout = timeout
        self.retry_times = retry_times
        self.client = None
    
    def connect(self):
        """建立连接"""
        for attempt in range(self.retry_times):
            try:
                self.client = MilvusClient(
                    uri=self.uri,
                    token=self.token,
                    timeout=self.timeout
                )
                
                # 验证连接
                self.client.list_collections()
                print(f"连接成功 (尝试 {attempt + 1}/{self.retry_times})")
                return True
                
            except Exception as e:
                print(f"连接失败 (尝试 {attempt + 1}/{self.retry_times}): {e}")
                if attempt == self.retry_times - 1:
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
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# 使用示例
connector = ZillizCloudConnector(
    uri="https://your-cluster-endpoint.zillizcloud.com:19530",
    token="your-api-token",
    timeout=60,
    retry_times=5
)

client = connector.get_client()
health = connector.health_check()
print(f"集群状态: {health}")
```

### 2. API Token 管理

#### Token 生成与管理
```python
import requests
import json
from datetime import datetime, timedelta

class TokenManager:
    """API Token 管理器"""
    
    def __init__(self, api_key, cluster_id):
        self.api_key = api_key
        self.cluster_id = cluster_id
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def create_token(self, token_name, expiry_days=30):
        """创建新的 API Token"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/tokens"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        
        payload = {
            "tokenName": token_name,
            "expiryTime": expiry_date.isoformat()
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            token_info = response.json()
            print(f"Token 创建成功: {token_name}")
            return token_info
        else:
            print(f"Token 创建失败: {response.text}")
            return None
    
    def list_tokens(self):
        """列出所有 Token"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/tokens"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            tokens = response.json()
            print("当前 Token 列表:")
            for token in tokens.get("tokens", []):
                print(f"  - {token['tokenName']}: {token['status']} (过期: {token['expiryTime']})")
            return tokens
        else:
            print(f"获取 Token 列表失败: {response.text}")
            return None
    
    def revoke_token(self, token_name):
        """撤销 Token"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/tokens/{token_name}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 200:
            print(f"Token '{token_name}' 已撤销")
            return True
        else:
            print(f"撤销 Token 失败: {response.text}")
            return False
    
    def rotate_token(self, old_token_name, new_token_name, expiry_days=30):
        """轮换 Token"""
        # 创建新 Token
        new_token = self.create_token(new_token_name, expiry_days)
        
        if new_token:
            print(f"新 Token 创建成功，请更新应用配置")
            print(f"新 Token: {new_token.get('token', 'N/A')}")
            
            # 可以选择立即撤销旧 Token 或设置延迟撤销
            confirm = input(f"是否立即撤销旧 Token '{old_token_name}'? (y/n): ")
            if confirm.lower() == 'y':
                self.revoke_token(old_token_name)
            
            return new_token
        
        return None

# 使用示例
# token_manager = TokenManager("your-api-key", "your-cluster-id")
# new_token = token_manager.create_token("production-token", 90)
# tokens = token_manager.list_tokens()
```

### 3. 连接池管理

#### 连接池实现
```python
import threading
from queue import Queue, Empty
import time

class ConnectionPool:
    """Zilliz Cloud 连接池"""
    
    def __init__(self, uri, token, pool_size=10, max_retries=3):
        self.uri = uri
        self.token = token
        self.pool_size = pool_size
        self.max_retries = max_retries
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        self.created_connections = 0
        
        # 预创建连接
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化连接池"""
        for _ in range(self.pool_size):
            try:
                client = MilvusClient(uri=self.uri, token=self.token)
                # 测试连接
                client.list_collections()
                self.pool.put(client)
                self.created_connections += 1
            except Exception as e:
                print(f"创建连接失败: {e}")
    
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
                return self._create_new_connection()
                
        except Empty:
            # 池中没有可用连接，创建新连接
            return self._create_new_connection()
    
    def _create_new_connection(self):
        """创建新连接"""
        for attempt in range(self.max_retries):
            try:
                client = MilvusClient(uri=self.uri, token=self.token)
                client.list_collections()  # 验证连接
                return client
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
    
    def return_connection(self, client):
        """归还连接"""
        try:
            # 验证连接是否仍然有效
            client.list_collections()
            self.pool.put_nowait(client)
        except Exception:
            # 连接无效，不归还到池中
            pass
    
    def close_all(self):
        """关闭所有连接"""
        while not self.pool.empty():
            try:
                client = self.pool.get_nowait()
                # Milvus 客户端通常不需要显式关闭
                del client
            except Empty:
                break

# 连接池上下文管理器
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

# 使用示例
pool = ConnectionPool(
    uri="https://your-cluster-endpoint.zillizcloud.com:19530",
    token="your-api-token",
    pool_size=5
)

# 使用连接池
with PooledConnection(pool) as client:
    collections = client.list_collections()
    print(f"集合列表: {collections}")

# 批量操作示例
def batch_search_with_pool(pool, vectors, collection_name):
    """使用连接池进行批量搜索"""
    results = []
    
    for vector_batch in vectors:
        with PooledConnection(pool) as client:
            result = client.search(
                collection_name=collection_name,
                data=vector_batch,
                limit=10
            )
            results.extend(result)
    
    return results
```

---

## 企业级应用实战

### 1. 高可用架构设计

#### 多集群容灾方案
```python
class DisasterRecoveryManager:
    """容灾管理器"""
    
    def __init__(self, primary_config, backup_config):
        self.primary_client = MilvusClient(**primary_config)
        self.backup_client = MilvusClient(**backup_config)
        self.is_primary_healthy = True
    
    def health_check(self):
        """健康检查"""
        try:
            # 检查主集群
            self.primary_client.list_collections()
            primary_healthy = True
        except Exception as e:
            print(f"主集群健康检查失败: {e}")
            primary_healthy = False
        
        try:
            # 检查备份集群
            self.backup_client.list_collections()
            backup_healthy = True
        except Exception as e:
            print(f"备份集群健康检查失败: {e}")
            backup_healthy = False
        
        return {
            "primary": primary_healthy,
            "backup": backup_healthy,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_active_client(self):
        """获取活跃客户端"""
        health = self.health_check()
        
        if health["primary"]:
            return self.primary_client, "primary"
        elif health["backup"]:
            print("主集群不可用，切换到备份集群")
            return self.backup_client, "backup"
        else:
            raise Exception("所有集群都不可用")
    
    def sync_data(self, collection_name):
        """数据同步"""
        try:
            # 从主集群获取数据
            primary_data = self.primary_client.query(
                collection_name=collection_name,
                filter="",
                output_fields=["*"]
            )
            
            # 同步到备份集群
            if primary_data:
                self.backup_client.insert(
                    collection_name=collection_name,
                    data=primary_data
                )
                print(f"同步了 {len(primary_data)} 条数据到备份集群")
            
        except Exception as e:
            print(f"数据同步失败: {e}")

# 使用示例
# primary_config = {"uri": "primary-cluster-uri", "token": "primary-token"}
# backup_config = {"uri": "backup-cluster-uri", "token": "backup-token"}
# dr_manager = DisasterRecoveryManager(primary_config, backup_config)
# client, cluster_type = dr_manager.get_active_client()
```

### 2. 数据治理与合规

#### 数据生命周期管理
```python
class DataLifecycleManager:
    """数据生命周期管理器"""
    
    def __init__(self, client):
        self.client = client
    
    def setup_data_retention_policy(self, collection_name, retention_days=90):
        """设置数据保留策略"""
        policy = {
            "collection_name": collection_name,
            "retention_days": retention_days,
            "created_at": datetime.now().isoformat()
        }
        
        # 在实际应用中，这里会存储到配置数据库
        print(f"为集合 '{collection_name}' 设置 {retention_days} 天数据保留策略")
        return policy
    
    def cleanup_expired_data(self, collection_name, retention_days=90):
        """清理过期数据"""
        try:
            # 计算过期时间戳
            expiry_date = datetime.now() - timedelta(days=retention_days)
            expiry_timestamp = int(expiry_date.timestamp())
            
            # 删除过期数据
            expr = f"timestamp < {expiry_timestamp}"
            result = self.client.delete(
                collection_name=collection_name,
                filter=expr
            )
            
            print(f"清理了 {result.delete_count} 条过期数据")
            return result.delete_count
            
        except Exception as e:
            print(f"清理过期数据失败: {e}")
            return 0
    
    def audit_data_access(self, collection_name, operation, user_id):
        """审计数据访问"""
        audit_record = {
            "timestamp": datetime.now().isoformat(),
            "collection_name": collection_name,
            "operation": operation,
            "user_id": user_id,
            "ip_address": "127.0.0.1"  # 实际应用中获取真实IP
        }
        
        # 在实际应用中，这里会存储到审计日志系统
        print(f"审计记录: {audit_record}")
        return audit_record

# 使用示例
# lifecycle_manager = DataLifecycleManager(client)
# lifecycle_manager.setup_data_retention_policy("user_vectors", 180)
# lifecycle_manager.cleanup_expired_data("user_vectors", 90)
```

### 3. 安全最佳实践

#### 访问控制与权限管理
```python
class SecurityManager:
    """安全管理器"""
    
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key
    
    def create_role_based_access(self, role_name, permissions):
        """创建基于角色的访问控制"""
        role_config = {
            "role_name": role_name,
            "permissions": permissions,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"创建角色 '{role_name}' 权限配置:")
        for permission in permissions:
            print(f"  - {permission}")
        
        return role_config
    
    def encrypt_sensitive_data(self, data, key=None):
        """加密敏感数据"""
        from cryptography.fernet import Fernet
        
        if key is None:
            key = Fernet.generate_key()
        
        f = Fernet(key)
        
        if isinstance(data, str):
            encrypted_data = f.encrypt(data.encode())
        else:
            encrypted_data = f.encrypt(str(data).encode())
        
        return {
            "encrypted_data": encrypted_data,
            "key": key
        }
    
    def setup_network_security(self, allowed_ips):
        """设置网络安全"""
        security_config = {
            "allowed_ips": allowed_ips,
            "ssl_enabled": True,
            "token_rotation_interval": 30,  # 天
            "max_connections": 100
        }
        
        print("网络安全配置:")
        for key, value in security_config.items():
            print(f"  {key}: {value}")
        
        return security_config

# 使用示例
# security_manager = SecurityManager(client, "your-api-key")
# role_config = security_manager.create_role_based_access(
#     "data_analyst", 
#     ["read_collections", "search_vectors", "view_stats"]
# )
```

---

## 学习总结与进阶路径

### 1. 知识体系总结

#### Zilliz Cloud 核心能力
- **云原生架构**: 自动扩缩容、多区域部署、高可用性
- **企业级功能**: 数据备份、监控告警、成本管理
- **开发者友好**: 丰富的API、多语言SDK、完善的文档
- **性能优化**: 智能索引选择、查询优化、批量处理

#### 与本地 Milvus 的对比
| 特性 | 本地 Milvus | Zilliz Cloud |
|------|-------------|--------------|
| 部署复杂度 | 高 | 低 |
| 运维成本 | 高 | 低 |
| 扩展性 | 手动 | 自动 |
| 可用性 | 需自建 | 内置高可用 |
| 成本 | 固定 | 按需付费 |
| 安全性 | 需自配置 | 企业级安全 |

### 2. 实战项目建议

#### 初级项目
1. **智能文档搜索系统**
   - 使用 Zilliz Cloud 存储文档向量
   - 实现语义搜索功能
   - 集成成本监控

2. **商品推荐引擎**
   - 构建商品特征向量
   - 实现相似商品推荐
   - 优化查询性能

#### 中级项目
1. **多模态内容检索**
   - 支持文本、图像、音频检索
   - 实现跨模态搜索
   - 部署多区域架构

2. **实时推荐系统**
   - 实时向量更新
   - 低延迟查询优化
   - 自动扩缩容配置

#### 高级项目
1. **企业级RAG系统**
   - 大规模知识库构建
   - 混合检索策略
   - 完整的数据治理

2. **AI驱动的搜索平台**
   - 多租户架构
   - 智能查询优化
   - 全面的监控体系

### 3. 学习资源推荐

#### 官方资源
- [Zilliz Cloud 官方文档](https://docs.zilliz.com/)
- [Milvus 社区](https://milvus.io/community)
- [技术博客](https://zilliz.com/blog)

#### 实践资源
- [GitHub 示例项目](https://github.com/zilliztech)
- [在线教程](https://zilliz.com/learn)
- [技术论坛](https://discuss.milvus.io/)

### 4. 下一步学习方向

#### 深度学习方向
1. **向量化技术**
   - 学习不同的embedding模型
   - 理解向量化的原理和优化
   - 掌握多模态向量化

2. **检索增强生成(RAG)**
   - 深入理解RAG架构
   - 学习检索策略优化
   - 掌握生成质量评估

#### 工程实践方向
1. **云原生架构**
   - 学习Kubernetes部署
   - 掌握微服务架构
   - 理解DevOps实践

2. **大数据处理**
   - 学习流式数据处理
   - 掌握批量数据导入
   - 理解数据管道设计

#### 业务应用方向
1. **行业解决方案**
   - 电商推荐系统
   - 金融风控应用
   - 医疗影像检索

2. **产品化思维**
   - 用户体验设计
   - 性能指标定义
   - 商业价值评估

---

## 附录

### A. 常见问题解答

#### Q1: Zilliz Cloud 与本地 Milvus 如何选择？
**A**: 
- **选择 Zilliz Cloud**: 快速上线、团队规模小、需要高可用、成本敏感
- **选择本地 Milvus**: 数据敏感、有专业运维团队、需要深度定制

#### Q2: 如何优化 Zilliz Cloud 的成本？
**A**:
- 启用自动扩缩容
- 合理设置数据保留策略
- 选择合适的索引类型
- 监控和优化查询模式

#### Q3: 如何保证数据安全？
**A**:
- 使用 API Token 认证
- 配置网络访问控制
- 启用数据加密
- 定期备份数据

### B. 性能调优检查清单

#### 索引优化
- [ ] 根据数据规模选择合适的索引类型
- [ ] 优化索引参数配置
- [ ] 定期重建索引

#### 查询优化
- [ ] 使用批量查询减少网络开销
- [ ] 优化搜索参数
- [ ] 实现查询结果缓存

#### 集群配置
- [ ] 配置自动扩缩容
- [ ] 选择合适的CU规格
- [ ] 启用多区域部署

### C. 监控指标参考

#### 性能指标
- 查询延迟 (P95, P99)
- 查询吞吐量 (QPS)
- 索引构建时间
- 内存使用率

#### 业务指标
- 数据增长率
- 用户活跃度
- 搜索成功率
- 系统可用性

#### 成本指标
- 每月总成本
- 单次查询成本
- 存储成本占比
- 计算成本占比

---

*本文档提供了 Zilliz Cloud 的全面学习指南，从基础概念到企业级应用，帮助你掌握云端向量数据库的核心技能。建议结合实际项目进行练习，逐步提升技术水平。*

### 1. 连接方式

#### 基础连接
```python
from pymilvus import connections, MilvusClient

class ZillizConnection:
    """Zilliz Cloud 连接管理"""
    
    def __init__(self, uri, token):
        self.uri = uri
        self.token = token
        self.client = None
    
    def connect_with_pymilvus(self):
        """使用 PyMilvus 连接"""
        try:
            connections.connect(
                alias="zilliz",
                uri=self.uri,
                token=self.token,
                secure=True
            )
            print("✅ PyMilvus 连接成功")
            return True
        except Exception as e:
            print(f"❌ PyMilvus 连接失败: {e}")
            return False
    
    def connect_with_client(self):
        """使用 MilvusClient 连接"""
        try:
            self.client = MilvusClient(
                uri=self.uri,
                token=self.token
            )
            # 测试连接
            collections = self.client.list_collections()
            print(f"✅ MilvusClient 连接成功，发现 {len(collections)} 个集合")
            return True
        except Exception as e:
            print(f"❌ MilvusClient 连接失败: {e}")
            return False
    
    def test_connection(self):
        """测试连接状态"""
        if self.client:
            try:
                # 执行简单查询测试连接
                collections = self.client.list_collections()
                return True
            except:
                return False
        return False

# 使用示例
uri = "https://your-cluster.zillizcloud.com:19530"
token = "your-api-token"

conn = ZillizConnection(uri, token)
if conn.connect_with_client():
    print("连接测试通过")
```

### 2. 认证与安全

#### API Token 管理
```python
import os
import json
from datetime import datetime, timedelta

class TokenManager:
    """API Token 管理器"""
    
    def __init__(self, token_file="zilliz_tokens.json"):
        self.token_file = token_file
        self.tokens = self.load_tokens()
    
    def load_tokens(self):
        """加载已保存的 tokens"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_tokens(self):
        """保存 tokens"""
        try:
            with open(self.token_file, 'w') as f:
                json.dump(self.tokens, f, indent=2)
        except Exception as e:
            print(f"保存 tokens 失败: {e}")
    
    def add_token(self, name, token, description=""):
        """添加新 token"""
        self.tokens[name] = {
            "token": token,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "last_used": None
        }
        self.save_tokens()
        print(f"Token '{name}' 已添加")
    
    def get_token(self, name):
        """获取 token"""
        if name in self.tokens:
            # 更新最后使用时间
            self.tokens[name]["last_used"] = datetime.now().isoformat()
            self.save_tokens()
            return self.tokens[name]["token"]
        return None
    
    def list_tokens(self):
        """列出所有 tokens"""
        print("已保存的 API Tokens:")
        for name, info in self.tokens.items():
            print(f"  {name}: {info['description']}")
            print(f"    创建时间: {info['created_at']}")
            print(f"    最后使用: {info.get('last_used', '未使用')}")

# 使用示例
# token_manager = TokenManager()
# token_manager.add_token("production", "your-prod-token", "生产环境")
# token_manager.add_token("development", "your-dev-token", "开发环境")
# prod_token = token_manager.get_token("production")
```

#### 连接池管理
```python
import threading
from queue import Queue
from contextlib import contextmanager

class ZillizConnectionPool:
    """Zilliz Cloud 连接池"""
    
    def __init__(self, uri, token, pool_size=5):
        self.uri = uri
        self.token = token
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化连接池"""
        for i in range(self.pool_size):
            try:
                client = MilvusClient(uri=self.uri, token=self.token)
                self.pool.put(client)
            except Exception as e:
                print(f"创建连接 {i} 失败: {e}")
    
    @contextmanager
    def get_connection(self):
        """获取连接（上下文管理器）"""
        client = None
        try:
            client = self.pool.get(timeout=30)
            yield client
        except Exception as e:
            print(f"获取连接失败: {e}")
            raise
        finally:
            if client:
                self.pool.put(client)
    
    def execute_with_retry(self, func, *args, **kwargs):
        """带重试的执行"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.get_connection() as client:
                    return func(client, *args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"执行失败，重试 {attempt + 1}/{max_retries}: {e}")

# 使用示例
# pool = ZillizConnectionPool(uri, token, pool_size=3)
# 
# def search_vectors(client, collection_name, vectors):
#     return client.search(collection_name, vectors, limit=10)
# 
# results = pool.execute_with_retry(search_vectors, "my_collection", [[0.1, 0.2, 0.3]])
```

---

## 云端特有功能

### 1. 自动扩缩容

#### 配置自动扩缩容
```python
def configure_auto_scaling(cluster_id, config, api_key):
    """配置自动扩缩容"""
    url = f"https://controller.api.zillizcloud.com/v1/clusters/{cluster_id}/autoscaling"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "enabled": True,
        "minCU": config["min_cu"],
        "maxCU": config["max_cu"],
        "targetCPUUtilization": config["target_cpu"],
        "scaleUpCooldown": config["scale_up_cooldown"],
        "scaleDownCooldown": config["scale_down_cooldown"]
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("自动扩缩容配置成功")
        return True
    else:
        print(f"配置失败: {response.text}")
        return False

# 配置示例
auto_scaling_config = {
    "min_cu": 1,
    "max_cu": 8,
    "target_cpu": 70,  # 目标 CPU 使用率 70%
    "scale_up_cooldown": 300,  # 扩容冷却时间 5 分钟
    "scale_down_cooldown": 600  # 缩容冷却时间 10 分钟
}

# configure_auto_scaling("your-cluster-id", auto_scaling_config, "your-api-key")
```

### 2. 数据备份与恢复

#### 自动备份配置
```python
class ZillizBackupManager:
    """Zilliz Cloud 备份管理"""
    
    def __init__(self, cluster_id, api_key):
        self.cluster_id = cluster_id
        self.api_key = api_key
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def configure_backup(self, backup_config):
        """配置自动备份"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/backup"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "enabled": backup_config["enabled"],
            "schedule": backup_config["schedule"],  # cron 表达式
            "retention": backup_config["retention_days"],
            "collections": backup_config.get("collections", [])  # 空列表表示所有集合
        }
        
        response = requests.put(url, headers=headers, json=payload)
        return response.status_code == 200
    
    def create_manual_backup(self, backup_name, collections=None):
        """创建手动备份"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/backups"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "name": backup_name,
            "collections": collections or []
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            backup_info = response.json()
            print(f"备份创建成功: {backup_info['backupId']}")
            return backup_info
        else:
            print(f"备份创建失败: {response.text}")
            return None
    
    def list_backups(self):
        """列出所有备份"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/backups"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()["backups"]
        return []
    
    def restore_backup(self, backup_id, target_cluster_id=None):
        """恢复备份"""
        url = f"{self.base_url}/backups/{backup_id}/restore"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "targetClusterId": target_cluster_id or self.cluster_id
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            restore_info = response.json()
            print(f"恢复任务已启动: {restore_info['restoreId']}")
            return restore_info
        else:
            print(f"恢复失败: {response.text}")
            return None

# 使用示例
# backup_manager = ZillizBackupManager("your-cluster-id", "your-api-key")
# 
# # 配置每日自动备份
# backup_config = {
#     "enabled": True,
#     "schedule": "0 2 * * *",  # 每天凌晨 2 点
#     "retention_days": 30,
#     "collections": []  # 备份所有集合
# }
# backup_manager.configure_backup(backup_config)
# 
# # 创建手动备份
# backup_manager.create_manual_backup("manual_backup_20241201")
```

### 3. 多区域部署

#### 跨区域复制
```python
class MultiRegionManager:
    """多区域管理器"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def create_replica(self, source_cluster_id, target_region):
        """创建跨区域副本"""
        url = f"{self.base_url}/clusters/{source_cluster_id}/replicas"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "targetRegion": target_region,
            "replicaType": "read_only"  # 只读副本
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            replica_info = response.json()
            print(f"副本创建成功: {replica_info['replicaId']}")
            return replica_info
        else:
            print(f"副本创建失败: {response.text}")
            return None
    
    def setup_global_load_balancer(self, clusters):
        """设置全局负载均衡"""
        # 这是一个概念性示例，实际实现可能因具体需求而异
        class GlobalLoadBalancer:
            def __init__(self, clusters):
                self.clusters = clusters
                self.current_index = 0
            
            def get_connection(self, region_preference=None):
                """根据区域偏好获取连接"""
                if region_preference:
                    # 优先选择指定区域的集群
                    for cluster in self.clusters:
                        if cluster["region"] == region_preference:
                            return cluster["uri"], cluster["token"]
                
                # 轮询选择
                cluster = self.clusters[self.current_index]
                self.current_index = (self.current_index + 1) % len(self.clusters)
                return cluster["uri"], cluster["token"]
        
        return GlobalLoadBalancer(clusters)

# 使用示例
# multi_region = MultiRegionManager("your-api-key")
# 
# # 创建美西到欧洲的副本
# replica = multi_region.create_replica("us-west-cluster-id", "eu-west-1")
# 
# # 设置全局负载均衡
# clusters = [
#     {"region": "us-west-2", "uri": "https://us-cluster.zillizcloud.com:19530", "token": "us-token"},
#     {"region": "eu-west-1", "uri": "https://eu-cluster.zillizcloud.com:19530", "token": "eu-token"}
# ]
# lb = multi_region.setup_global_load_balancer(clusters)
# uri, token = lb.get_connection("us-west-2")
```

---

## 性能优化与监控

### 1. 性能监控

#### 实时性能监控
```python
import time
import psutil
from datetime import datetime
import matplotlib.pyplot as plt

class ZillizPerformanceMonitor:
    """Zilliz Cloud 性能监控器"""
    
    def __init__(self, client):
        self.client = client
        self.metrics_history = []
    
    def collect_metrics(self, collection_name):
        """收集性能指标"""
        try:
            start_time = time.time()
            
            # 执行测试查询
            test_vector = [[0.1] * 128]  # 假设是 128 维向量
            results = self.client.search(
                collection_name=collection_name,
                data=test_vector,
                limit=10
            )
            
            query_time = time.time() - start_time
            
            # 获取集合统计信息
            stats = self.client.get_collection_stats(collection_name)
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "query_latency": query_time * 1000,  # 毫秒
                "row_count": stats["row_count"],
                "memory_usage": psutil.virtual_memory().percent,
                "cpu_usage": psutil.cpu_percent()
            }
            
            self.metrics_history.append(metrics)
            return metrics
            
        except Exception as e:
            print(f"收集指标失败: {e}")
            return None
    
    def monitor_continuous(self, collection_name, interval=60, duration=3600):
        """连续监控"""
        print(f"开始监控集合 '{collection_name}'，间隔 {interval} 秒")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            metrics = self.collect_metrics(collection_name)
            if metrics:
                print(f"[{metrics['timestamp']}] "
                      f"查询延迟: {metrics['query_latency']:.2f}ms, "
                      f"数据量: {metrics['row_count']}, "
                      f"内存: {metrics['memory_usage']:.1f}%, "
                      f"CPU: {metrics['cpu_usage']:.1f}%")
            
            time.sleep(interval)
    
    def generate_report(self):
        """生成性能报告"""
        if not self.metrics_history:
            print("没有可用的监控数据")
            return
        
        # 计算统计信息
        latencies = [m["query_latency"] for m in self.metrics_history]
        
        report = {
            "监控时间段": f"{self.metrics_history[0]['timestamp']} 到 {self.metrics_history[-1]['timestamp']}",
            "总查询次数": len(latencies),
            "平均延迟": f"{sum(latencies) / len(latencies):.2f}ms",
            "最小延迟": f"{min(latencies):.2f}ms",
            "最大延迟": f"{max(latencies):.2f}ms",
            "P95延迟": f"{sorted(latencies)[int(len(latencies) * 0.95)]:.2f}ms",
            "P99延迟": f"{sorted(latencies)[int(len(latencies) * 0.99)]:.2f}ms"
        }
        
        print("=== 性能监控报告 ===")
        for key, value in report.items():
            print(f"{key}: {value}")
        
        return report

# 使用示例
# monitor = ZillizPerformanceMonitor(client)
# monitor.monitor_continuous("my_collection", interval=30, duration=1800)  # 监控 30 分钟
# report = monitor.generate_report()
```

### 2. 查询优化

#### 智能查询优化器
```python
class QueryOptimizer:
    """查询优化器"""
    
    def __init__(self, client):
        self.client = client
        self.query_cache = {}
    
    def optimize_search_params(self, collection_name, sample_vectors, target_latency=100):
        """优化搜索参数"""
        print(f"为集合 '{collection_name}' 优化搜索参数，目标延迟: {target_latency}ms")
        
        # 测试不同的搜索参数组合
        param_combinations = [
            {"metric_type": "L2", "params": {"nprobe": 10}},
            {"metric_type": "L2", "params": {"nprobe": 20}},
            {"metric_type": "L2", "params": {"nprobe": 50}},
            {"metric_type": "IP", "params": {"nprobe": 10}},
            {"metric_type": "IP", "params": {"nprobe": 20}},
        ]
        
        best_params = None
        best_score = float('inf')
        
        for params in param_combinations:
            try:
                # 测试查询性能
                start_time = time.time()
                results = self.client.search(
                    collection_name=collection_name,
                    data=sample_vectors,
                    limit=10,
                    search_params=params
                )
                latency = (time.time() - start_time) * 1000
                
                # 计算得分（延迟越低越好）
                score = latency
                if latency <= target_latency:
                    score = latency * 0.5  # 满足目标延迟的参数给予奖励
                
                print(f"参数 {params}: 延迟 {latency:.2f}ms, 得分 {score:.2f}")
                
                if score < best_score:
                    best_score = score
                    best_params = params
                    
            except Exception as e:
                print(f"测试参数 {params} 失败: {e}")
        
        print(f"最优参数: {best_params}")
        return best_params
    
    def batch_search_optimizer(self, collection_name, vectors, batch_size=None):
        """批量搜索优化"""
        if batch_size is None:
            # 自动确定最优批量大小
            batch_size = self._find_optimal_batch_size(collection_name, vectors)
        
        results = []
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            batch_results = self.client.search(
                collection_name=collection_name,
                data=batch,
                limit=10
            )
            results.extend(batch_results)
        
        return results
    
    def _find_optimal_batch_size(self, collection_name, vectors):
        """找到最优批量大小"""
        test_vectors = vectors[:100]  # 使用前100个向量测试
        batch_sizes = [1, 5, 10, 20, 50]
        
        best_batch_size = 1
        best_throughput = 0
        
        for batch_size in batch_sizes:
            try:
                start_time = time.time()
                for i in range(0, len(test_vectors), batch_size):
                    batch = test_vectors[i:i + batch_size]
                    self.client.search(
                        collection_name=collection_name,
                        data=batch,
                        limit=10
                    )
                
                total_time = time.time() - start_time
                throughput = len(test_vectors) / total_time
                
                print(f"批量大小 {batch_size}: 吞吐量 {throughput:.2f} queries/sec")
                
                if throughput > best_throughput:
                    best_throughput = throughput
                    best_batch_size = batch_size
                    
            except Exception as e:
                print(f"测试批量大小 {batch_size} 失败: {e}")
        
        print(f"最优批量大小: {best_batch_size}")
        return best_batch_size

# 使用示例
# optimizer = QueryOptimizer(client)
# sample_vectors = [[random.random() for _ in range(128)] for _ in range(10)]
# best_params = optimizer.optimize_search_params("my_collection", sample_vectors)
```

### 3. 索引优化

#### 索引策略选择
```python
class IndexOptimizer:
    """索引优化器"""
    
    def __init__(self, client):
        self.client = client
    
    def recommend_index_type(self, collection_name, vector_dim, data_size):
        """推荐索引类型"""
        recommendations = []
        
        # 基于数据规模推荐
        if data_size < 100000:
            recommendations.append({
                "index_type": "FLAT",
                "reason": "数据量较小，FLAT索引提供精确搜索",
                "params": {},
                "pros": ["100%召回率", "简单易用"],
                "cons": ["查询速度较慢"]
            })
        
        if data_size >= 100000:
            recommendations.append({
                "index_type": "IVF_FLAT",
                "reason": "中等数据量，IVF_FLAT平衡性能和精度",
                "params": {"nlist": min(4096, int(data_size ** 0.5))},
                "pros": ["较好的查询性能", "可调节精度"],
                "cons": ["需要训练时间"]
            })
        
        if data_size >= 1000000:
            recommendations.append({
                "index_type": "IVF_PQ",
                "reason": "大数据量，IVF_PQ节省内存",
                "params": {
                    "nlist": min(4096, int(data_size ** 0.5)),
                    "m": vector_dim // 8  # PQ分段数
                },
                "pros": ["内存效率高", "适合大规模数据"],
                "cons": ["精度略有损失"]
            })
        
        if vector_dim <= 512:
            recommendations.append({
                "index_type": "HNSW",
                "reason": "中低维度向量，HNSW提供优秀性能",
                "params": {"M": 16, "efConstruction": 200},
                "pros": ["查询速度快", "内存友好"],
                "cons": ["构建时间较长"]
            })
        
        return recommendations
    
    def benchmark_index_types(self, collection_name, test_vectors):
        """基准测试不同索引类型"""
        index_types = [
            {"type": "IVF_FLAT", "params": {"nlist": 128}},
            {"type": "IVF_PQ", "params": {"nlist": 128, "m": 8}},
            {"type": "HNSW", "params": {"M": 16, "efConstruction": 200}}
        ]
        
        results = []
        
        for index_config in index_types:
            try:
                print(f"测试索引类型: {index_config['type']}")
                
                # 创建索引
                start_time = time.time()
                self.client.create_index(
                    collection_name=collection_name,
                    field_name="vector",
                    index_params={
                        "index_type": index_config["type"],
                        "metric_type": "L2",
                        "params": index_config["params"]
                    }
                )
                build_time = time.time() - start_time
                
                # 加载集合
                self.client.load_collection(collection_name)
                
                # 测试查询性能
                start_time = time.time()
                search_results = self.client.search(
                    collection_name=collection_name,
                    data=test_vectors,
                    limit=10
                )
                query_time = time.time() - start_time
                
                results.append({
                    "index_type": index_config["type"],
                    "build_time": build_time,
                    "query_time": query_time,
                    "avg_query_latency": query_time / len(test_vectors) * 1000
                })
                
                print(f"  构建时间: {build_time:.2f}s")
                print(f"  查询时间: {query_time:.2f}s")
                print(f"  平均延迟: {query_time / len(test_vectors) * 1000:.2f}ms")
                
            except Exception as e:
                print(f"测试 {index_config['type']} 失败: {e}")
        
        return results

# 使用示例
# index_optimizer = IndexOptimizer(client)
# recommendations = index_optimizer.recommend_index_type("my_collection", 128, 500000)
# for rec in recommendations:
#     print(f"推荐: {rec['index_type']} - {rec['reason']}")
```

---

## 成本管理与计费

### 1. 成本监控

#### 成本分析器
```python
class CostAnalyzer:
    """成本分析器"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def get_billing_info(self, cluster_id, start_date, end_date):
        """获取计费信息"""
        url = f"{self.base_url}/clusters/{cluster_id}/billing"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取计费信息失败: {response.text}")
            return None
    
    def analyze_cost_trends(self, billing_data):
        """分析成本趋势"""
        if not billing_data:
            return None
        
        daily_costs = billing_data.get("dailyCosts", [])
        
        analysis = {
            "总成本": sum(day["cost"] for day in daily_costs),
            "平均日成本": sum(day["cost"] for day in daily_costs) / len(daily_costs),
            "最高日成本": max(day["cost"] for day in daily_costs),
            "最低日成本": min(day["cost"] for day in daily_costs),
            "成本构成": self._analyze_cost_breakdown(billing_data)
        }
        
        return analysis
    
    def _analyze_cost_breakdown(self, billing_data):
        """分析成本构成"""
        breakdown = {}
        
        for item in billing_data.get("costBreakdown", []):
            service = item["service"]
            cost = item["cost"]
            breakdown[service] = cost
        
        return breakdown
    
    def generate_cost_report(self, cluster_id, month):
        """生成月度成本报告"""
        start_date = f"{month}-01"
        end_date = f"{month}-31"
        
        billing_data = self.get_billing_info(cluster_id, start_date, end_date)
        if not billing_data:
            return None
        
        analysis = self.analyze_cost_trends(billing_data)
        
        print(f"=== {month} 月度成本报告 ===")
        print(f"总成本: ${analysis['总成本']:.2f}")
        print(f"平均日成本: ${analysis['平均日成本']:.2f}")
        print(f"最高日成本: ${analysis['最高日成本']:.2f}")
        print(f"最低日成本: ${analysis['最低日成本']:.2f}")
        
        print("\n成本构成:")
        for service, cost in analysis["成本构成"].items():
            percentage = (cost / analysis["总成本"]) * 100
            print(f"  {service}: ${cost:.2f} ({percentage:.1f}%)")
        
        return analysis

# 使用示例
# cost_analyzer = CostAnalyzer("your-api-key")
# report = cost_analyzer.generate_cost_report("your-cluster-id", "2024-12")
```

### 2. 成本优化建议

#### 自动成本优化器
```python
class CostOptimizer:
    """成本优化器"""
    
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key
    
    def analyze_usage_patterns(self, cluster_id, days=30):
        """分析使用模式"""
        # 获取历史使用数据
        usage_data = self._get_usage_data(cluster_id, days)
        
        patterns = {
            "peak_hours": self._find_peak_hours(usage_data),
            "low_usage_periods": self._find_low_usage_periods(usage_data),
            "average_cpu_usage": self._calculate_average_cpu(usage_data),
            "storage_growth": self._calculate_storage_growth(usage_data)
        }
        
        return patterns
    
    def generate_optimization_recommendations(self, cluster_id):
        """生成优化建议"""
        patterns = self.analyze_usage_patterns(cluster_id)
        recommendations = []
        
        # CPU 使用率优化
        if patterns["average_cpu_usage"] < 30:
            recommendations.append({
                "type": "downsize",
                "description": "CPU使用率较低，建议降低集群规格",
                "potential_savings": "30-50%",
                "action": "将CU数量减少50%"
            })
        
        # 存储优化
        if patterns["storage_growth"] < 5:  # 每月增长小于5%
            recommendations.append({
                "type": "storage_optimization",
                "description": "存储增长缓慢，可以优化存储配置",
                "potential_savings": "10-20%",
                "action": "启用数据压缩和清理策略"
            })
        
        # 自动扩缩容
        if len(patterns["low_usage_periods"]) > 8:  # 一天中有8小时以上低使用率
            recommendations.append({
                "type": "auto_scaling",
                "description": "存在明显的使用高峰和低谷，建议启用自动扩缩容",
                "potential_savings": "20-40%",
                "action": "配置自动扩缩容策略"
            })
        
        return recommendations
    
    def implement_optimization(self, cluster_id, optimization_type):
        """实施优化建议"""
        if optimization_type == "auto_scaling":
            # 配置自动扩缩容
            config = {
                "min_cu": 1,
                "max_cu": 4,
                "target_cpu": 70,
                "scale_up_cooldown": 300,
                "scale_down_cooldown": 600
            }
            return self._configure_auto_scaling(cluster_id, config)
        
        elif optimization_type == "downsize":
            # 降低集群规格
            return self._scale_cluster(cluster_id, new_cu_size=2)
        
        elif optimization_type == "storage_optimization":
            # 存储优化
            return self._optimize_storage(cluster_id)
    
    def _get_usage_data(self, cluster_id, days):
        """获取使用数据（模拟）"""
        # 实际实现中，这里会调用 Zilliz Cloud API 获取真实数据
        import random
        
        usage_data = []
        for day in range(days):
            for hour in range(24):
                usage_data.append({
                    "timestamp": f"2024-12-{day+1:02d} {hour:02d}:00:00",
                    "cpu_usage": random.uniform(20, 80),
                    "memory_usage": random.uniform(30, 70),
                    "storage_usage": 1000 + day * 10  # 模拟存储增长
                })
        
        return usage_data
    
    def _find_peak_hours(self, usage_data):
        """找到使用高峰时段"""
        hourly_avg = {}
        for data in usage_data:
            hour = int(data["timestamp"].split()[1].split(":")[0])
            if hour not in hourly_avg:
                hourly_avg[hour] = []
            hourly_avg[hour].append(data["cpu_usage"])
        
        # 计算每小时平均使用率
        for hour in hourly_avg:
            hourly_avg[hour] = sum(hourly_avg[hour]) / len(hourly_avg[hour])
        
        # 找到使用率最高的时段
        peak_hours = sorted(hourly_avg.items(), key=lambda x: x[1], reverse=True)[:6]
        return [hour for hour, usage in peak_hours]
    
    def _find_low_usage_periods(self, usage_data):
        """找到低使用率时段"""
        hourly_avg = {}
        for data in usage_data:
            hour = int(data["timestamp"].split()[1].split(":")[0])
            if hour not in hourly_avg:
                hourly_avg[hour] = []
            hourly_avg[hour].append(data["cpu_usage"])
        
        for hour in hourly_avg:
            hourly_avg[hour] = sum(hourly_avg[hour]) / len(hourly_avg[hour])
        
        # 找到使用率低于30%的时段
        low_usage_hours = [hour for hour, usage in hourly_avg.items() if usage < 30]
        return low_usage_hours

# 使用示例
# optimizer = CostOptimizer(client, "your-api-key")
# recommendations = optimizer.generate_optimization_recommendations("your-cluster-id")
# for rec in recommendations:
#     print(f"优化建议: {rec['description']}")
#     print(f"潜在节省: {rec['potential_savings']}")
#     print(f"建议行动: {rec['action']}")
```

## 连接配置与认证

### 1. 连接方式

#### 基础连接
```python
from pymilvus import connections, MilvusClient

# 方式1: 使用 connections (推荐用于复杂应用)
def connect_with_connections():
    """使用 connections 连接"""
    connections.connect(
        alias="zilliz_cloud",
        uri="https://your-cluster.zillizcloud.com:19530",
        token="your-api-token",
        secure=True
    )
    print("连接成功 (connections)")

# 方式2: 使用 MilvusClient (推荐用于简单应用)
def connect_with_client():
    """使用 MilvusClient 连接"""
    client = MilvusClient(
        uri="https://your-cluster.zillizcloud.com:19530",
        token="your-api-token"
    )
    print("连接成功 (MilvusClient)")
    return client

# 方式3: 使用环境变量
import os

def connect_with_env():
    """使用环境变量连接"""
    uri = os.getenv('ZILLIZ_URI')
    token = os.getenv('ZILLIZ_TOKEN')
    
    if not uri or not token:
        raise ValueError("请设置 ZILLIZ_URI 和 ZILLIZ_TOKEN 环境变量")
    
    client = MilvusClient(uri=uri, token=token)
    return client
```

#### 高级连接配置
```python
from pymilvus import connections
import ssl

def advanced_connection():
    """高级连接配置"""
    
    # SSL 配置
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # 连接池配置
    connections.connect(
        alias="zilliz_advanced",
        uri="https://your-cluster.zillizcloud.com:19530",
        token="your-api-token",
        secure=True,
        # 连接池设置
        pool_size=10,
        # 超时设置
        timeout=30,
        # 重试设置
        retry_on_rpc_failure=True,
        retry_on_rate_limit=True,
        # SSL 设置
        ssl_context=ssl_context
    )
```

### 2. 认证管理

#### API Token 管理
```python
import requests
import json
from datetime import datetime, timedelta

class ZillizAuthManager:
    """Zilliz Cloud 认证管理器"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def create_api_token(self, token_name, expires_in_days=30):
        """创建 API Token"""
        url = f"{self.base_url}/apiKeys"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        expires_at = datetime.now() + timedelta(days=expires_in_days)
        
        payload = {
            "name": token_name,
            "description": f"API Token created at {datetime.now()}",
            "expiresAt": expires_at.isoformat()
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            token_info = response.json()
            print(f"✅ API Token 创建成功")
            print(f"Token ID: {token_info['id']}")
            print(f"Token: {token_info['token']}")
            return token_info
        else:
            print(f"❌ API Token 创建失败: {response.text}")
            return None
    
    def list_api_tokens(self):
        """列出所有 API Token"""
        url = f"{self.base_url}/apiKeys"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            tokens = response.json()
            print("📋 API Tokens 列表:")
            for token in tokens.get('data', []):
                print(f"  - {token['name']} (ID: {token['id']})")
                print(f"    状态: {token['status']}")
                print(f"    过期时间: {token.get('expiresAt', 'Never')}")
            return tokens
        else:
            print(f"❌ 获取 Token 列表失败: {response.text}")
            return None
    
    def revoke_api_token(self, token_id):
        """撤销 API Token"""
        url = f"{self.base_url}/apiKeys/{token_id}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ API Token {token_id} 已撤销")
            return True
        else:
            print(f"❌ 撤销 Token 失败: {response.text}")
            return False

# 使用示例
# auth_manager = ZillizAuthManager("your-master-api-key")
# token_info = auth_manager.create_api_token("demo-token", 30)
# auth_manager.list_api_tokens()
```

#### 连接测试工具
```python
from pymilvus import MilvusClient, connections
import time

def test_connection(uri, token, test_name="连接测试"):
    """测试连接性能和稳定性"""
    print(f"🔍 开始 {test_name}...")
    
    try:
        # 测试连接时间
        start_time = time.time()
        client = MilvusClient(uri=uri, token=token)
        connect_time = time.time() - start_time
        
        # 测试基本操作
        start_time = time.time()
        collections = client.list_collections()
        list_time = time.time() - start_time
        
        print(f"✅ {test_name} 成功")
        print(f"  连接时间: {connect_time:.2f}s")
        print(f"  列表操作时间: {list_time:.2f}s")
        print(f"  集合数量: {len(collections)}")
        
        return True
        
    except Exception as e:
        print(f"❌ {test_name} 失败: {e}")
        return False

def connection_benchmark(uri, token, iterations=5):
    """连接性能基准测试"""
    print(f"🚀 开始连接性能基准测试 ({iterations} 次)...")
    
    connect_times = []
    success_count = 0
    
    for i in range(iterations):
        try:
            start_time = time.time()
            client = MilvusClient(uri=uri, token=token)
            client.list_collections()
            connect_time = time.time() - start_time
            
            connect_times.append(connect_time)
            success_count += 1
            print(f"  第 {i+1} 次: {connect_time:.2f}s")
            
        except Exception as e:
            print(f"  第 {i+1} 次: 失败 - {e}")
    
    if connect_times:
        avg_time = sum(connect_times) / len(connect_times)
        min_time = min(connect_times)
        max_time = max(connect_times)
        
        print(f"\n📊 基准测试结果:")
        print(f"  成功率: {success_count}/{iterations} ({success_count/iterations*100:.1f}%)")
        print(f"  平均连接时间: {avg_time:.2f}s")
        print(f"  最快连接时间: {min_time:.2f}s")
        print(f"  最慢连接时间: {max_time:.2f}s")

# 使用示例
# test_connection("your-uri", "your-token")
# connection_benchmark("your-uri", "your-token", 5)
```

---

## 云端特有功能

### 1. 自动扩缩容

#### 配置自动扩缩容
```python
import requests

class ZillizAutoScaling:
    """Zilliz Cloud 自动扩缩容管理"""
    
    def __init__(self, api_key, cluster_id):
        self.api_key = api_key
        self.cluster_id = cluster_id
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def configure_auto_scaling(self, config):
        """配置自动扩缩容"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/scaling"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "enabled": config.get("enabled", True),
            "minCU": config.get("min_cu", 1),
            "maxCU": config.get("max_cu", 8),
            "targetCPUUtilization": config.get("cpu_threshold", 70),
            "targetMemoryUtilization": config.get("memory_threshold", 80),
            "scaleUpCooldown": config.get("scale_up_cooldown", 300),
            "scaleDownCooldown": config.get("scale_down_cooldown", 600)
        }
        
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ 自动扩缩容配置成功")
            return response.json()
        else:
            print(f"❌ 配置失败: {response.text}")
            return None
    
    def get_scaling_status(self):
        """获取扩缩容状态"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/scaling/status"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            status = response.json()
            print("📊 扩缩容状态:")
            print(f"  当前 CU: {status.get('currentCU')}")
            print(f"  目标 CU: {status.get('targetCU')}")
            print(f"  状态: {status.get('status')}")
            print(f"  CPU 使用率: {status.get('cpuUtilization')}%")
            print(f"  内存使用率: {status.get('memoryUtilization')}%")
            return status
        else:
            print(f"❌ 获取状态失败: {response.text}")
            return None

# 使用示例
scaling_config = {
    "enabled": True,
    "min_cu": 1,
    "max_cu": 8,
    "cpu_threshold": 70,
    "memory_threshold": 80,
    "scale_up_cooldown": 300,
    "scale_down_cooldown": 600
}

# auto_scaling = ZillizAutoScaling("your-api-key", "your-cluster-id")
# auto_scaling.configure_auto_scaling(scaling_config)
# auto_scaling.get_scaling_status()
```

### 2. 多区域部署

#### 区域选择和配置
```python
class ZillizRegionManager:
    """Zilliz Cloud 区域管理"""
    
    AVAILABLE_REGIONS = {
        "aws-us-east-1": {
            "name": "美国东部 (弗吉尼亚)",
            "provider": "AWS",
            "latency_zones": ["北美", "南美"]
        },
        "aws-us-west-2": {
            "name": "美国西部 (俄勒冈)",
            "provider": "AWS", 
            "latency_zones": ["北美", "亚太"]
        },
        "aws-eu-west-1": {
            "name": "欧洲 (爱尔兰)",
            "provider": "AWS",
            "latency_zones": ["欧洲", "中东", "非洲"]
        },
        "aws-ap-southeast-1": {
            "name": "亚太 (新加坡)",
            "provider": "AWS",
            "latency_zones": ["亚太", "澳洲"]
        },
        "gcp-us-central1": {
            "name": "美国中部 (爱荷华)",
            "provider": "GCP",
            "latency_zones": ["北美"]
        }
    }
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def list_available_regions(self):
        """列出可用区域"""
        print("🌍 可用区域列表:")
        for region_id, info in self.AVAILABLE_REGIONS.items():
            print(f"  {region_id}:")
            print(f"    名称: {info['name']}")
            print(f"    提供商: {info['provider']}")
            print(f"    低延迟区域: {', '.join(info['latency_zones'])}")
            print()
    
    def recommend_region(self, user_location):
        """推荐最佳区域"""
        recommendations = {
            "中国": "aws-ap-southeast-1",
            "日本": "aws-ap-southeast-1", 
            "韩国": "aws-ap-southeast-1",
            "美国": "aws-us-west-2",
            "加拿大": "aws-us-east-1",
            "英国": "aws-eu-west-1",
            "德国": "aws-eu-west-1",
            "法国": "aws-eu-west-1"
        }
        
        recommended = recommendations.get(user_location, "aws-us-west-2")
        region_info = self.AVAILABLE_REGIONS[recommended]
        
        print(f"💡 为 {user_location} 推荐区域:")
        print(f"  区域: {recommended}")
        print(f"  名称: {region_info['name']}")
        print(f"  提供商: {region_info['provider']}")
        
        return recommended
    
    def test_region_latency(self, regions=None):
        """测试区域延迟"""
        import time
        import requests
        
        if regions is None:
            regions = list(self.AVAILABLE_REGIONS.keys())
        
        print("🔍 测试区域延迟...")
        latency_results = {}
        
        for region in regions:
            try:
                # 模拟延迟测试 (实际应用中需要真实的端点)
                test_url = f"https://{region}.zillizcloud.com/health"
                
                start_time = time.time()
                # response = requests.get(test_url, timeout=5)
                # 模拟延迟
                time.sleep(0.1)  # 模拟网络延迟
                latency = (time.time() - start_time) * 1000
                
                latency_results[region] = latency
                print(f"  {region}: {latency:.0f}ms")
                
            except Exception as e:
                print(f"  {region}: 测试失败 - {e}")
                latency_results[region] = float('inf')
        
        # 推荐最低延迟的区域
        best_region = min(latency_results, key=latency_results.get)
        print(f"\n🏆 推荐区域: {best_region} ({latency_results[best_region]:.0f}ms)")
        
        return latency_results

# 使用示例
# region_manager = ZillizRegionManager("your-api-key")
# region_manager.list_available_regions()
# region_manager.recommend_region("中国")
# region_manager.test_region_latency()
```

### 3. 数据备份与恢复

#### 自动备份配置
```python
class ZillizBackupManager:
    """Zilliz Cloud 备份管理"""
    
    def __init__(self, api_key, cluster_id):
        self.api_key = api_key
        self.cluster_id = cluster_id
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def configure_backup(self, backup_config):
        """配置自动备份"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/backup/config"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "enabled": backup_config.get("enabled", True),
            "schedule": backup_config.get("schedule", "0 2 * * *"),  # 每天凌晨2点
            "retention": backup_config.get("retention_days", 7),
            "compression": backup_config.get("compression", True),
            "encryption": backup_config.get("encryption", True)
        }
        
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ 备份配置成功")
            return response.json()
        else:
            print(f"❌ 备份配置失败: {response.text}")
            return None
    
    def create_manual_backup(self, backup_name):
        """创建手动备份"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/backup"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "name": backup_name,
            "description": f"Manual backup created at {datetime.now()}",
            "type": "manual"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            backup_info = response.json()
            print(f"✅ 手动备份创建成功: {backup_info['backupId']}")
            return backup_info
        else:
            print(f"❌ 手动备份创建失败: {response.text}")
            return None
    
    def list_backups(self):
        """列出所有备份"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/backup"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            backups = response.json()
            print("📋 备份列表:")
            for backup in backups.get('data', []):
                print(f"  - {backup['name']} (ID: {backup['id']})")
                print(f"    类型: {backup['type']}")
                print(f"    状态: {backup['status']}")
                print(f"    创建时间: {backup['createdAt']}")
                print(f"    大小: {backup.get('size', 'Unknown')}")
                print()
            return backups
        else:
            print(f"❌ 获取备份列表失败: {response.text}")
            return None
    
    def restore_from_backup(self, backup_id, restore_config):
        """从备份恢复"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/restore"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "backupId": backup_id,
            "targetCluster": restore_config.get("target_cluster", self.cluster_id),
            "collections": restore_config.get("collections", []),  # 空列表表示恢复所有
            "overwrite": restore_config.get("overwrite", False)
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            restore_info = response.json()
            print(f"✅ 恢复任务创建成功: {restore_info['restoreId']}")
            return restore_info
        else:
            print(f"❌ 恢复任务创建失败: {response.text}")
            return None

# 使用示例
backup_config = {
    "enabled": True,
    "schedule": "0 2 * * *",  # 每天凌晨2点
    "retention_days": 7,
    "compression": True,
    "encryption": True
}

# backup_manager = ZillizBackupManager("your-api-key", "your-cluster-id")
# backup_manager.configure_backup(backup_config)
# backup_manager.create_manual_backup("demo-backup-20241201")
# backup_manager.list_backups()
```

---

## 性能优化与监控

### 1. 性能监控

#### 实时性能监控
```python
import time
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class ZillizPerformanceMonitor:
    """Zilliz Cloud 性能监控"""
    
    def __init__(self, api_key, cluster_id):
        self.api_key = api_key
        self.cluster_id = cluster_id
        self.base_url = "https://controller.api.zillizcloud.com/v1"
        self.metrics_history = []
    
    def get_cluster_metrics(self):
        """获取集群性能指标"""
        url = f"{self.base_url}/clusters/{self.cluster_id}/metrics"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 获取最近1小时的指标
        params = {
            "start": (datetime.now() - timedelta(hours=1)).isoformat(),
            "end": datetime.now().isoformat(),
            "step": "1m"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            metrics = response.json()
            return self._process_metrics(metrics)
        else:
            print(f"❌ 获取指标失败: {response.text}")
            return None
    
    def _process_metrics(self, raw_metrics):
        """处理原始指标数据"""
        processed = {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": raw_metrics.get("cpu", {}).get("current", 0),
            "memory_usage": raw_metrics.get("memory", {}).get("current", 0),
            "disk_usage": raw_metrics.get("disk", {}).get("current", 0),
            "qps": raw_metrics.get("qps", {}).get("current", 0),
            "latency_p99": raw_metrics.get("latency", {}).get("p99", 0),
            "latency_avg": raw_metrics.get("latency", {}).get("avg", 0),
            "active_connections": raw_metrics.get("connections", {}).get("active", 0),
            "index_size": raw_metrics.get("storage", {}).get("index_size", 0),
            "data_size": raw_metrics.get("storage", {}).get("data_size", 0)
        }
        
        return processed
    
    def monitor_performance(self, duration_minutes=60, interval_seconds=60):
        """持续监控性能"""
        print(f"🔍 开始性能监控 (持续 {duration_minutes} 分钟)...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            try:
                metrics = self.get_cluster_metrics()
                if metrics:
                    self.metrics_history.append(metrics)
                    self._print_current_metrics(metrics)
                    
                    # 检查性能告警
                    self._check_performance_alerts(metrics)
                
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                print("监控已停止")
                break
            except Exception as e:
                print(f"监控异常: {e}")
                time.sleep(interval_seconds)
        
        # 生成监控报告
        self._generate_performance_report()
    
    def _print_current_metrics(self, metrics):
        """打印当前指标"""
        print(f"\n📊 [{metrics['timestamp']}] 性能指标:")
        print(f"  CPU 使用率: {metrics['cpu_usage']:.1f}%")
        print(f"  内存使用率: {metrics['memory_usage']:.1f}%")
        print(f"  磁盘使用率: {metrics['disk_usage']:.1f}%")
        print(f"  QPS: {metrics['qps']:.0f}")
        print(f"  平均延迟: {metrics['latency_avg']:.2f}ms")
        print(f"  P99 延迟: {metrics['latency_p99']:.2f}ms")
        print(f"  活跃连接: {metrics['active_connections']}")
    
    def _check_performance_alerts(self, metrics):
        """检查性能告警"""
        alerts = []
        
        if metrics['cpu_usage'] > 80:
            alerts.append(f"⚠️  CPU 使用率过高: {metrics['cpu_usage']:.1f}%")
        
        if metrics['memory_usage'] > 85:
            alerts.append(f"⚠️  内存使用率过高: {metrics['memory_usage']:.1f}%")
        
        if metrics['latency_p99'] > 1000:
            alerts.append(f"⚠️  P99 延迟过高: {metrics['latency_p99']:.2f}ms")
        
        if metrics['qps'] < 10:
            alerts.append(f"⚠️  QPS 过低: {metrics['qps']:.0f}")
        
        for alert in alerts:
            print(alert)
    
    def _generate_performance_report(self):
        """生成性能报告"""
        if not self.metrics_history:
            print("❌ 没有性能数据")
            return
        
        print("\n📈 性能监控报告:")
        
        # 计算统计信息
        cpu_values = [m['cpu_usage'] for m in self.metrics_history]
        memory_values = [m['memory_usage'] for m in self.metrics_history]
        latency_values = [m['latency_avg'] for m in self.metrics_history]
        qps_values = [m['qps'] for m in self.metrics_history]
        
        print(f"  监控时长: {len(self.metrics_history)} 个数据点")
        print(f"  CPU 使用率: 平均 {sum(cpu_values)/len(cpu_values):.1f}%, 最高 {max(cpu_values):.1f}%")
        print(f"  内存使用率: 平均 {sum(memory_values)/len(memory_values):.1f}%, 最高 {max(memory_values):.1f}%")
        print(f"  平均延迟: 平均 {sum(latency_values)/len(latency_values):.2f}ms, 最高 {max(latency_values):.2f}ms")
        print(f"  QPS: 平均 {sum(qps_values)/len(qps_values):.0f}, 最高 {max(qps_values):.0f}")
        
        # 保存详细数据
        report_file = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.metrics_history, f, indent=2, ensure_ascii=False)
        print(f"  详细报告已保存: {report_file}")

# 使用示例
# monitor = ZillizPerformanceMonitor("your-api-key", "your-cluster-id")
# monitor.monitor_performance(duration_minutes=30, interval_seconds=60)
```

### 2. 查询优化

#### 查询性能分析
```python
from pymilvus import MilvusClient
import time
import numpy as np

class ZillizQueryOptimizer:
    """Zilliz Cloud 查询优化器"""
    
    def __init__(self, client):
        self.client = client
        self.query_stats = []
    
    def analyze_query_performance(self, collection_name, query_vectors, top_k=10, iterations=5):
        """分析查询性能"""
        print(f"🔍 分析查询性能 (集合: {collection_name})...")
        
        results = {
            "collection": collection_name,
            "query_count": len(query_vectors),
            "top_k": top_k,
            "iterations": iterations,
            "latencies": [],
            "throughput": [],
            "accuracy": []
        }
        
        for i in range(iterations):
            print(f"  第 {i+1} 轮测试...")
            
            # 测试延迟
            latencies = []
            start_time = time.time()
            
            for vector in query_vectors:
                query_start = time.time()
                
                search_results = self.client.search(
                    collection_name=collection_name,
                    data=[vector],
                    limit=top_k,
                    output_fields=["id"]
                )
                
                query_latency = (time.time() - query_start) * 1000
                latencies.append(query_latency)
            
            total_time = time.time() - start_time
            
            # 计算指标
            avg_latency = sum(latencies) / len(latencies)
            throughput = len(query_vectors) / total_time
            
            results["latencies"].append(avg_latency)
            results["throughput"].append(throughput)
            
            print(f"    平均延迟: {avg_latency:.2f}ms")
            print(f"    吞吐量: {throughput:.2f} QPS")
        
        # 计算最终统计
        self._print_performance_summary(results)
        return results
    
    def _print_performance_summary(self, results):
        """打印性能摘要"""
        latencies = results["latencies"]
        throughputs = results["throughput"]
        
        print(f"\n📊 性能分析结果:")
        print(f"  集合: {results['collection']}")
        print(f"  查询数量: {results['query_count']}")
        print(f"  Top-K: {results['top_k']}")
        print(f"  测试轮数: {results['iterations']}")
        print(f"  平均延迟: {sum(latencies)/len(latencies):.2f}ms (±{np.std(latencies):.2f})")
        print(f"  平均吞吐量: {sum(throughputs)/len(throughputs):.2f} QPS (±{np.std(throughputs):.2f})")
        print(f"  最佳延迟: {min(latencies):.2f}ms")
        print(f"  最高吞吐量: {max(throughputs):.2f} QPS")
    
    def optimize_search_params(self, collection_name, query_vector, test_params):
        """优化搜索参数"""
        print(f"🔧 优化搜索参数...")
        
        best_params = None
        best_score = 0
        results = []
        
        for params in test_params:
            print(f"  测试参数: {params}")
            
            try:
                # 测试性能
                start_time = time.time()
                
                search_results = self.client.search(
                    collection_name=collection_name,
                    data=[query_vector],
                    limit=params.get("limit", 10),
                    search_params=params.get("search_params", {}),
                    output_fields=["id"]
                )
                
                latency = (time.time() - start_time) * 1000
                
                # 计算得分 (延迟越低得分越高)
                score = 1000 / latency if latency > 0 else 0
                
                result = {
                    "params": params,
                    "latency": latency,
                    "score": score,
                    "result_count": len(search_results[0])
                }
                
                results.append(result)
                
                print(f"    延迟: {latency:.2f}ms, 得分: {score:.2f}")
                
                if score > best_score:
                    best_score = score
                    best_params = params
                    
            except Exception as e:
                print(f"    参数测试失败: {e}")
        
        print(f"\n🏆 最优参数:")
        print(f"  参数: {best_params}")
        print(f"  延迟: {min(r['latency'] for r in results if r['params'] == best_params):.2f}ms")
        
        return best_params, results
    
    def benchmark_different_strategies(self, collection_name, query_vectors):
        """基准测试不同策略"""
        strategies = [
            {
                "name": "默认搜索",
                "params": {}
            },
            {
                "name": "高精度搜索",
                "params": {
                    "search_params": {"nprobe": 128}
                }
            },
            {
                "name": "高速搜索", 
                "params": {
                    "search_params": {"nprobe": 16}
                }
            },
            {
                "name": "批量搜索",
                "params": {
                    "batch_size": 10
                }
            }
        ]
        
        print(f"🚀 基准测试不同搜索策略...")
        
        for strategy in strategies:
            print(f"\n测试策略: {strategy['name']}")
            
            start_time = time.time()
            total_queries = 0
            
            try:
                if strategy["params"].get("batch_size"):
                    # 批量搜索
                    batch_size = strategy["params"]["batch_size"]
                    for i in range(0, len(query_vectors), batch_size):
                        batch = query_vectors[i:i+batch_size]
                        self.client.search(
                            collection_name=collection_name,
                            data=batch,
                            limit=10
                        )
                        total_queries += len(batch)
                else:
                    # 单个搜索
                    for vector in query_vectors:
                        self.client.search(
                            collection_name=collection_name,
                            data=[vector],
                            limit=10,
                            search_params=strategy["params"].get("search_params", {})
                        )
                        total_queries += 1
                
                total_time = time.time() - start_time
                throughput = total_queries / total_time
                avg_latency = (total_time / total_queries) * 1000
                
                print(f"  总查询数: {total_queries}")
                print(f"  总时间: {total_time:.2f}s")
                print(f"  平均延迟: {avg_latency:.2f}ms")
                print(f"  吞吐量: {throughput:.2f} QPS")
                
            except Exception as e:
                print(f"  策略测试失败: {e}")

# 使用示例
# client = MilvusClient(uri="your-uri", token="your-token")
# optimizer = ZillizQueryOptimizer(client)

# # 生成测试向量
# test_vectors = np.random.random((10, 768)).tolist()

# # 分析查询性能
# optimizer.analyze_query_performance("your_collection", test_vectors)

# # 优化搜索参数
# test_params = [
#     {"limit": 10, "search_params": {"nprobe": 16}},
#     {"limit": 10, "search_params": {"nprobe": 32}},
#     {"limit": 10, "search_params": {"nprobe": 64}},
#     {"limit": 10, "search_params": {"nprobe": 128}}
# ]
# optimizer.optimize_search_params("your_collection", test_vectors[0], test_params)

# # 基准测试
# optimizer.benchmark_different_strategies("your_collection", test_vectors)
```

---

## 成本管理与计费

### 1. 成本监控

#### 成本分析工具
```python
import requests
from datetime import datetime, timedelta
import json

class ZillizCostManager:
    """Zilliz Cloud 成本管理"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://controller.api.zillizcloud.com/v1"
    
    def get_billing_info(self, start_date=None, end_date=None):
        """获取计费信息"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        url = f"{self.base_url}/billing"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        params = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat()
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            billing_data = response.json()
            self._print_billing_summary(billing_data)
            return billing_data
        else:
            print(f"❌ 获取计费信息失败: {response.text}")
            return None
    
    def _print_billing_summary(self, billing_data):
        """打印计费摘要"""
        print("💰 计费信息摘要:")
        
        total_cost = billing_data.get("totalCost", 0)
        currency = billing_data.get("currency", "USD")
        
        print(f"  总费用: {total_cost:.2f} {currency}")
        print(f"  计费周期: {billing_data.get('startDate')} - {billing_data.get('endDate')}")
        
        # 按服务分类的费用
        services = billing_data.get("services", [])
        if services:
            print("  服务费用明细:")
            for service in services:
                print(f"    {service['name']}: {service['cost']:.2f} {currency}")
        
        # 按集群分类的费用
        clusters = billing_data.get("clusters", [])
        if clusters:
            print("  集群费用明细:")
            for cluster in clusters:
                print(f"    {cluster['name']}: {cluster['cost']:.2f} {currency}")
                print(f"      计算单元小时: {cluster.get('cuHours', 0):.1f}")
                print(f"      存储 GB·小时: {cluster.get('storageGBHours', 0):.1f}")
    
    def get_cost_breakdown(self, cluster_id):
        """获取集群成本分解"""
        url = f"{self.base_url}/clusters/{cluster_id}/billing"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            cost_data = response.json()
            self._print_cost_breakdown(cost_data)
            return cost_data
        else:
            print(f"❌ 获取成本分解失败: {response.text}")
            return None
    
    def _print_cost_breakdown(self, cost_data):
        """打印成本分解"""
        print("📊 成本分解:")
        
        # 计算成本
        compute_cost = cost_data.get("computeCost", 0)
        storage_cost = cost_data.get("storageCost", 0)
        network_cost = cost_data.get("networkCost", 0)
        total_cost = compute_cost + storage_cost + network_cost
        
        print(f"  计算成本: ${compute_cost:.2f} ({compute_cost/total_cost*100:.1f}%)")
        print(f"  存储成本: ${storage_cost:.2f} ({storage_cost/total_cost*100:.1f}%)")
        print(f"  网络成本: ${network_cost:.2f} ({network_cost/total_cost*100:.1f}%)")
        print(f"  总成本: ${total_cost:.2f}")
        
        # 使用量详情
        usage = cost_data.get("usage", {})
        print("  使用量详情:")
        print(f"    计算单元小时: {usage.get('cuHours', 0):.1f}")
        print(f"    存储 GB·小时: {usage.get('storageGBHours', 0):.1f}")
        print(f"    网络传输 GB: {usage.get('networkGB', 0):.1f}")
    
    def set_cost_alerts(self, alert_config):
        """设置成本告警"""
        url = f"{self.base_url}/billing/alerts"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "enabled": alert_config.get("enabled", True),
            "thresholds": [
                {
                    "type": "monthly",
                    "amount": alert_config.get("monthly_limit", 100),
                    "currency": "USD"
                },
                {
                    "type": "daily",
                    "amount": alert_config.get("daily_limit", 10),
                    "currency": "USD"
                }
            ],
            "notifications": {
                "email": alert_config.get("email", []),
                "webhook": alert_config.get("webhook", "")
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("✅ 成本告警设置成功")
            return response.json()
        else:
            print(f"❌ 成本告警设置失败: {response.text}")
            return None
    
    def estimate_monthly_cost(self, cluster_config):
        """估算月度成本"""
        # 成本计算公式 (示例价格)
        PRICING = {
            "compute_per_cu_hour": 0.50,  # 每 CU 每小时
            "storage_per_gb_hour": 0.001,  # 每 GB 每小时
            "network_per_gb": 0.10  # 每 GB 网络传输
        }
        
        cu_size = cluster_config.get("cu_size", 1)
        storage_gb = cluster_config.get("storage_gb", 100)
        network_gb_per_month = cluster_config.get("network_gb_per_month", 10)
        
        # 假设 24/7 运行
        hours_per_month = 24 * 30
        
        compute_cost = cu_size * PRICING["compute_per_cu_hour"] * hours_per_month
        storage_cost = storage_gb * PRICING["storage_per_gb_hour"] * hours_per_month
        network_cost = network_gb_per_month * PRICING["network_per_gb"]
        
        total_cost = compute_cost + storage_cost + network_cost
        
        print("💡 月度成本估算:")
        print(f"  集群配置:")
        print(f"    计算单元: {cu_size} CU")
        print(f"    存储容量: {storage_gb} GB")
        print(f"    月度网络传输: {network_gb_per_month} GB")
        print(f"  成本分解:")
        print(f"    计算成本: ${compute_cost:.2f}")
        print(f"    存储成本: ${storage_cost:.2f}")
        print(f"    网络成本: ${network_cost:.2f}")
        print(f"  预估月度总成本: ${total_cost:.2f}")
        
        return {
            "compute_cost": compute_cost,
            "storage_cost": storage_cost,
            "network_cost": network_cost,
            "total_cost": total_cost
        }

# 使用示例
# cost_manager = ZillizCostManager("your-api-key")

# # 获取计费信息
# billing_info = cost_manager.get_billing_info()

# # 获取集群成本分解
# cost_breakdown = cost_manager.get_cost_breakdown("your-cluster-id")

# # 设置成本告警
# alert_config = {
#     "enabled": True,
#     "monthly_limit": 100,
#     "daily_limit": 10,
#     "email": ["admin@example.com"]
# }
# cost_manager.set_cost_alerts(alert_config)

# # 估算成本
# cluster_config = {
#     "cu_size": 2,
#     "storage_gb": 500,
#     "network_gb_per_month": 50
# }
# cost_manager.estimate_monthly_cost(cluster_config)
```

### 2. 成本优化建议

#### 自动化成本优化
```python
class ZillizCostOptimizer:
    """Zilliz Cloud 成本优化器"""
    
    def __init__(self, cost_manager, cluster_manager):
        self.cost_manager = cost_manager
        self.cluster_manager = cluster_manager
    
    def analyze_cost_efficiency(self, cluster_id):
        """分析成本效率"""
        print("📈 分析成本效率...")
        
        # 获取成本数据
        cost_data = self.cost_manager.get_cost_breakdown(cluster_id)
        if not cost_data:
            return None
        
        # 获取性能数据
        cluster_info = self.cluster_manager.get_cluster_info()
        if not cluster_info:
            return None
        
        # 计算效率指标
        total_cost = cost_data.get("computeCost", 0) + cost_data.get("storageCost", 0)
        usage = cost_data.get("usage", {})
        cu_hours = usage.get("cuHours", 1)
        
        # 成本效率分析
        cost_per_cu_hour = total_cost / cu_hours if cu_hours > 0 else 0
        
        efficiency_report = {
            "cluster_id": cluster_id,
            "total_cost": total_cost,
            "cu_hours": cu_hours,
            "cost_per_cu_hour": cost_per_cu_hour,
            "recommendations": []
        }
        
        # 生成优化建议
        recommendations = self._generate_recommendations(cost_data, cluster_info)
        efficiency_report["recommendations"] = recommendations
        
        self._print_efficiency_report(efficiency_report)
        return efficiency_report
    
    def _generate_recommendations(self, cost_data, cluster_info):
        """生成优化建议"""
        recommendations = []
        
        usage = cost_data.get("usage", {})
        cu_hours = usage.get("cuHours", 0)
        storage_gb_hours = usage.get("storageGBHours", 0)
        
        # 计算利用率
        total_hours = 24 * 30  # 假设30天
        cu_utilization = cu_hours / total_hours if total_hours > 0 else 0
        
        # 低利用率建议
        if cu_utilization