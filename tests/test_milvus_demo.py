"""
Milvus 演示代码的测试
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock


class TestMilvusDemo:
    """Milvus 演示代码测试类"""

    def test_demo_files_exist(self):
        """测试演示文件是否存在"""
        demo_path = "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/milvus/demo/02demo"
        
        demo_files = [
            "01_basic_usage.py",
            "02_advanced_features.py", 
            "03_langchain_integration.py",
            "run_all_demos.py"
        ]
        
        for file_name in demo_files:
            file_path = os.path.join(demo_path, file_name)
            assert os.path.exists(file_path), f"演示文件不存在: {file_name}"

    def test_demo_files_have_main_function(self):
        """测试演示文件是否包含main函数"""
        demo_path = "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/milvus/demo/02demo"
        
        demo_files = [
            "01_basic_usage.py",
            "02_advanced_features.py",
            "03_langchain_integration.py",
            "run_all_demos.py"
        ]
        
        for file_name in demo_files:
            file_path = os.path.join(demo_path, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert 'def main(' in content, f"文件 {file_name} 缺少main函数"

    def test_demo_data_structure(self):
        """测试演示数据结构"""
        # 测试向量维度
        vector_dim = 128
        assert vector_dim > 0
        
        # 测试数据字段
        expected_fields = ["id", "vector", "text", "subject"]
        assert len(expected_fields) == 4
        assert "vector" in expected_fields

    def test_database_file_cleanup(self):
        """测试数据库文件清理功能"""
        # 创建临时数据库文件
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # 确认文件存在
        assert os.path.exists(tmp_path)
        
        # 清理文件
        os.remove(tmp_path)
        
        # 确认文件已删除
        assert not os.path.exists(tmp_path)

    def test_vector_dimension_consistency(self):
        """测试向量维度一致性"""
        # 模拟向量数据
        vector_dim = 128
        test_vector = [0.1] * vector_dim  # 简单的向量数据
        
        assert len(test_vector) == vector_dim
        assert all(isinstance(x, (int, float)) for x in test_vector)

    @pytest.mark.parametrize("collection_name", [
        "demo_collection",
        "test_collection", 
        "langchain_collection"
    ])
    def test_collection_names(self, collection_name):
        """测试集合名称有效性"""
        assert isinstance(collection_name, str)
        assert len(collection_name) > 0
        assert collection_name.replace("_", "").isalnum()


class TestProjectStructure:
    """项目结构测试类"""

    def test_project_root_files(self):
        """测试项目根目录必要文件"""
        project_root = "/Users/cuixueyong/code/github/yili-ai-learn"
        
        required_files = [
            "README.md",
            "requirements.txt",
            ".gitignore",
            "setup.py",
            "pyproject.toml"
        ]
        
        for file_name in required_files:
            file_path = os.path.join(project_root, file_name)
            assert os.path.exists(file_path), f"缺少必要文件: {file_name}"

    def test_milvus_demo_structure(self):
        """测试 Milvus 演示目录结构"""
        demo_path = "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/milvus/demo/02demo"
        
        required_files = [
            "01_basic_usage.py",
            "02_advanced_features.py",
            "03_langchain_integration.py", 
            "run_all_demos.py",
            "README.md",
            "__init__.py"
        ]
        
        for file_name in required_files:
            file_path = os.path.join(demo_path, file_name)
            assert os.path.exists(file_path), f"缺少演示文件: {file_name}"

    def test_init_files_exist(self):
        """测试__init__.py文件是否存在"""
        init_paths = [
            "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/__init__.py",
            "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/milvus/__init__.py",
            "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/milvus/demo/__init__.py",
            "/Users/cuixueyong/code/github/yili-ai-learn/向量数据库/milvus/demo/02demo/__init__.py"
        ]
        
        for init_path in init_paths:
            assert os.path.exists(init_path), f"缺少__init__.py文件: {init_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])