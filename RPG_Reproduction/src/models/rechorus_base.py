# src/models/rechorus_base.py
"""
ReChorus框架兼容的模型基类
用于将RPG模型集成到ReChorus框架中
"""

import torch
import torch.nn as nn
import numpy as np
from abc import ABC, abstractmethod

class ReChorusBaseModel(nn.Module, ABC):
    """ReChorus兼容的模型基类"""
    
    def __init__(self, config, dataset):
        """
        初始化基类
        
        Args:
            config: 配置字典
            dataset: 数据集对象
        """
        super(ReChorusBaseModel, self).__init__()
        self.config = config
        self.dataset = dataset
        
        # 设备设置
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 模型参数
        self.n_users = dataset.n_users
        self.n_items = dataset.n_items
        
        print(f"初始化模型: {self.__class__.__name__}")
        print(f"用户数: {self.n_users}")
        print(f"物品数: {self.n_items}")
        print(f"使用设备: {self.device}")
    
    @abstractmethod
    def forward(self, batch_data):
        """
        前向传播
        
        Args:
            batch_data: 批次数据字典
            
        Returns:
            predictions: 预测结果
        """
        pass
    
    @abstractmethod
    def calculate_loss(self, batch_data):
        """
        计算损失
        
        Args:
            batch_data: 批次数据字典
            
        Returns:
            loss: 损失值
            loss_dict: 损失字典
        """
        pass
    
    def predict(self, batch_data):
        """
        预测 (用于评估)
        
        Args:
            batch_data: 批次数据字典
            
        Returns:
            predictions: 预测结果
        """
        # 默认实现，返回前向传播结果
        return self.forward(batch_data)
    
    def save_model(self, path):
        """保存模型"""
        torch.save({
            'model_state_dict': self.state_dict(),
            'config': self.config,
            'n_users': self.n_users,
            'n_items': self.n_items
        }, path)
        print(f"模型已保存到: {path}")
    
    def load_model(self, path):
        """加载模型"""
        checkpoint = torch.load(path, map_location=self.device)
        self.load_state_dict(checkpoint['model_state_dict'])
        print(f"模型已从 {path} 加载")
    
    def freeze_parameters(self):
        """冻结所有参数"""
        for param in self.parameters():
            param.requires_grad = False
    
    def unfreeze_parameters(self):
        """解冻所有参数"""
        for param in self.parameters():
            param.requires_grad = True
    
    def count_parameters(self):
        """统计参数数量"""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        return {
            'total': total_params,
            'trainable': trainable_params,
            'non_trainable': total_params - trainable_params
        }
    
    def summary(self):
        """打印模型摘要"""
        print("=" * 60)
        print(f"模型: {self.__class__.__name__}")
        print("=" * 60)
        
        # 参数统计
        param_counts = self.count_parameters()
        print(f"总参数: {param_counts['total']:,}")
        print(f"可训练参数: {param_counts['trainable']:,}")
        print(f"不可训练参数: {param_counts['non_trainable']:,}")
        
        # 层信息
        print("\n模型结构:")
        for name, module in self.named_children():
            num_params = sum(p.numel() for p in module.parameters())
            print(f"  {name}: {module.__class__.__name__} ({num_params:,} 参数)")
        
        print("=" * 60)


class ReChorusDataLoader:
    """ReChorus兼容的数据加载器"""
    
    def __init__(self, dataset, config):
        self.dataset = dataset
        self.config = config
        self.batch_size = config.get('batch_size', 256)
        
    def get_train_loader(self):
        """获取训练数据加载器"""
        from torch.utils.data import DataLoader
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=0,
            collate_fn=self.collate_fn
        )
    
    def get_test_loader(self):
        """获取测试数据加载器"""
        from torch.utils.data import DataLoader
        return DataLoader(
            self.dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=0,
            collate_fn=self.collate_fn
        )
    
    @staticmethod
    def collate_fn(batch):
        """
        批处理函数
        
        Args:
            batch: 批次数据列表
            
        Returns:
            批处理后的数据
        """
        # 默认实现，假设batch是元组列表
        if isinstance(batch[0], tuple):
            # 按列收集
            return tuple(torch.stack([item[i] for item in batch]) for i in range(len(batch[0])))
        elif isinstance(batch[0], dict):
            # 字典类型
            keys = batch[0].keys()
            return {key: torch.stack([item[key] for item in batch]) for key in keys}
        else:
            # 其他类型，直接堆叠
            return torch.stack(batch)