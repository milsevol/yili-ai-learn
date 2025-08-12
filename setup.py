#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yili-ai-learn 项目安装配置
"""

from setuptools import setup, find_packages
import os

# 读取 README 文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AI 学习项目"

# 读取依赖
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 过滤注释和空行
            requirements = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
            return requirements
    return []

setup(
    name="yili-ai-learn",
    version="0.1.0",
    author="崔学勇",
    author_email="your-email@example.com",
    description="一个专注于人工智能学习的综合性项目",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/yili-ai-learn",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
        "openai": [
            "openai>=1.0.0",
        ],
        "transformers": [
            "sentence-transformers>=2.2.0",
            "transformers>=4.20.0",
            "torch>=1.12.0",
        ],
        "full": [
            "openai>=1.0.0",
            "sentence-transformers>=2.2.0",
            "transformers>=4.20.0",
            "torch>=1.12.0",
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ]
    },
    entry_points={
        "console_scripts": [
            "yili-milvus-demo=向量数据库.milvus.demo.02demo.run_all_demos:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml"],
    },
    keywords="ai, machine learning, deep learning, vector database, milvus, langchain",
    project_urls={
        "Bug Reports": "https://github.com/your-username/yili-ai-learn/issues",
        "Source": "https://github.com/your-username/yili-ai-learn",
        "Documentation": "https://github.com/your-username/yili-ai-learn/blob/main/README.md",
    },
)