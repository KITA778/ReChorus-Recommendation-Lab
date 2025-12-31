
import sys
sys.path.insert(0, r"D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction\..\src")

# 现在可以导入ReChorus模块
try:
    import main
    print("✅ 成功导入ReChorus main模块")
    print("运行: python main.py --help")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
