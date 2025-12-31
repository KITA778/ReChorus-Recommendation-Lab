#!/usr/bin/env python
import os
import sys
import yaml

# 添加路径
sys.path.insert(0, r"D:\机器学习\ReChorus-master\ReChorus\src")
sys.path.insert(0, r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction")

# 导入环境设置
try:
    from src.environment import setup_environment
    setup_environment()
except ImportError as e:
    print(f"环境设置导入失败: {e}")
    print("继续运行...")

def main():
    print("=" * 60)
    print("RPG模型训练脚本")
    print("=" * 60)
    
    # 加载配置
    config_path = "configs/rpg_config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"数据集: {config['dataset']['name']}")
    print(f"训练轮数: {config['training']['epochs']}")
    
    # 尝试导入并运行训练
    try:
        # 尝试从现有模块导入
        from src.models.rpg_rechorus import RPGModel
        print("成功导入RPGModel")
        
        # 创建模型实例
        model = RPGModel(config)
        print(f"模型创建成功: {model}")
        
    except Exception as e:
        print(f"导入或创建模型失败: {e}")
        print("\n尝试替代方案: 使用ReChorus框架运行基线模型...")
        
        # 如果RPG失败，我们至少可以运行ReChorus的基线模型
        import subprocess
        print("运行SASRec作为替代...")
        subprocess.run(["python", "../src/main.py", "--model", "SASRec", "--dataset", "ml-1m"])

if __name__ == "__main__":
    main()
