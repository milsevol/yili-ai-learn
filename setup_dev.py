#!/usr/bin/env python3
"""
开发环境快速设置脚本

这个脚本帮助快速设置项目的开发环境，包括：
- 检查Python版本
- 安装依赖包
- 设置pre-commit hooks
- 运行基础测试
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(cmd, description="", check=True):
    """运行命令并处理错误"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {e}")
        if e.stderr:
            print(f"错误详情: {e.stderr}")
        return False


def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("需要Python 3.8或更高版本")
        return False


def check_system_info():
    """检查系统信息"""
    print("💻 系统信息:")
    print(f"   操作系统: {platform.system()} {platform.release()}")
    print(f"   架构: {platform.machine()}")
    print(f"   Python路径: {sys.executable}")


def install_dependencies():
    """安装项目依赖"""
    print("📦 安装项目依赖...")
    
    # 升级pip
    if not run_command("python -m pip install --upgrade pip", "升级pip"):
        return False
    
    # 安装基础依赖
    if not run_command("pip install -r requirements.txt", "安装基础依赖"):
        return False
    
    # 安装开发依赖
    if not run_command("pip install -e .[dev]", "安装开发依赖"):
        print("⚠️  开发依赖安装失败，尝试手动安装...")
        dev_packages = [
            "pytest>=6.0",
            "pytest-cov>=2.0", 
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
            "isort>=5.10.0",
            "pre-commit>=2.20.0"
        ]
        for package in dev_packages:
            run_command(f"pip install {package}", f"安装 {package}", check=False)
    
    return True


def setup_pre_commit():
    """设置pre-commit hooks"""
    print("🔧 设置pre-commit hooks...")
    
    if not run_command("pre-commit install", "安装pre-commit hooks"):
        print("⚠️  pre-commit安装失败，跳过...")
        return False
    
    return True


def run_basic_tests():
    """运行基础测试"""
    print("🧪 运行基础测试...")
    
    # 检查代码格式
    print("检查代码格式...")
    run_command("black --check 向量数据库/ --diff", "检查代码格式", check=False)
    
    # 运行测试
    if os.path.exists("tests"):
        run_command("pytest tests/ -v", "运行测试", check=False)
    else:
        print("⚠️  测试目录不存在，跳过测试...")
    
    return True


def create_vscode_settings():
    """创建VSCode设置"""
    print("⚙️  创建VSCode设置...")
    
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)
    
    settings = {
        "python.defaultInterpreterPath": sys.executable,
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "python.linting.mypyEnabled": True,
        "python.formatting.provider": "black",
        "python.sortImports.args": ["--profile", "black"],
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.organizeImports": True
        },
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/.mypy_cache": True,
            "**/.pytest_cache": True,
            "**/milvus_lite.db": True
        }
    }
    
    import json
    with open(vscode_dir / "settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print("✅ VSCode设置已创建")


def main():
    """主函数"""
    print("🚀 开始设置yili-ai-learn开发环境...")
    print("=" * 50)
    
    # 检查系统信息
    check_system_info()
    print()
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    print()
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败")
        sys.exit(1)
    print()
    
    # 设置pre-commit
    setup_pre_commit()
    print()
    
    # 创建VSCode设置
    create_vscode_settings()
    print()
    
    # 运行基础测试
    run_basic_tests()
    print()
    
    print("🎉 开发环境设置完成!")
    print("\n📋 接下来你可以:")
    print("   1. 运行 'make run-milvus-demo' 来体验Milvus演示")
    print("   2. 运行 'make test' 来执行测试")
    print("   3. 运行 'make format' 来格式化代码")
    print("   4. 查看 README.md 了解更多信息")
    print("\n💡 提示: 使用 'make help' 查看所有可用命令")


if __name__ == "__main__":
    main()