# Makefile for yili-ai-learn project

.PHONY: help install install-dev test lint format clean docs run-milvus-demo

# 默认目标
help:
	@echo "Available commands:"
	@echo "  install      - 安装项目依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  test         - 运行测试"
	@echo "  lint         - 运行代码检查"
	@echo "  format       - 格式化代码"
	@echo "  clean        - 清理临时文件"
	@echo "  docs         - 生成文档"
	@echo "  run-milvus-demo - 运行 Milvus 演示"

# 安装项目依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
install-dev:
	pip install -e ".[dev]"

# 运行测试
test:
	pytest tests/ -v --cov=向量数据库 --cov-report=html --cov-report=term

# 代码检查
lint:
	flake8 向量数据库/
	mypy 向量数据库/

# 格式化代码
format:
	black 向量数据库/
	isort 向量数据库/

# 清理临时文件
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -name ".coverage" -delete
	find . -name "htmlcov" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name "milvus_lite.db" -delete
	find . -name "*.db" -delete

# 生成文档
docs:
	@echo "文档生成功能待实现"

# 运行 Milvus 演示
run-milvus-demo:
	python -m 向量数据库.milvus.demo.02demo.run_all_demos

# 检查代码质量
check: lint test
	@echo "代码质量检查完成"

# 完整的开发环境设置
setup-dev: install-dev
	@echo "开发环境设置完成"

# 发布前检查
pre-commit: format lint test
	@echo "发布前检查完成"