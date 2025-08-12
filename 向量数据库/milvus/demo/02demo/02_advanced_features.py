#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Milvus Lite 高级功能示例
演示批量操作、数据管理、性能优化等高级功能
"""

import random
import time
import json
from typing import List, Dict, Any

try:
    from pymilvus import MilvusClient
except ImportError:
    print("请先安装 pymilvus: pip install -U pymilvus")
    exit(1)

class MilvusAdvancedDemo:
    def __init__(self, db_path: str = "./milvus_advanced_demo.db"):
        """初始化 Milvus 客户端"""
        self.client = MilvusClient(db_path)
        self.collection_name = "advanced_demo_collection"
        self.dimension = 256
        
    def setup_collection(self):
        """设置集合"""
        print("=== 设置集合 ===")
        
        # 删除已存在的集合
        if self.client.has_collection(self.collection_name):
            print(f"删除已存在的集合: {self.collection_name}")
            self.client.drop_collection(self.collection_name)
        
        # 创建新集合
        print(f"创建集合: {self.collection_name}")
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=self.dimension,
            metric_type="COSINE",  # 使用余弦相似度
            consistency_level="Strong"
        )
        
        # 创建索引
        print("创建向量索引...")
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 256}
        }
        
        self.client.create_index(
            collection_name=self.collection_name,
            field_name="vector",
            index_params=index_params
        )
        print("✓ 集合设置完成\n")
    
    def generate_sample_data(self, count: int) -> List[Dict[str, Any]]:
        """生成示例数据"""
        print(f"生成 {count} 条示例数据...")
        
        categories = ["人工智能", "机器学习", "深度学习", "自然语言处理", "计算机视觉"]
        sources = ["论文", "博客", "新闻", "教程", "文档"]
        
        data = []
        for i in range(count):
            # 生成归一化向量（用于余弦相似度）
            vector = [random.gauss(0, 1) for _ in range(self.dimension)]
            norm = sum(x*x for x in vector) ** 0.5
            vector = [x/norm for x in vector]
            
            category = categories[i % len(categories)]
            source = sources[i % len(sources)]
            
            data.append({
                "id": i,
                "vector": vector,
                "title": f"{category}相关{source}标题_{i}",
                "content": f"这是一篇关于{category}的{source}，内容编号为{i}",
                "category": category,
                "source": source,
                "publish_year": 2020 + (i % 4),
                "view_count": random.randint(100, 10000),
                "rating": round(random.uniform(3.0, 5.0), 1)
            })
        
        print(f"✓ 数据生成完成")
        return data
    
    def batch_insert_demo(self):
        """批量插入演示"""
        print("=== 批量插入演示 ===")
        
        total_count = 5000
        batch_size = 1000
        
        print(f"准备插入 {total_count} 条数据，批次大小: {batch_size}")
        
        start_time = time.time()
        
        for i in range(0, total_count, batch_size):
            batch_data = self.generate_sample_data(batch_size)
            
            # 更新 ID 以避免重复
            for j, item in enumerate(batch_data):
                item["id"] = i + j
            
            print(f"插入批次 {i//batch_size + 1}/{(total_count-1)//batch_size + 1}...")
            self.client.insert(
                collection_name=self.collection_name,
                data=batch_data
            )
        
        total_time = time.time() - start_time
        print(f"✓ 批量插入完成，总耗时: {total_time:.2f} 秒")
        print(f"  平均插入速度: {total_count/total_time:.0f} 条/秒\n")
    
    def complex_search_demo(self):
        """复杂搜索演示"""
        print("=== 复杂搜索演示 ===")
        
        # 生成查询向量
        query_vector = [random.gauss(0, 1) for _ in range(self.dimension)]
        norm = sum(x*x for x in query_vector) ** 0.5
        query_vector = [x/norm for x in query_vector]
        
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 20}
        }
        
        # 1. 基础搜索
        print("1. 基础向量搜索...")
        start_time = time.time()
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=5,
            search_params=search_params,
            output_fields=["title", "category", "rating"]
        )
        search_time = time.time() - start_time
        
        print(f"   搜索耗时: {search_time:.4f} 秒")
        for i, result in enumerate(results[0]):
            print(f"   {i+1}. 相似度: {1-result['distance']:.4f}, 标题: {result['entity']['title']}")
        print()
        
        # 2. 带类别过滤的搜索
        print("2. 带类别过滤的搜索（只搜索人工智能类别）...")
        filtered_results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=3,
            search_params=search_params,
            filter="category == '人工智能'",
            output_fields=["title", "category", "source"]
        )
        
        for i, result in enumerate(filtered_results[0]):
            print(f"   {i+1}. 相似度: {1-result['distance']:.4f}")
            print(f"      标题: {result['entity']['title']}")
            print(f"      来源: {result['entity']['source']}")
        print()
        
        # 3. 复合条件搜索
        print("3. 复合条件搜索（评分>4.0且发布年份>=2022）...")
        complex_results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=3,
            search_params=search_params,
            filter="rating > 4.0 and publish_year >= 2022",
            output_fields=["title", "rating", "publish_year"]
        )
        
        for i, result in enumerate(complex_results[0]):
            print(f"   {i+1}. 相似度: {1-result['distance']:.4f}")
            print(f"      标题: {result['entity']['title']}")
            print(f"      评分: {result['entity']['rating']}, 年份: {result['entity']['publish_year']}")
        print()
    
    def data_management_demo(self):
        """数据管理演示"""
        print("=== 数据管理演示 ===")
        
        # 1. 查询统计信息
        print("1. 集合统计信息...")
        stats = self.client.get_collection_stats(self.collection_name)
        print(f"   总实体数量: {stats['row_count']}")
        print()
        
        # 2. 按条件查询
        print("2. 查询高评分内容（评分>=4.5）...")
        high_rating_results = self.client.query(
            collection_name=self.collection_name,
            filter="rating >= 4.5",
            output_fields=["title", "rating", "view_count"],
            limit=5
        )
        
        for result in high_rating_results:
            print(f"   ID: {result['id']}, 评分: {result['rating']}")
            print(f"   标题: {result['title']}")
            print(f"   浏览量: {result['view_count']}")
            print()
        
        # 3. 按类别统计
        print("3. 按类别查询数量...")
        categories = ["人工智能", "机器学习", "深度学习", "自然语言处理", "计算机视觉"]
        
        for category in categories:
            count_results = self.client.query(
                collection_name=self.collection_name,
                filter=f"category == '{category}'",
                output_fields=["id"],
                limit=16384  # 设置足够大的限制来获取所有结果
            )
            print(f"   {category}: {len(count_results)} 条")
        print()
        
        # 4. 删除低评分数据
        print("4. 删除低评分数据（评分<3.5）...")
        delete_filter = "rating < 3.5"
        
        # 先查询要删除的数据数量
        to_delete = self.client.query(
            collection_name=self.collection_name,
            filter=delete_filter,
            output_fields=["id"],
            limit=16384
        )
        
        print(f"   找到 {len(to_delete)} 条低评分数据")
        
        if len(to_delete) > 0:
            self.client.delete(
                collection_name=self.collection_name,
                filter=delete_filter
            )
            print(f"   ✓ 已删除 {len(to_delete)} 条低评分数据")
            
            # 检查删除后的统计信息
            new_stats = self.client.get_collection_stats(self.collection_name)
            print(f"   删除后实体数量: {new_stats['row_count']}")
        print()
    
    def performance_analysis(self):
        """性能分析"""
        print("=== 性能分析 ===")
        
        # 生成多个查询向量
        query_vectors = []
        for _ in range(10):
            vector = [random.gauss(0, 1) for _ in range(self.dimension)]
            norm = sum(x*x for x in vector) ** 0.5
            query_vectors.append([x/norm for x in vector])
        
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 20}
        }
        
        # 单次搜索性能测试
        print("1. 单次搜索性能测试...")
        times = []
        for i in range(10):
            start_time = time.time()
            self.client.search(
                collection_name=self.collection_name,
                data=[query_vectors[i]],
                limit=10,
                search_params=search_params,
                output_fields=["title"]
            )
            times.append(time.time() - start_time)
        
        avg_time = sum(times) / len(times)
        print(f"   平均搜索时间: {avg_time:.4f} 秒")
        print(f"   最快搜索时间: {min(times):.4f} 秒")
        print(f"   最慢搜索时间: {max(times):.4f} 秒")
        print()
        
        # 批量搜索性能测试
        print("2. 批量搜索性能测试...")
        start_time = time.time()
        batch_results = self.client.search(
            collection_name=self.collection_name,
            data=query_vectors,
            limit=10,
            search_params=search_params,
            output_fields=["title"]
        )
        batch_time = time.time() - start_time
        
        print(f"   批量搜索时间（10个查询）: {batch_time:.4f} 秒")
        print(f"   平均每个查询时间: {batch_time/10:.4f} 秒")
        print(f"   批量 vs 单次性能提升: {avg_time*10/batch_time:.2f}x")
        print()
    
    def export_sample_data(self, filename: str = "sample_results.json"):
        """导出示例数据"""
        print(f"=== 导出示例数据到 {filename} ===")
        
        # 查询一些示例数据
        sample_data = self.client.query(
            collection_name=self.collection_name,
            filter="rating >= 4.0",
            output_fields=["title", "content", "category", "rating", "publish_year"],
            limit=20
        )
        
        # 保存到 JSON 文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已导出 {len(sample_data)} 条数据到 {filename}")
        print()
    
    def cleanup(self):
        """清理资源"""
        print("=== 清理资源 ===")
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
            print(f"✓ 已删除集合: {self.collection_name}")

def main():
    print("=== Milvus Lite 高级功能演示 ===\n")
    
    demo = MilvusAdvancedDemo()
    
    try:
        # 1. 设置集合
        demo.setup_collection()
        
        # 2. 批量插入演示
        demo.batch_insert_demo()
        
        # 3. 复杂搜索演示
        demo.complex_search_demo()
        
        # 4. 数据管理演示
        demo.data_management_demo()
        
        # 5. 性能分析
        demo.performance_analysis()
        
        # 6. 导出示例数据
        demo.export_sample_data()
        
        print("=== 高级功能演示完成 ===")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
    
    finally:
        # 清理资源（可选）
        # demo.cleanup()
        pass

if __name__ == "__main__":
    main()