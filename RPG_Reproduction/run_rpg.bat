@'
@echo off
chcp 65001 > nul

echo.
echo ===========================================
echo   RPG复现项目 - 运行脚本
echo ===========================================
echo.

REM 设置路径
set PROJECT_ROOT=D:\机器学习\ReChorus-master\ReChorus\RPG_Reproduction
set RECHORUS_SRC=D:\机器学习\ReChorus-master\ReChorus\src

echo 项目目录: %PROJECT_ROOT%
echo ReChorus目录: %RECHORUS_SRC%
echo.

REM 设置Python路径
set PYTHONPATH=%RECHORUS_SRC%;%PROJECT_ROOT%;%PYTHONPATH%

REM 激活环境
call conda activate rpg_reproduction

REM 进入项目目录
cd /d %PROJECT_ROOT%

echo 运行测试...
python test_import.py

echo.
echo 现在可以:
echo 1. 运行ReChorus: python main.py --help
echo 2. 运行数据预处理: python data_process.py --help
echo 3. 开始RPG模型实现
echo.

pause
'@ | Out-File -FilePath "run_rpg.bat" -Encoding GB2312