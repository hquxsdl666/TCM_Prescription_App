#!/bin/bash
# 使用Docker构建APK

echo "=========================================="
echo "使用Docker构建APK"
echo "=========================================="

# 检查Docker
docker --version

# 运行构建容器
docker run -it --rm \
    -v $(pwd):/home/user/app \
    -w /home/user/app \
    kivy/buildozer \
    bash -c "pip install -r requirements.txt && buildozer android debug"

echo ""
echo "构建完成！"
echo "APK文件位置: bin/*.apk"
