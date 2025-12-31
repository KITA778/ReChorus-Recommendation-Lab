# scripts/integrate_rechorus.py
import os
import sys
import shutil

def create_integration():
    """创建ReChorus集成"""
    
    # 获取当前目录和ReChorus目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    rechorus_root = os.path.join(project_root, "..")  # ReChorus主目录
    
    print(f"项目根目录: {project_root}")
    print(f"ReChorus目录: {rechorus_root}")
    
    # 检查ReChorus关键文件
    required_files = {
        "main.py": "主程序入口",
        "data_process.py": "数据预处理",
        "src/__init__.py": "源代码包",
        "src/models/__init__.py": "模型包",
        "src/utils/__init__.py": "工具包"
    }
    
    print("\n检查ReChorus关键文件:")
    for file, desc in required_files.items():
        file_path = os.path.join(rechorus_root, file)
        if os.path.exists(file_path):
            print(f"✓ {file}: {desc}")
        else:
            print(f"✗ {file}: 未找到")
    
    # 创建集成配置文件
    create_config_file(project_root, rechorus_root)
    
    # 创建环境设置文件
    create_environment_setup(project_root, rechorus_root)
    
    # 创建运行脚本
    create_run_scripts(project_root, rechorus_root)
    
    print("\n=== ReChorus集成完成 ===")
    print("现在你可以:")
    print("1. 使用 scripts/run_rpg.py 运行RPG模型")
    print("2. 使用 scripts/run_baseline.py 运行基线模型")
    print("3. 使用 scripts/evaluate_all.py 评估所有模型")

def create_config_file(project_root, rechorus_root):
    """创建集成配置文件"""
    
    config_content = f"""
# ReChorus集成配置
import os
import sys

# 项目根目录
PROJECT_ROOT = r"{project_root}"

# ReChorus根目录
RECHORUS_ROOT = r"{rechorus_root}"

# 数据目录
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")

# 配置目录
CONFIG_ROOT = os.path.join(PROJECT_ROOT, "configs")

# 结果目录
RESULT_ROOT = os.path.join(PROJECT_ROOT, "results")

# 日志目录
LOG_ROOT = os.path.join(PROJECT_ROOT, "logs")

# 检查点目录
CHECKPOINT_ROOT = os.path.join(PROJECT_ROOT, "checkpoints")

# 设置Python路径
def setup_paths():
    '''设置Python路径'''
    # 添加ReChorus源代码路径
    rechorus_src = os.path.join(RECHORUS_ROOT, "src")
    if rechorus_src not in sys.path:
        sys.path.insert(0, rechorus_src)
    
    # 添加项目源代码路径
    project_src = os.path.join(PROJECT_ROOT, "src")
    if project_src not in sys.path:
        sys.path.insert(0, project_src)
    
    # 添加当前目录
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
    
    return True

# 自动设置路径
setup_paths()
"""
    
    config_file = os.path.join(project_root, "configs", "integration_config.py")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print(f"创建集成配置文件: {config_file}")

def create_environment_setup(project_root, rechorus_root):
    """创建环境设置模块"""
    
    env_content = f"""
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
    print(f"项目目录: {{PROJECT_ROOT}}")
    print(f"ReChorus目录: {{RECHORUS_ROOT}}")
    print(f"数据目录: {{DATA_ROOT}}")
    
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
    
    print("\\n检查目录结构:")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✓ {{dir_path}}")
        else:
            print(f"  ✗ {{dir_path}} (不存在)")
    
    # 检查ReChorus模块
    print("\\n检查ReChorus模块:")
    try:
        # 尝试导入ReChorus模块
        from utils import data_loader
        from models import BaseModel
        print("  ✓ ReChorus模块可用")
    except ImportError as e:
        print(f"  ✗ ReChorus模块导入失败: {{e}}")
    
    # 检查项目模块
    print("\\n检查项目模块:")
    try:
        # 尝试导入项目模块
        from src.models.rpg_model import RPGModel
        print("  ✓ RPG模型模块可用")
    except ImportError as e:
        print(f"  ✗ 项目模块导入失败: {{e}}")
    
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    setup_environment()
"""
    
    env_file = os.path.join(project_root, "src", "environment.py")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print(f"创建环境设置模块: {env_file}")

def create_run_scripts(project_root, rechorus_root):
    """创建运行脚本"""
    
    # 创建RPG运行脚本
    rpg_script = f"""#!/usr/bin/env python
# RPG模型运行脚本

import os
import sys
import yaml
import argparse

# 设置环境
sys.path.insert(0, r"{project_root}")
from src.environment import setup_environment
setup_environment()

# 导入项目模块
from src.models.rpg_model import RPGModel
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
    
    print(f"数据集: {{args.dataset}}")
    print(f"训练轮数: {{args.epochs}}")
    print(f"批次大小: {{args.batch_size}}")
    print(f"语义ID长度: {{args.semantic_id_length}}")
    
    if args.train:
        print("\\n进入训练模式...")
        # 这里调用训练函数
        from scripts.train_rpg import train_rpg_model
        train_rpg_model(config)
    
    elif args.test:
        print("\\n进入测试模式...")
        # 这里调用测试函数
        from scripts.test_rpg import test_rpg_model
        test_rpg_model(config)
    
    elif args.evaluate:
        print("\\n进入评估模式...")
        # 这里调用评估函数
        from scripts.evaluate_rpg import evaluate_rpg_model
        evaluate_rpg_model(config)
    
    else:
        print("\\n请指定模式: --train, --test 或 --evaluate")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
"""
    
    rpg_script_file = os.path.join(project_root, "scripts", "run_rpg.py")
    with open(rpg_script_file, "w", encoding="utf-8") as f:
        f.write(rpg_script)
    
    # 设置执行权限
    os.chmod(rpg_script_file, 0o755)
    
    print(f"创建RPG运行脚本: {rpg_script_file}")

if __name__ == "__main__":
    create_integration()