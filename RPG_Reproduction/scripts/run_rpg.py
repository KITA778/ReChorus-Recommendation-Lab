#!/usr/bin/env python
# RPG模型运行脚本

import os
import sys
import yaml
import argparse

# 设置环境
sys.path.insert(0, r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction")
from src.environment import setup_environment
setup_environment()

# 导入项目模块
from src.models.rpg_rechorus import RPGModel
from src.utils.semantic_id_generator import SemanticIDGenerator
from src.data.dataset_wrapper import RPGDataset

def parse_args():
    '''解析命令行参数'''
    parser = argparse.ArgumentParser(description='运行RPG模型')
    
    parser.add_argument('--config', type=str, default='configs/rpg_config.yaml',
                       help='配置文件路径')
    parser.add_argument('--dataset', type=str, default='ml-100k',
                       help='数据集名称')
    parser.add_argument('--epochs', type=int, default=20,
                       help='训练轮数')
    parser.add_argument('--batch_size', type=int, default=256,
                       help='批次大小')
    parser.add_argument('--semantic_id_length', type=int, default=16,
                       help='语义ID长度')
    parser.add_argument('--train', action='store_true',
                       help='训练模式')
    parser.add_argument('--test', action='store_true',
                       help='测试模式')
    parser.add_argument('--evaluate', action='store_true',
                       help='评估模式')
    
    return parser.parse_args()

def load_config(config_path):
    '''加载配置文件'''
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def main():
    '''主函数'''
    args = parse_args()
    
    print("=" * 60)
    print("RPG模型运行脚本")
    print("=" * 60)
    
    # 加载配置
    config = load_config(args.config)
    
    # 更新配置参数
    config['dataset']['name'] = args.dataset
    config['training']['epochs'] = args.epochs
    config['training']['batch_size'] = args.batch_size
    config['semantic_id']['length'] = args.semantic_id_length
    
    print(f"数据集: {args.dataset}")
    print(f"训练轮数: {args.epochs}")
    print(f"批次大小: {args.batch_size}")
    print(f"语义ID长度: {args.semantic_id_length}")
    
    if args.train:
        print("\n进入训练模式...")
        # 这里调用训练函数
        from scripts.train_rpg import train_rpg_model
        train_rpg_model(config)
    
    elif args.test:
        print("\n进入测试模式...")
        # 这里调用测试函数
        from scripts.test_rpg import test_rpg_model
        test_rpg_model(config)
    
    elif args.evaluate:
        print("\n进入评估模式...")
        # 这里调用评估函数
        from scripts.evaluate_rpg import evaluate_rpg_model
        evaluate_rpg_model(config)
    
    else:
        print("\n请指定模式: --train, --test 或 --evaluate")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
