#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Milvus Lite 基础使用示例
演示如何使用 Milvus Lite 进行基本的向量数据库操作
"""

import random
import time
from pymilvus import MilvusClient

def main():
    print("=== Milvus Lite 基础使用示例 ===\n")
    
    # 1. 创建客户端连接
    print("1. 创建 Milvus Lite 客户端...")
    client = MilvusClient("./milvus_basic_demo.db")
    print("✓ 客户端创建成功\n")
    
    # 2. 创建集合
    collection_name = "basic_demo_collection"
    dimension = 128
    
    print(f"2. 创建集合 '{collection_name}'...")
    
    # 检查集合是否已存在
    if client.has_collection(collection_name):
        print(f"集合 '{collection_name}' 已存在，删除后重新创建...")
        client.drop_collection(collection_name)
    
    # 创建新集合
    client.create_collection(
        collection_name=collection_name,
        dimension=dimension,
        metric_type="L2",
        consistency_level="Strong"
    )
    print(f"✓ 集合 '{collection_name}' 创建成功\n")
    
    # 3. 准备和插入数据
    print("3. 准备示例数据...")
    data = []
    categories = ["科技", "体育", "娱乐", "财经", "健康"]
    
    for i in range(1000):
        vector = [random.random() for _ in range(dimension)]
        category = categories[i % len(categories)]
        data.append({
            "id": i,
            "vector": vector,
            "text": f"这是关于{category}的第{i}条新闻内容",
            "category": category,
            "score": random.randint(1, 100)
        })
    
    print(f"✓ 准备了 {len(data)} 条数据")
    
    print("4. 插入数据到集合...")
    start_time = time.time()
    client.insert(collection_name=collection_name, data=data)
    insert_time = time.time() - start_time
    print(f"✓ 数据插入完成，耗时: {insert_time:.2f} 秒\n")
    
    # 5. 创建索引
    print("5. 创建向量索引...")
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    
    client.create_index(
        collection_name=collection_name,
        field_name="vector",
        index_params=index_params
    )
    print("✓ 索引创建成功\n")
    
    # 6. 执行向量搜索
    print("6. 执行向量搜索...")
    query_vector = [random.random() for _ in range(dimension)]
    
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }
    
    start_time = time.time()
    results = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=5,
        search_params=search_params,
        output_fields=["text", "category", "score"]
    )
    search_time = time.time() - start_time
    
    print(f"✓ 搜索完成，耗时: {search_time:.4f} 秒")
    print("搜索结果:")
    for i, result in enumerate(results[0]):
        print(f"  {i+1}. ID: {result['id']}, 距离: {result['distance']:.4f}")
        print(f"     文本: {result['entity']['text']}")
        print(f"     类别: {result['entity']['category']}, 评分: {result['entity']['score']}")
        print()
    
    # 7. 带过滤条件的搜索
    print("7. 执行带过滤条件的搜索（只搜索科技类新闻）...")
    filtered_results = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=3,
        search_params=search_params,
        filter="category == '科技'",
        output_fields=["text", "category", "score"]
    )
    
    print("过滤搜索结果:")
    for i, result in enumerate(filtered_results[0]):
        print(f"  {i+1}. ID: {result['id']}, 距离: {result['distance']:.4f}")
        print(f"     文本: {result['entity']['text']}")
        print(f"     类别: {result['entity']['category']}")
        print()
    
    # 8. 查询特定数据
    print("8. 查询特定 ID 的数据...")
    query_results = client.query(
        collection_name=collection_name,
        filter="id in [1, 10, 100]",
        output_fields=["text", "category", "score"]
    )
    
    print("查询结果:")
    for result in query_results:
        print(f"  ID: {result['id']}")
        print(f"  文本: {result['text']}")
        print(f"  类别: {result['category']}, 评分: {result['score']}")
        print()
    
    # 9. 获取集合统计信息
    print("9. 获取集合统计信息...")
    stats = client.get_collection_stats(collection_name=collection_name)
    print(f"✓ 集合中的实体数量: {stats['row_count']}")
    
    # 10. 列出所有集合
    print("\n10. 列出所有集合...")
    collections = client.list_collections()
    print(f"✓ 当前数据库中的集合: {collections}")
    
    print("\n=== 基础使用示例完成 ===")

if __name__ == "__main__":
    main()