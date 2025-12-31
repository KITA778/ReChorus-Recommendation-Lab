
# ReChorus集成配置
import os
import sys

# 项目根目录
PROJECT_ROOT = r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction"

# ReChorus根目录
RECHORUS_ROOT = r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction\.."

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
