[app]

# 应用标题
title = 中药处方识别整理

# 包名
package.name = tcm_prescription

# 包域名
package.domain = org.example

# 源文件
source.dir = .

# 包含的文件
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,db

# 版本号
version = 1.0.0

# 依赖项
requirements = python3,kivy==2.2.1,kivymd==1.1.1,openpyxl==3.1.2,python-dateutil==2.8.2,Pillow

# 图标
# icon.filename = %(source.dir)s/data/icon.png

# 启动画面
# presplash.filename = %(source.dir)s/data/presplash.png

# 方向
orientation = portrait

# 全屏
fullscreen = 0

# Android API版本
android.api = 33

# Android NDK版本
android.ndk = 25b

# Android SDK版本
android.sdk = 33

# 最低API版本
android.minapi = 21

# 目标API版本
android.targetapi = 33

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA

# 架构
android.archs = arm64-v8a, armeabi-v7a

# 添加Android权限说明
android.meta_data = android.support.FILE_PROVIDER_PATHS=./file_provider_paths.xml

[buildozer]

# 日志级别
log_level = 2

# 警告模式
warn_on_root = 1

# 构建目录
build_dir = ./.buildozer

# 二进制目录
bin_dir = ./bin
