#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Milvus Lite 与 LangChain 集成示例
演示如何在 LangChain 框架中使用 Milvus Lite 作为向量存储
"""

import os
from typing import List

# 检查必要的依赖
try:
    from langchain_milvus import Milvus
    from langchain_core.documents import Document
    from langchain_core.embeddings import Embeddings
except ImportError:
    print("请安装 LangChain Milvus 集成: pip install langchain-milvus")
    exit(1)

# 简单的嵌入模型示例（实际使用中建议使用 OpenAI 或其他专业嵌入模型）
class SimpleEmbeddings(Embeddings):
    """简单的嵌入模型示例，用于演示目的"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """嵌入文档列表"""
        import hashlib
        import random
        
        embeddings = []
        for text in texts:
            # 使用文本哈希作为随机种子，确保相同文本产生相同向量
            seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
            random.seed(seed)
            
            # 生成归一化向量
            vector = [random.gauss(0, 1) for _ in range(self.dimension)]
            norm = sum(x*x for x in vector) ** 0.5
            vector = [x/norm for x in vector]
            embeddings.append(vector)
        
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """嵌入查询文本"""
        return self.embed_documents([text])[0]

def create_sample_documents() -> List[Document]:
    """创建示例文档"""
    documents = [
        Document(
            page_content="人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
            metadata={"category": "AI", "source": "教科书", "difficulty": "初级"}
        ),
        Document(
            page_content="机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。",
            metadata={"category": "ML", "source": "论文", "difficulty": "中级"}
        ),
        Document(
            page_content="深度学习是机器学习的一个分支，使用多层神经网络来模拟人脑的工作方式。",
            metadata={"category": "DL", "source": "博客", "difficulty": "高级"}
        ),
        Document(
            page_content="自然语言处理（NLP）是人工智能的一个领域，专注于计算机与人类语言之间的交互。",
            metadata={"category": "NLP", "source": "维基百科", "difficulty": "中级"}
        ),
        Document(
            page_content="计算机视觉是人工智能的一个领域，致力于让计算机能够理解和解释视觉信息。",
            metadata={"category": "CV", "source": "教程", "difficulty": "中级"}
        ),
        Document(
            page_content="强化学习是机器学习的一种方法，通过与环境交互来学习最优行为策略。",
            metadata={"category": "RL", "source": "研究报告", "difficulty": "高级"}
        ),
        Document(
            page_content="神经网络是受生物神经系统启发的计算模型，是深度学习的基础。",
            metadata={"category": "NN", "source": "教科书", "difficulty": "中级"}
        ),
        Document(
            page_content="卷积神经网络（CNN）是一种特殊的神经网络，特别适用于图像处理任务。",
            metadata={"category": "CNN", "source": "论文", "difficulty": "高级"}
        ),
        Document(
            page_content="循环神经网络（RNN）是一种能够处理序列数据的神经网络架构。",
            metadata={"category": "RNN", "source": "博客", "difficulty": "高级"}
        ),
        Document(
            page_content="Transformer是一种基于注意力机制的神经网络架构，在自然语言处理中表现出色。",
            metadata={"category": "Transformer", "source": "论文", "difficulty": "高级"}
        )
    ]
    
    return documents

def basic_langchain_demo():
    """基础 LangChain 集成演示"""
    print("=== LangChain 基础集成演示 ===\n")
    
    # 1. 创建嵌入模型
    print("1. 创建嵌入模型...")
    embeddings = SimpleEmbeddings(dimension=384)
    print("✓ 嵌入模型创建完成\n")
    
    # 2. 创建 Milvus 向量存储
    print("2. 创建 Milvus 向量存储...")
    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": "./langchain_milvus_demo.db"},
        collection_name="langchain_collection",
        drop_old=True  # 删除已存在的集合
    )
    print("✓ 向量存储创建完成\n")
    
    # 3. 添加文档
    print("3. 添加示例文档...")
    documents = create_sample_documents()
    
    # 添加文档到向量存储
    ids = vector_store.add_documents(documents)
    print(f"✓ 已添加 {len(documents)} 个文档，ID: {ids[:3]}...\n")
    
    # 4. 相似性搜索
    print("4. 执行相似性搜索...")
    query = "什么是神经网络？"
    
    # 基础相似性搜索
    similar_docs = vector_store.similarity_search(query, k=3)
    
    print(f"查询: {query}")
    print("相似文档:")
    for i, doc in enumerate(similar_docs):
        print(f"  {i+1}. {doc.page_content}")
        print(f"     元数据: {doc.metadata}")
        print()
    
    # 5. 带分数的相似性搜索
    print("5. 带分数的相似性搜索...")
    similar_docs_with_scores = vector_store.similarity_search_with_score(query, k=3)
    
    print("相似文档（带分数）:")
    for i, (doc, score) in enumerate(similar_docs_with_scores):
        print(f"  {i+1}. 相似度分数: {score:.4f}")
        print(f"     内容: {doc.page_content}")
        print(f"     类别: {doc.metadata.get('category', 'N/A')}")
        print()
    
    return vector_store

def retriever_demo(vector_store):
    """检索器演示"""
    print("=== 检索器演示 ===\n")
    
    # 1. 创建基础检索器
    print("1. 创建基础检索器...")
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    query = "深度学习和机器学习的关系"
    docs = retriever.invoke(query)
    
    print(f"查询: {query}")
    print("检索结果:")
    for i, doc in enumerate(docs):
        print(f"  {i+1}. {doc.page_content}")
        print(f"     难度: {doc.metadata.get('difficulty', 'N/A')}")
        print()
    
    # 2. 创建 MMR 检索器（最大边际相关性）
    print("2. 创建 MMR 检索器...")
    mmr_retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 8, "lambda_mult": 0.5}
    )
    
    mmr_docs = mmr_retriever.invoke(query)
    
    print("MMR 检索结果（多样性更好）:")
    for i, doc in enumerate(mmr_docs):
        print(f"  {i+1}. {doc.page_content}")
        print(f"     类别: {doc.metadata.get('category', 'N/A')}")
        print()

def metadata_filtering_demo(vector_store):
    """元数据过滤演示"""
    print("=== 元数据过滤演示 ===\n")
    
    # 1. 按难度过滤
    print("1. 搜索高级难度的文档...")
    query = "人工智能技术"
    
    # 创建带过滤条件的检索器
    filtered_retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"difficulty": "高级"}
        }
    )
    
    filtered_docs = filtered_retriever.invoke(query)
    
    print("高级难度文档:")
    for i, doc in enumerate(filtered_docs):
        print(f"  {i+1}. {doc.page_content}")
        print(f"     难度: {doc.metadata.get('difficulty')}")
        print(f"     来源: {doc.metadata.get('source')}")
        print()
    
    # 2. 按来源过滤
    print("2. 搜索论文来源的文档...")
    paper_retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"source": "论文"}
        }
    )
    
    paper_docs = paper_retriever.invoke(query)
    
    print("论文来源文档:")
    for i, doc in enumerate(paper_docs):
        print(f"  {i+1}. {doc.page_content}")
        print(f"     类别: {doc.metadata.get('category')}")
        print()

def document_management_demo(vector_store):
    """文档管理演示"""
    print("=== 文档管理演示 ===\n")
    
    # 1. 添加新文档
    print("1. 添加新文档...")
    new_documents = [
        Document(
            page_content="生成对抗网络（GAN）是一种深度学习架构，由两个神经网络相互竞争。",
            metadata={"category": "GAN", "source": "论文", "difficulty": "高级", "year": 2023}
        ),
        Document(
            page_content="BERT是一种基于Transformer的预训练语言模型，在多项NLP任务中表现出色。",
            metadata={"category": "BERT", "source": "论文", "difficulty": "高级", "year": 2023}
        )
    ]
    
    new_ids = vector_store.add_documents(new_documents)
    print(f"✓ 已添加 {len(new_documents)} 个新文档，ID: {new_ids}\n")
    
    # 2. 搜索新添加的文档
    print("2. 搜索新添加的文档...")
    query = "生成对抗网络"
    results = vector_store.similarity_search(query, k=2)
    
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.page_content}")
        print(f"     年份: {doc.metadata.get('year', 'N/A')}")
        print()
    
    # 3. 删除文档（通过 ID）
    print("3. 删除指定文档...")
    if new_ids:
        vector_store.delete(ids=[new_ids[0]])
        print(f"✓ 已删除文档 ID: {new_ids[0]}\n")

def performance_comparison():
    """性能对比演示"""
    print("=== 性能对比演示 ===\n")
    
    import time
    
    # 创建两个不同配置的向量存储进行对比
    embeddings = SimpleEmbeddings(dimension=256)
    
    # 配置1：较小的向量维度
    print("1. 创建小维度向量存储（256维）...")
    small_store = Milvus(
        embedding_function=embeddings,
        connection_args={"uri": "./small_dim_demo.db"},
        collection_name="small_collection",
        drop_old=True
    )
    
    # 配置2：较大的向量维度
    large_embeddings = SimpleEmbeddings(dimension=768)
    print("2. 创建大维度向量存储（768维）...")
    large_store = Milvus(
        embedding_function=large_embeddings,
        connection_args={"uri": "./large_dim_demo.db"},
        collection_name="large_collection",
        drop_old=True
    )
    
    # 准备测试数据
    documents = create_sample_documents() * 10  # 扩展到100个文档
    
    # 测试插入性能
    print("3. 测试插入性能...")
    
    start_time = time.time()
    small_store.add_documents(documents)
    small_insert_time = time.time() - start_time
    
    start_time = time.time()
    large_store.add_documents(documents)
    large_insert_time = time.time() - start_time
    
    print(f"   小维度插入时间: {small_insert_time:.2f} 秒")
    print(f"   大维度插入时间: {large_insert_time:.2f} 秒")
    print()
    
    # 测试搜索性能
    print("4. 测试搜索性能...")
    query = "人工智能和机器学习"
    
    # 小维度搜索
    start_time = time.time()
    for _ in range(10):
        small_store.similarity_search(query, k=5)
    small_search_time = time.time() - start_time
    
    # 大维度搜索
    start_time = time.time()
    for _ in range(10):
        large_store.similarity_search(query, k=5)
    large_search_time = time.time() - start_time
    
    print(f"   小维度搜索时间（10次）: {small_search_time:.4f} 秒")
    print(f"   大维度搜索时间（10次）: {large_search_time:.4f} 秒")
    print(f"   平均搜索时间对比: {small_search_time/10:.4f} vs {large_search_time/10:.4f} 秒")
    print()

def main():
    print("=== Milvus Lite 与 LangChain 集成演示 ===\n")
    
    try:
        # 1. 基础集成演示
        vector_store = basic_langchain_demo()
        
        # 2. 检索器演示
        retriever_demo(vector_store)
        
        # 3. 元数据过滤演示
        metadata_filtering_demo(vector_store)
        
        # 4. 文档管理演示
        document_management_demo(vector_store)
        
        # 5. 性能对比演示
        performance_comparison()
        
        print("=== LangChain 集成演示完成 ===")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()