#!/bin/bash
# 中药处方识别整理软件 - APK构建脚本

set -e

echo "=========================================="
echo "中药处方识别整理软件 - APK构建"
echo "=========================================="

# 检查Python版本
echo ""
echo "检查Python版本..."
python3 --version

# 检查依赖
echo ""
echo "检查依赖..."
if ! command -v buildozer &> /dev/null; then
    echo "正在安装buildozer..."
    pip install buildozer
fi

# 安装项目依赖
echo ""
echo "安装项目依赖..."
pip install -r requirements.txt

# 运行测试
echo ""
echo "运行测试..."
python3 test_app.py

if [ $? -ne 0 ]; then
    echo "测试失败，请检查代码"
    exit 1
fi

echo ""
echo "测试通过！"

# 构建APK
echo ""
echo "开始构建APK..."
echo "这可能需要几分钟到几十分钟，请耐心等待..."

buildozer android debug

# 检查构建结果
if [ -f "bin/tcm_prescription-1.0.0-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo ""
    echo "=========================================="
    echo "构建成功！"
    echo "=========================================="
    echo ""
    echo "APK文件位置: bin/tcm_prescription-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
    echo ""
    echo "安装到设备:"
    echo "  buildozer android deploy run"
    echo ""
    echo "或直接复制APK到设备安装"
else
    echo ""
    echo "=========================================="
    echo "构建失败，请检查错误信息"
    echo "=========================================="
    exit 1
fi
