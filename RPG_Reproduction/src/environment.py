
# 环境设置模块
import os
import sys

# 导入集成配置
from configs.integration_config import *

def setup_environment():
    '''设置环境'''
    print("=" * 60)
    print("ReChorus RPG复现项目 - 环境设置")
    print("=" * 60)
    
    # 显示路径信息
    print(f"项目目录: {PROJECT_ROOT}")
    print(f"ReChorus目录: {RECHORUS_ROOT}")
    print(f"数据目录: {DATA_ROOT}")
    
    # 检查关键目录
    required_dirs = [
        DATA_ROOT,
        os.path.join(DATA_ROOT, "raw"),
        os.path.join(DATA_ROOT, "processed"),
        CONFIG_ROOT,
        RESULT_ROOT,
        LOG_ROOT,
        CHECKPOINT_ROOT
    ]
    
    print("\n检查目录结构:")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} (不存在)")
    
    # 检查ReChorus模块
    print("\n检查ReChorus模块:")
    try:
        # 尝试导入ReChorus模块
        from utils import data_loader
        from models import BaseModel
        print("  ✓ ReChorus模块可用")
    except ImportError as e:
        print(f"  ✗ ReChorus模块导入失败: {e}")
    
    # 检查项目模块
    print("\n检查项目模块:")
    try:
        # 尝试导入项目模块
        from src.models.rpg_model import RPGModel
        print("  ✓ RPG模型模块可用")
    except ImportError as e:
        print(f"  ✗ 项目模块导入失败: {e}")
    
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    setup_environment()
