#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有 Milvus Lite 演示的主脚本
提供交互式菜单，让用户选择要运行的演示
"""

import os
import sys
import subprocess
import time

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🚀 Milvus Lite 演示程序集合")
    print("=" * 60)
    print("本程序将演示 Milvus Lite 的各种功能和用法")
    print("包括基础操作、高级功能和 LangChain 集成")
    print("=" * 60)
    print()

def check_dependencies():
    """检查必要的依赖是否已安装"""
    print("🔍 检查依赖包...")
    
    required_packages = [
        ("pymilvus", "pip install -U pymilvus"),
        ("langchain_milvus", "pip install langchain-milvus"),
        ("langchain_core", "pip install langchain-core")
    ]
    
    missing_packages = []
    
    for package, install_cmd in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - 已安装")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append((package, install_cmd))
    
    if missing_packages:
        print("\n⚠️  发现缺失的依赖包:")
        for package, install_cmd in missing_packages:
            print(f"   {package}: {install_cmd}")
        
        print("\n请先安装缺失的依赖包，然后重新运行此程序。")
        print("或者运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包检查完成\n")
    return True

def run_demo(script_name, description):
    """运行指定的演示脚本"""
    print(f"\n🎯 开始运行: {description}")
    print("=" * 50)
    
    try:
        # 检查脚本文件是否存在
        if not os.path.exists(script_name):
            print(f"❌ 错误: 找不到脚本文件 {script_name}")
            return False
        
        # 运行脚本
        start_time = time.time()
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"\n✅ {description} 运行完成")
            print(f"⏱️  耗时: {duration:.2f} 秒")
            return True
        else:
            print(f"\n❌ {description} 运行失败")
            print(f"错误代码: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ 运行 {description} 时出现异常: {e}")
        return False

def show_menu():
    """显示主菜单"""
    print("\n📋 请选择要运行的演示:")
    print("1. 基础使用演示 (01_basic_usage.py)")
    print("2. 高级功能演示 (02_advanced_features.py)")
    print("3. LangChain 集成演示 (03_langchain_integration.py)")
    print("4. 运行所有演示")
    print("5. 查看演示说明")
    print("6. 清理生成的数据库文件")
    print("0. 退出程序")
    print("-" * 40)

def show_demo_info():
    """显示演示说明"""
    print("\n📖 演示说明:")
    print()
    
    demos = [
        ("基础使用演示", [
            "• 创建 Milvus Lite 客户端连接",
            "• 集合的创建、删除和管理",
            "• 数据插入和索引创建",
            "• 基础向量搜索功能",
            "• 带过滤条件的搜索",
            "• 数据查询和删除操作",
            "• 集合统计信息获取"
        ]),
        ("高级功能演示", [
            "• 批量数据插入（5000条数据）",
            "• 复杂搜索条件和过滤",
            "• 性能分析和基准测试",
            "• 数据管理和统计分析",
            "• 数据导出到JSON文件",
            "• 不同索引类型的性能对比"
        ]),
        ("LangChain 集成演示", [
            "• 与 LangChain 框架无缝集成",
            "• 文档向量化和存储",
            "• 相似性搜索和检索器",
            "• 元数据过滤和文档管理",
            "• MMR（最大边际相关性）检索",
            "• 不同向量维度的性能对比"
        ])
    ]
    
    for title, features in demos:
        print(f"🔹 {title}:")
        for feature in features:
            print(f"   {feature}")
        print()

def cleanup_databases():
    """清理生成的数据库文件"""
    print("\n🧹 清理数据库文件...")
    
    db_files = [
        "milvus_basic_demo.db",
        "milvus_advanced_demo.db", 
        "langchain_milvus_demo.db",
        "small_dim_demo.db",
        "large_dim_demo.db"
    ]
    
    cleaned_count = 0
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"✅ 已删除: {db_file}")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ 删除 {db_file} 失败: {e}")
        else:
            print(f"ℹ️  文件不存在: {db_file}")
    
    # 清理可能生成的JSON文件
    json_files = ["sample_results.json"]
    for json_file in json_files:
        if os.path.exists(json_file):
            try:
                os.remove(json_file)
                print(f"✅ 已删除: {json_file}")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ 删除 {json_file} 失败: {e}")
    
    if cleaned_count > 0:
        print(f"\n✅ 清理完成，共删除 {cleaned_count} 个文件")
    else:
        print("\n✅ 没有需要清理的文件")

def run_all_demos():
    """运行所有演示"""
    print("\n🚀 开始运行所有演示...")
    
    demos = [
        ("01_basic_usage.py", "基础使用演示"),
        ("02_advanced_features.py", "高级功能演示"),
        ("03_langchain_integration.py", "LangChain 集成演示")
    ]
    
    success_count = 0
    total_start_time = time.time()
    
    for script, description in demos:
        if run_demo(script, description):
            success_count += 1
        
        # 在演示之间添加分隔
        print("\n" + "="*60 + "\n")
        time.sleep(1)  # 短暂暂停
    
    total_time = time.time() - total_start_time
    
    print(f"🎉 所有演示运行完成!")
    print(f"✅ 成功: {success_count}/{len(demos)} 个演示")
    print(f"⏱️  总耗时: {total_time:.2f} 秒")

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("请输入选项 (0-6): ").strip()
            
            if choice == "0":
                print("\n👋 感谢使用 Milvus Lite 演示程序!")
                break
                
            elif choice == "1":
                run_demo("01_basic_usage.py", "基础使用演示")
                
            elif choice == "2":
                run_demo("02_advanced_features.py", "高级功能演示")
                
            elif choice == "3":
                run_demo("03_langchain_integration.py", "LangChain 集成演示")
                
            elif choice == "4":
                run_all_demos()
                
            elif choice == "5":
                show_demo_info()
                
            elif choice == "6":
                cleanup_databases()
                
            else:
                print("❌ 无效选项，请重新选择")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
        
        # 添加分隔线
        print("\n" + "-"*60)

if __name__ == "__main__":
    main()