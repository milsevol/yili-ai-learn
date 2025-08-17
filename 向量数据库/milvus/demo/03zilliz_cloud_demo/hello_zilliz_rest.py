import configparser
import os
import requests
import json

# 读取配置文件
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_file_path)

# 获取Milvus连接信息
milvus_uri = config.get('example', 'uri')
api_key = config.get('example', 'token')

# 确保URI格式正确
if not milvus_uri.startswith("https://"):
    milvus_uri = f"https://{milvus_uri}"

# 移除URI中可能存在的端口号
if ":443" in milvus_uri:
    milvus_uri = milvus_uri.replace(":443", "")

print(f"使用URI: {milvus_uri}")
print(f"使用API Key: {api_key}")

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 尝试获取集合列表
try:
    # 构建API端点URL
    collections_url = f"{milvus_uri}/v1/vector/collections"
    print(f"请求URL: {collections_url}")
    
    # 发送GET请求
    response = requests.get(collections_url, headers=headers)
    
    # 检查响应状态
    if response.status_code == 200:
        collections = response.json()
        print(f"\n成功连接到Zilliz Cloud!")
        print(f"集合列表: {json.dumps(collections, indent=2)}")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
        
except Exception as e:
    print(f"连接错误: {e}")