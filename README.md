# 中药处方识别整理软件

一款专业的中药手写处方识别、整理、统计和AI辅助诊断的Android应用程序。

## 功能特点

### 1. 手写处方识别
- 📷 支持拍照识别手写处方
- 🖼️ 支持从相册选择图片识别
- 🔍 智能解析处方内容（患者信息、症状、诊断、方剂、药材等）
- 📁 支持批量处理多张处方图片

### 2. Excel导出
- 📊 自动整理识别结果为Excel表格
- 📋 包含完整的处方信息：患者姓名、年龄、性别、日期、症状、诊断、方剂、药材、用法等
- 💾 支持批量导出多个处方
- 📄 提供Excel模板下载

### 3. 方剂数据库
- 🗄️ 本地SQLite数据库存储所有处方
- 🔍 支持按患者姓名、方剂名称、症状等搜索
- 📈 可视化统计功能
  - 药材使用频率统计
  - 方剂使用频率统计
  - 月度趋势分析
  - 患者就诊统计
  - 诊断分类统计

### 4. AI中医诊断
- 🤖 接入大模型API进行智能诊断
- 📚 学习本地数据库中的方剂知识
- 💡 根据症状推荐方剂和药材
- 📝 自动生成完整的诊断报告

## 技术架构

- **前端框架**: Kivy (Python跨平台GUI框架)
- **数据库**: SQLite
- **OCR引擎**: Tesseract OCR (支持中文手写识别)
- **Excel处理**: openpyxl
- **AI模型**: OpenAI API / 文心一言 / 通义千问等

## 安装说明

### 环境要求
- Python 3.8+
- Android 5.0+ (API 21+)

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行桌面版
```bash
python main.py
```

### 构建Android APK

#### 方法一：使用Buildozer

1. 安装buildozer
```bash
pip install buildozer
```

2. 构建APK
```bash
buildozer android debug
```

3. 安装到设备
```bash
buildozer android deploy run
```

#### 方法二：使用Docker

```bash
docker run -it --rm \
    -v $(pwd):/home/user/app \
    kivy/buildozer \
    buildozer android debug
```

## 使用指南

### 首次使用
1. 打开应用，进入主界面
2. 点击"扫描处方"开始识别处方
3. 拍照或从相册选择处方图片
4. 点击"识别"按钮进行OCR识别
5. 查看识别结果，确认无误后点击"保存"

### 批量处理
1. 进入"批量处理"界面
2. 选择多个处方图片
3. 点击"开始处理"
4. 处理完成后导出Excel

### 查看统计
1. 点击主界面的"统计分析"
2. 查看各种统计图表
3. 了解药材使用频率、方剂使用趋势等

### AI诊断
1. 点击"AI诊断开方"
2. 输入患者症状
3. 填写患者基本信息
4. 点击"AI诊断开方"
5. 查看诊断结果并保存

## 项目结构

```
TCM_Prescription_App/
├── main.py                 # 主程序入口
├── database.py             # 数据库管理模块
├── ocr_engine.py           # OCR识别引擎
├── excel_export.py         # Excel导出模块
├── llm_api.py              # 大模型API模块
├── statistics_manager.py   # 统计管理模块
├── test_app.py             # 测试模块
├── requirements.txt        # 依赖列表
├── buildozer.spec          # Buildozer配置文件
└── README.md               # 项目说明
```

## 测试

运行测试套件：
```bash
python test_app.py
```

## 配置说明

### OCR配置
在 `ocr_engine.py` 中配置Tesseract路径：
```python
# Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Linux/Mac
# 通常不需要配置，使用系统默认路径
```

### 大模型API配置
在 `llm_api.py` 中配置API密钥：
```python
# 方式1：环境变量
export OPENAI_API_KEY='your-api-key'

# 方式2：代码中设置
llm = LLMAPI(api_key='your-api-key')
```

## 常见问题

### Q: OCR识别准确率低怎么办？
A: 
1. 确保处方图片清晰，光线充足
2. 尽量使处方文字水平
3. 可以手动编辑识别结果后保存

### Q: 如何备份数据？
A:
1. 数据库文件位于应用数据目录
2. 可以通过"导出Excel"功能备份所有处方
3. 定期导出数据到安全位置

### Q: 支持哪些大模型API？
A:
- OpenAI GPT-4/GPT-3.5
- 百度文心一言
- 阿里通义千问
- 本地部署的开源模型

## 更新日志

### v1.0.0 (2024-01)
- 初始版本发布
- 实现处方识别、Excel导出、数据库管理、AI诊断等核心功能

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎反馈。

---

**注意**: 本软件仅供学习和参考使用，实际诊疗请遵医嘱。
