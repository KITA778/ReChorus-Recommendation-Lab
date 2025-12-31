# scripts/simple_setup.py
"""
最简单的集成方案：直接使用ReChorus作为依赖
"""

import os
import sys

# 设置路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rechorus_src = os.path.join(project_root, "..", "src")

print(f"项目根目录: {project_root}")
print(f"ReChorus源码目录: {rechorus_src}")

# 检查ReChorus是否存在
if not os.path.exists(os.path.join(rechorus_src, "main.py")):
    print("错误: ReChorus源码目录不存在或没有main.py")
    sys.exit(1)

# 创建配置文件
config_content = f'''# ReChorus配置
import os
import sys

# 添加ReChorus到Python路径
sys.path.insert(0, r"{rechorus_src}")

# 添加项目源码到Python路径
sys.path.insert(0, r"{project_root}")
sys.path.insert(0, os.path.join(r"{project_root}", "src"))

print("✅ 环境设置完成")
print(f"   项目目录: {{r'{project_root}'}}")
print(f"   ReChorus目录: {{r'{rechorus_src}'}}")
'''

config_file = os.path.join(project_root, "config.py")
with open(config_file, "w", encoding="utf-8") as f:
    f.write(config_content)

print(f"创建配置文件: {config_file}")

# 创建测试脚本
test_content = '''
import sys
sys.path.insert(0, r"{}")

# 现在可以导入ReChorus模块
try:
    import main
    print("✅ 成功导入ReChorus main模块")
    print("运行: python main.py --help")
except ImportError as e:
    print(f"❌ 导入失败: {{e}}")
'''.format(rechorus_src)

test_file = os.path.join(project_root, "test_import.py")
with open(test_file, "w", encoding="utf-8") as f:
    f.write(test_content)

print(f"创建测试脚本: {test_file}")

print("\n✅ 简单集成完成!")
print("运行以下命令测试:")
print(f"  cd {project_root}")
print(f"  python test_import.py")