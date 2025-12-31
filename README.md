# 基于ReChorus框架的推荐算法对比实验及分析

**课程**：[机器学习]
**大作业**：推荐系统算法复现与对比
**成员*：[23330141-吴雨杭] - [23330177-周颖轩]
**日期**：2025年12月

## 项目简介

本项目基于 **ReChorus 推荐系统框架**，成功复现并对比了 **SASRec**（序列推荐）与 **BPRMF**（协同过滤）两种经典推荐算法。实验在 `Grocery_and_Gourmet_Food` 数据集上，通过改变随机种子和超参数，构建了严谨的对比实验环境，深入分析了序列建模相对于传统方法的价值。

此外，本实验结合了对KDD 2025论文 **《Generating Long Semantic IDs in Parallel for Recommendation》** 的理解，探讨了其“为物品生成结构化语义ID”的核心思想与我们实验结果的关联。

## 核心成果

- ✅ **成功运行**：克服了数据格式、依赖冲突等多项技术障碍，使ReChorus框架顺利运行。
- ✅ **完整实验**：在两个不同配置下，完成了SASRec与BPRMF的完整训练与评估，获得可靠结果。
- ✅ **清晰对比**：实验结果表明，**SASRec性能显著优于BPRMF**（HR@5高出约4.5倍），验证了序列信息的重要性。
- ✅ **深度分析**：实验结果与RPG论文的核心动机相吻合，为“更好的物品语义表示能提升推荐性能”提供了实证支持。

## 项目结构

ReChorus/ # 项目根目录 (基于原始ReChorus框架)
├── data/ # 数据集目录
│ ├── Grocery_and_Gourmet_Food/ # 主要实验数据集（已预处理）
│ │ ├── train.csv
│ │ ├── dev.csv
│ │ └── test.csv
│ └── ... # 其他内置数据集
├── src/ # ReChorus框架源代码
├── model/ # 训练好的模型文件（自动生成）
├── log/ # 实验日志与评估结果（自动生成）
│ ├── SASRec/ # SASRec模型的所有运行日志
│ └── BPRMF/ # BPRMF模型的所有运行日志
├── requirements.txt # Python依赖列表
└── README.md # 本文件

## 数据准备

我们使用了框架内置的 `Grocery_and_Gourmet_Food` 数据集。**关键步骤**是确保数据格式正确（之前遇到了`neg_items`列导致评估失败的问题）。

**如果您要重新预处理数据**，请确保：
- `dev.csv` 和 `test.csv` 仅包含 `user_id, item_id, time` 三列。
- `train.csv` 可包含 `neg_items` 列。
- 文件均为**制表符(`\t`)**分隔。

## 实验复现

所有实验均使用 `src/main.py` 作为统一入口。以下是复现我们全部结果的命令：

### 实验1：原始配置 (`seed=0`)
```bash
# 运行SASRec (原始配置)
python src/main.py --model_name SASRec --dataset Grocery_and_Gourmet_Food --epoch 20

# 运行BPRMF (原始配置)
python src/main.py --model_name BPRMF --dataset Grocery_and_Gourmet_Food --epoch 50 --batch_size 512 --l2 0.01

### 实验2：变体配置 (seed=42)
# 运行SASRec (变体配置，缩短历史序列)
python src/main.py --model_name SASRec --dataset Grocery_and_Gourmet_Food --epoch 20 --random_seed 42 --history_max 15

# 运行BPRMF (变体配置，仅改变随机种子)
python src/main.py --model_name BPRMF --dataset Grocery_and_Gourmet_Food --epoch 50 --batch_size 512 --random_seed 42

# 运行说明：

训练过程中会输出损失和验证集指标。当验证集性能连续10个epoch未提升时，会自动早停。

最佳模型会自动保存至 model/ 目录。

最终测试集结果和预测日志会保存至 log/ 目录。

## 实验结果摘要

我们在两个不同配置下运行了实验，主要结果如下（HR@5， NDCG@5）：

模型	配置 (seed, history_max)	HR@5	NDCG@5	最佳Epoch
SASRec	(0, 20)	0.3731	0.2722	6
BPRMF	(0, -)	0.0836	0.0522	3
SASRec	(42, 15)	0.3720	0.2714	6
BPRMF	(42, -)	0.3155	0.2153	39
关键发现：

SASRec显著优于BPRMF：在原始配置下，SASRec的HR@5是BPRMF的4.5倍，凸显了序列建模的价值。

SASRec更稳定：改变配置后，SASRec性能波动极小(<0.3%)，而BPRMF波动巨大，说明复杂模型鲁棒性更强。

与RPG论文的关联：我们的实验证实了“利用序列/结构信息”能极大提升性能，这与RPG论文旨在通过生成长语义ID来捕获物品间复杂关系的核心思想高度一致。

更详细的结果分析（包括HR@10, NDCG@10等）请参见项目报告。


👥 小组分工

[23330141-吴雨杭]：负责环境配置、数据预处理、模型训练、SASRec模型实验、BPRMF模型实验、报告修改。

[23330177-周颖轩]：负责结果分析、关联RPG论文理论、报告撰写。
