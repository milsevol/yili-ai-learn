import os
from pymilvus import MilvusClient

def main():
    # 获取当前脚本所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 在当前目录下创建数据库文件
    db_path = os.path.join(current_dir, "01localMilvus.db")
    client = MilvusClient(db_path)
    print(f"数据库路径: {db_path}")
    if client.has_collection(collection_name="demo_collection"):
        client.drop_collection(collection_name="demo_collection")
    client.create_collection(
        collection_name="demo_collection",
        dimension=768,  # The vectors we will use in this demo has 768 dimensions
    )


if __name__ == "__main__":
    main()
