# scripts/create_test_data.py
"""
创建测试数据
"""

import os
import pandas as pd
import numpy as np

def create_test_datasets():
    """创建测试数据集"""
    
    # 创建数据目录
    data_dir = "data/processed"
    os.makedirs(data_dir, exist_ok=True)
    
    # 创建ml-100k数据集
    create_ml100k_dataset(data_dir)
    
    # 创建ml-1m数据集
    create_ml1m_dataset(data_dir)
    
    print("测试数据集创建完成!")

def create_ml100k_dataset(data_dir):
    """创建ml-100k测试数据集"""
    np.random.seed(42)
    
    n_users = 100
    n_items = 200
    n_interactions = 5000
    
    # 生成交互数据
    data = {
        'user_id': np.random.randint(0, n_users, n_interactions),
        'item_id': np.random.randint(0, n_items, n_interactions),
        'rating': np.random.randint(1, 6, n_interactions),
        'timestamp': np.arange(n_interactions)
    }
    
    df = pd.DataFrame(data)
    
    # 按用户分割
    train_data, valid_data, test_data = [], [], []
    
    for user_id in range(n_users):
        user_interactions = df[df['user_id'] == user_id]
        
        if len(user_interactions) < 10:
            continue
        
        # 排序
        user_interactions = user_interactions.sort_values('timestamp')
        
        # 分割
        n = len(user_interactions)
        train_end = int(n * 0.7)
        valid_end = int(n * 0.8)
        
        train_data.append(user_interactions.iloc[:train_end])
        valid_data.append(user_interactions.iloc[train_end:valid_end])
        test_data.append(user_interactions.iloc[valid_end:])
    
    # 合并
    train_df = pd.concat(train_data)
    valid_df = pd.concat(valid_data)
    test_df = pd.concat(test_data)
    
    # 保存
    train_df.to_csv(f"{data_dir}/ml-100k_train.csv", index=False)
    valid_df.to_csv(f"{data_dir}/ml-100k_valid.csv", index=False)
    test_df.to_csv(f"{data_dir}/ml-100k_test.csv", index=False)
    
    print(f"ml-100k数据集创建完成:")
    print(f"  训练集: {len(train_df)} 条记录")
    print(f"  验证集: {len(valid_df)} 条记录")
    print(f"  测试集: {len(test_df)} 条记录")

def create_ml1m_dataset(data_dir):
    """创建ml-1m测试数据集"""
    np.random.seed(42)
    
    n_users = 200
    n_items = 400
    n_interactions = 10000
    
    # 生成交互数据
    data = {
        'user_id': np.random.randint(0, n_users, n_interactions),
        'item_id': np.random.randint(0, n_items, n_interactions),
        'rating': np.random.randint(1, 6, n_interactions),
        'timestamp': np.arange(n_interactions)
    }
    
    df = pd.DataFrame(data)
    
    # 按用户分割
    train_data, valid_data, test_data = [], [], []
    
    for user_id in range(n_users):
        user_interactions = df[df['user_id'] == user_id]
        
        if len(user_interactions) < 10:
            continue
        
        # 排序
        user_interactions = user_interactions.sort_values('timestamp')
        
        # 分割
        n = len(user_interactions)
        train_end = int(n * 0.7)
        valid_end = int(n * 0.8)
        
        train_data.append(user_interactions.iloc[:train_end])
        valid_data.append(user_interactions.iloc[train_end:valid_end])
        test_data.append(user_interactions.iloc[valid_end:])
    
    # 合并
    train_df = pd.concat(train_data)
    valid_df = pd.concat(valid_data)
    test_df = pd.concat(test_data)
    
    # 保存
    train_df.to_csv(f"{data_dir}/ml-1m_train.csv", index=False)
    valid_df.to_csv(f"{data_dir}/ml-1m_valid.csv", index=False)
    test_df.to_csv(f"{data_dir}/ml-1m_test.csv", index=False)
    
    print(f"ml-1m数据集创建完成:")
    print(f"  训练集: {len(train_df)} 条记录")
    print(f"  验证集: {len(valid_df)} 条记录")
    print(f"  测试集: {len(test_df)} 条记录")

def create_semantic_ids():
    """创建语义ID数据"""
    
    data_dir = "data/semantic_ids"
    os.makedirs(data_dir, exist_ok=True)
    
    # 创建模拟的语义ID
    np.random.seed(42)
    
    # ml-100k物品的语义ID
    n_items_100k = 200
    semantic_id_length = 16
    codebook_size = 256
    
    semantic_ids_100k = np.random.randint(
        0, codebook_size, 
        size=(n_items_100k, semantic_id_length)
    )
    
    # 保存
    np.save(f"{data_dir}/ml-100k_semantic_ids.npy", semantic_ids_100k)
    
    # ml-1m物品的语义ID
    n_items_1m = 400
    semantic_ids_1m = np.random.randint(
        0, codebook_size,
        size=(n_items_1m, semantic_id_length)
    )
    
    np.save(f"{data_dir}/ml-1m_semantic_ids.npy", semantic_ids_1m)
    
    print("语义ID数据创建完成:")
    print(f"  ml-100k语义ID: {semantic_ids_100k.shape}")
    print(f"  ml-1m语义ID: {semantic_ids_1m.shape}")

if __name__ == "__main__":
    print("开始创建测试数据...")
    create_test_datasets()
    create_semantic_ids()
    print("所有测试数据创建完成!")