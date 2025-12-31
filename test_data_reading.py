import pandas as pd
import os
import sys

class Args:
    def __init__(self):
        self.data_path = 'data/'
        self.dataset = 'ml-1m'
        self.sep = ','

args = Args()

prefix = os.path.join(args.data_path, args.dataset)
sep = args.sep

print(f'数据路径: {prefix}')
print(f'分隔符: {repr(sep)}')

for key in ['train', 'valid', 'test']:
    file_path = os.path.join(prefix, key + '.csv')
    print(f'\n读取 {file_path}...')
    
    if os.path.exists(file_path):
        try:
            # 使用与ReChorus相同的方式读取
            df = pd.read_csv(file_path, sep=sep)
            print(f'  成功读取，形状: {df.shape}')
            print(f'  列名: {df.columns.tolist()}')
            
            # 检查列名
            for col in ['user_id', 'item_id', 'time']:
                if col in df.columns:
                    print(f'  ✓ 找到列: {col}')
                else:
                    print(f'  ✗ 未找到列: {col}')
            
            # 尝试排序（这是报错的地方）
            print(f'  尝试按 [\"user_id\", \"time\"] 排序...')
            sorted_df = df.sort_values(by=['user_id', 'time'])
            print(f'  ✓ 排序成功')
            
        except Exception as e:
            print(f'  ✗ 读取或排序失败: {e}')
            # 查看文件前几行
            with open(file_path, 'r', encoding='utf-8') as f:
                first_lines = f.readlines()[:3]
                print(f'  文件前3行:')
                for i, line in enumerate(first_lines):
                    print(f'    行{i}: {repr(line)}')
    else:
        print(f'  ✗ 文件不存在')
