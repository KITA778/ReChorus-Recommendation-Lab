# scripts/main_rpg.py
"""
RPG模型主运行脚本
集成了ReChorus框架的功能
"""

import os
import sys
import yaml
import argparse
import torch
import numpy as np
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.environment import setup_environment
from src.models.rpg_rechorus import create_rpg_model
from src.data.rechorus_dataset import create_dataset
from src.utils.rechorus_trainer import ReChorusTrainer

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='RPG模型主运行脚本')
    
    parser.add_argument('--config', type=str, default='configs/rpg_config.yaml',
                       help='配置文件路径')
    parser.add_argument('--dataset', type=str, default='ml-100k',
                       help='数据集名称')
    parser.add_argument('--mode', type=str, default='train',
                       choices=['train', 'test', 'evaluate', 'tune'],
                       help='运行模式')
    parser.add_argument('--epochs', type=int, default=20,
                       help='训练轮数')
    parser.add_argument('--batch_size', type=int, default=256,
                       help='批次大小')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                       help='学习率')
    parser.add_argument('--semantic_id_length', type=int, default=16,
                       help='语义ID长度')
    parser.add_argument('--seed', type=int, default=42,
                       help='随机种子')
    parser.add_argument('--use_cuda', action='store_true',
                       help='使用CUDA')
    parser.add_argument('--debug', action='store_true',
                       help='调试模式')
    
    return parser.parse_args()

def load_config(config_path):
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def set_random_seed(seed):
    """设置随机种子"""
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    print(f"设置随机种子: {seed}")

def setup_device(use_cuda):
    """设置设备"""
    if use_cuda and torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"使用设备: CUDA ({torch.cuda.get_device_name(0)})")
    else:
        device = torch.device('cpu')
        print(f"使用设备: CPU")
    
    return device

def run_training(config, args):
    """运行训练"""
    print("\n" + "="*60)
    print("开始训练RPG模型")
    print("="*60)
    
    # 创建数据集
    print("创建数据集...")
    train_dataset = create_dataset(config, mode='train')
    valid_dataset = create_dataset(config, mode='valid')
    
    # 获取数据集统计
    train_stats = train_dataset.get_statistics()
    valid_stats = valid_dataset.get_statistics()
    
    print(f"训练集统计: {train_stats}")
    print(f"验证集统计: {valid_stats}")
    
    # 更新配置
    config['n_users'] = train_stats['n_users']
    config['n_items'] = train_stats['n_items']
    
    # 创建模型
    print("创建模型...")
    model = create_rpg_model(config, train_dataset)
    
    # 创建训练器
    print("创建训练器...")
    trainer = ReChorusTrainer(model, config)
    
    # 训练模型
    print("开始训练...")
    trainer.train(train_dataset, valid_dataset)
    
    print("训练完成!")

def run_testing(config, args):
    """运行测试"""
    print("\n" + "="*60)
    print("开始测试RPG模型")
    print("="*60)
    
    # 创建数据集
    print("创建测试数据集...")
    test_dataset = create_dataset(config, mode='test')
    test_stats = test_dataset.get_statistics()
    
    print(f"测试集统计: {test_stats}")
    
    # 更新配置
    config['n_users'] = test_stats['n_users']
    config['n_items'] = test_stats['n_items']
    
    # 创建模型
    print("创建模型...")
    model = create_rpg_model(config, test_dataset)
    
    # 加载检查点
    checkpoint_path = config.get('checkpoint_path', 'checkpoints/best_model.pt')
    if os.path.exists(checkpoint_path):
        print(f"加载检查点: {checkpoint_path}")
        model.load_model(checkpoint_path)
    else:
        print(f"警告: 检查点不存在 {checkpoint_path}")
    
    # 创建训练器
    print("创建训练器...")
    trainer = ReChorusTrainer(model, config)
    
    # 测试模型
    print("开始测试...")
    test_results = trainer.test(test_dataset)
    
    print(f"测试结果: {test_results}")
    
    # 保存结果
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = os.path.join(results_dir, f'test_results_{timestamp}.json')
    
    import json
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    print(f"测试结果已保存到: {results_file}")

def run_evaluation(config, args):
    """运行评估"""
    print("\n" + "="*60)
    print("开始评估RPG模型")
    print("="*60)
    
    # 这里可以添加与其他模型的对比评估
    print("评估功能开发中...")
    
    # 暂时调用测试函数
    run_testing(config, args)

def main():
    """主函数"""
    # 解析参数
    args = parse_args()
    
    # 设置环境
    setup_environment()
    
    # 设置随机种子
    set_random_seed(args.seed)
    
    # 加载配置
    config = load_config(args.config)
    
    # 更新配置参数
    config['dataset_name'] = args.dataset
    config['training']['epochs'] = args.epochs
    config['training']['batch_size'] = args.batch_size
    config['training']['learning_rate'] = args.learning_rate
    config['semantic_id']['length'] = args.semantic_id_length
    config['debug'] = args.debug
    
    # 设置设备
    device = setup_device(args.use_cuda)
    config['device'] = device
    
    # 根据模式运行
    if args.mode == 'train':
        run_training(config, args)
    elif args.mode == 'test':
        run_testing(config, args)
    elif args.mode == 'evaluate':
        run_evaluation(config, args)
    elif args.mode == 'tune':
        print("超参数调优功能开发中...")
    else:
        print(f"未知模式: {args.mode}")
    
    print("\n" + "="*60)
    print("RPG模型运行完成")
    print("="*60)

if __name__ == "__main__":
    main()