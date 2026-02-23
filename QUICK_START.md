# 快速入门指南

## 环境准备

### 1. 安装Python 3.8+
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# macOS
brew install python3

# Windows
# 从官网下载安装: https://www.python.org/downloads/
```

### 2. 安装依赖
```bash
cd TCM_Prescription_App
pip install -r requirements.txt
```

## 快速开始

### 方式1：运行桌面版应用
```bash
python main.py
```

### 方式2：运行演示脚本
```bash
python demo.py
```

### 方式3：运行测试
```bash
python test_app.py
```

## 构建Android APK

### 方法1：使用Buildozer（推荐）

```bash
# 安装buildozer
pip install buildozer

# 构建APK
buildozer android debug

# 安装到设备
buildozer android deploy run
```

### 方法2：使用Docker

```bash
# 运行Docker构建脚本
bash docker_build.sh
```

### 方法3：使用提供的构建脚本

```bash
# 运行构建脚本
bash build_apk.sh
```

## 应用使用指南

### 主界面功能

1. **📷 扫描处方** - 拍照或选择图片识别处方
2. **📋 处方记录** - 查看和管理所有处方
3. **📊 统计分析** - 查看各类统计报告
4. **🤖 AI诊断开方** - 输入症状获取AI诊断建议

### 扫描处方流程

1. 点击"扫描处方"
2. 选择"拍照"或"从相册选择"
3. 点击"识别"按钮
4. 查看识别结果
5. 确认无误后点击"保存"

### 批量处理流程

1. 进入"批量处理"界面
2. 点击"选择文件"选择多张处方图片
3. 点击"开始处理"
4. 处理完成后导出Excel

### AI诊断流程

1. 点击"AI诊断开方"
2. 输入患者症状
3. 填写患者基本信息（姓名、年龄）
4. 点击"AI诊断开方"
5. 查看诊断结果
6. 点击"保存处方"保存到数据库

## 配置说明

### 配置OCR引擎（可选）

默认使用模拟OCR，如需真实OCR识别：

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# macOS
brew install tesseract tesseract-lang

# 然后在 ocr_engine.py 中启用真实OCR
```

### 配置大模型API（可选）

```bash
# 设置环境变量
export OPENAI_API_KEY='your-api-key'

# 或在 llm_api.py 中直接设置
```

## 常见问题

### Q: 应用启动失败？
A: 检查是否安装了所有依赖：`pip install -r requirements.txt`

### Q: OCR识别不准确？
A: 
- 确保处方图片清晰
- 尽量使文字水平
- 确保光线充足
- 可以手动编辑识别结果

### Q: 如何备份数据？
A: 
- 数据库文件位于用户目录下的 `tcm_prescriptions.db`
- 可以通过"导出Excel"功能备份所有处方

### Q: 构建APK失败？
A:
- 确保安装了Android SDK和NDK
- 检查buildozer配置是否正确
- 尝试使用Docker构建

## 文件说明

```
TCM_Prescription_App/
├── main.py              # 主程序入口
├── database.py          # 数据库模块
├── ocr_engine.py        # OCR识别模块
├── excel_export.py      # Excel导出模块
├── llm_api.py           # AI诊断模块
├── statistics_manager.py # 统计模块
├── test_app.py          # 测试文件
├── demo.py              # 演示脚本
├── requirements.txt     # 依赖列表
├── buildozer.spec       # APK构建配置
└── README.md            # 详细说明
```

## 技术支持

如有问题，请查看：
1. README.md - 详细项目说明
2. PROJECT_SUMMARY.md - 项目总结
3. 测试文件 - 了解功能使用方法

---

**注意**: 本软件仅供学习和参考，实际诊疗请遵医嘱。
