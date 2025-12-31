# ReChorus配置
import os
import sys

# 添加ReChorus到Python路径
sys.path.insert(0, r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction\..\src")

# 添加项目源码到Python路径
sys.path.insert(0, r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction")
sys.path.insert(0, os.path.join(r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction", "src"))

print("✅ 环境设置完成")
print(f"   项目目录: {r'D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction'}")
print(f"   ReChorus目录: {r'D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction\..\src'}")
