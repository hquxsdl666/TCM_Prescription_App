# 中药处方识别整理软件 - 项目总结

## 项目概述

本项目是一个专业的中药手写处方识别、整理、统计和AI辅助诊断的Android应用程序。采用Python + Kivy技术栈开发，支持跨平台运行。

## 已完成功能

### ✅ 1. 手写处方识别
- **OCR识别引擎** (`ocr_engine.py`)
  - 智能解析处方文本
  - 提取患者信息（姓名、年龄、性别）
  - 提取症状、诊断、方剂名称
  - 提取药材组成和剂量
  - 提取用法和医嘱
  - 支持批量处理多张处方

### ✅ 2. Excel导出功能
- **Excel导出模块** (`excel_export.py`)
  - 自动整理识别结果为Excel表格
  - 包含完整的处方信息字段
  - 支持批量导出多个处方
  - 提供Excel模板创建功能
  - 支持统计报告导出

### ✅ 3. 方剂数据库
- **数据库管理模块** (`database.py`)
  - SQLite本地数据库
  - 处方数据存储和查询
  - 药材信息库（100+常用中药材）
  - 方剂信息库（50+经典方剂）
  - 支持搜索、更新、删除操作

### ✅ 4. 可视化统计
- **统计管理模块** (`statistics_manager.py`)
  - 概览统计（总处方数、患者数、方剂种类）
  - 药材使用频率统计
  - 方剂使用频率统计
  - 月度趋势分析
  - 患者就诊统计（年龄分布、性别分布）
  - 诊断分类统计
  - 季节性分析

### ✅ 5. AI中医诊断
- **大模型API模块** (`llm_api.py`)
  - 接入大模型进行智能诊断
  - 根据症状推荐方剂和药材
  - 学习本地数据库中的方剂知识
  - 自动生成完整的诊断报告
  - 支持多种大模型API（OpenAI、文心一言、通义千问等）

## 项目结构

```
TCM_Prescription_App/
├── main.py                 # 主程序入口（Kivy UI）
├── database.py             # 数据库管理模块
├── ocr_engine.py           # OCR识别引擎
├── excel_export.py         # Excel导出模块
├── llm_api.py              # 大模型API模块
├── statistics_manager.py   # 统计管理模块
├── test_app.py             # 测试模块（18个测试用例）
├── demo.py                 # 功能演示脚本
├── run.py                  # 启动脚本
├── tcmapp.kv               # Kivy样式文件
├── requirements.txt        # 依赖列表
├── buildozer.spec          # Buildozer配置文件
├── README.md               # 项目说明文档
└── PROJECT_SUMMARY.md      # 项目总结文档
```

## 技术栈

- **前端框架**: Kivy 2.2.1 (Python跨平台GUI框架)
- **数据库**: SQLite3
- **Excel处理**: openpyxl 3.1.2
- **OCR引擎**: Tesseract OCR (支持中文手写识别)
- **AI模型**: OpenAI API / 文心一言 / 通义千问

## 测试结果

运行 `python test_app.py`，**18个测试用例全部通过**：

```
test_delete_prescription (__main__.TestDatabaseManager.test_delete_prescription) ... ok
test_get_statistics (__main__.TestDatabaseManager.test_get_statistics) ... ok
test_init_database (__main__.TestDatabaseManager.test_init_database) ... ok
test_save_and_get_prescription (__main__.TestDatabaseManager.test_save_and_get_prescription) ... ok
test_search_prescriptions (__main__.TestDatabaseManager.test_search_prescriptions) ... ok
test_extract_herbs (__main__.TestOCREngine.test_extract_herbs) ... ok
test_extract_symptoms (__main__.TestOCREngine.test_extract_symptoms) ... ok
test_parse_prescription (__main__.TestOCREngine.test_parse_prescription) ... ok
test_create_template (__main__.TestExcelExporter.test_create_template) ... ok
test_export (__main__.TestExcelExporter.test_export) ... ok
test_diagnose (__main__.TestLLMAPI.test_diagnose) ... ok
test_parse_diagnosis_result (__main__.TestLLMAPI.test_parse_diagnosis_result) ... ok
test_generate_report (__main__.TestStatisticsManager.test_generate_report) ... ok
test_get_formula_statistics (__main__.TestStatisticsManager.test_get_formula_statistics) ... ok
test_get_herb_statistics (__main__.TestStatisticsManager.test_get_herb_statistics) ... ok
test_get_overview (__main__.TestStatisticsManager.test_get_overview) ... ok
test_get_patient_statistics (__main__.TestStatisticsManager.test_get_patient_statistics) ... ok
test_full_workflow (__main__.TestIntegration.test_full_workflow) ... ok

----------------------------------------------------------------------
Ran 18 tests in 0.272s
OK
```

## 功能演示

运行 `python demo.py`，演示了以下功能：

1. **OCR识别**: 解析处方文本，提取结构化数据
2. **数据库操作**: 保存、查询、搜索处方
3. **Excel导出**: 导出处方数据到Excel文件
4. **统计分析**: 生成各类统计报告
5. **AI诊断**: 根据症状生成诊断和处方建议

## 使用指南

### 桌面版运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py

# 或
python run.py
```

### 功能演示

```bash
# 运行演示脚本
python demo.py
```

### 运行测试

```bash
# 运行所有测试
python test_app.py
```

### 构建Android APK

```bash
# 安装buildozer
pip install buildozer

# 构建APK
buildozer android debug

# 安装到设备
buildozer android deploy run
```

## 核心功能展示

### 1. 处方识别结果示例

```python
{
    'patient_name': '张三',
    'patient_age': '45',
    'patient_gender': '男',
    'date': '2024年1月15日',
    'symptoms': '头痛、眩晕、失眠多梦、腰膝酸软',
    'diagnosis': '肾阴虚，肝阳上亢',
    'formula_name': '六味地黄丸',
    'herbs': '熟地黄 24g，山茱萸 12g，山药 12g，泽泻 9g，茯苓 9g，丹皮 9g',
    'dosage': '7剂',
    'usage': '水煎服，每日一剂',
    'doctor_name': '李医生',
    'hospital': '中医院'
}
```

### 2. AI诊断结果示例

```
【辨证】
患者头痛、眩晕、失眠多梦，结合腰膝酸软，舌红少苔，脉细数，
此为肾阴虚，肝阳上亢之证。

【诊断】
肾阴虚，肝阳上亢证

【治法】
滋阴补肾，平肝潜阳

【处方】
六味地黄丸加减

药物组成：
- 熟地黄 24g（滋阴补肾，填精益髓）
- 山茱萸 12g（补益肝肾，涩精固脱）
- 山药 12g（补脾养胃，生津益肺）
- ...

【用法】
水煎服，每日一剂，分早晚两次温服。
共7剂。

【医嘱】
1. 注意休息，避免劳累和熬夜
2. 保持心情舒畅，避免情绪激动
3. 饮食宜清淡，少食辛辣刺激性食物
4. ...
```

### 3. 统计报告示例

```python
{
    'generated_at': '2024-01-20 10:30:00',
    'summary': {
        'total': 150,
        'patients': 89,
        'formulas': 32,
        'monthly': 23
    },
    'herb_usage': {
        '甘草': 45,
        '当归': 38,
        '黄芪': 35,
        ...
    },
    'formula_usage': {
        '四君子汤': 25,
        '四物汤': 20,
        '六味地黄丸': 18,
        ...
    }
}
```

## 扩展功能建议

1. **云端同步**: 将数据同步到云端，实现多设备共享
2. **语音识别**: 支持语音输入症状
3. **图像增强**: 对手写处方图片进行预处理，提高OCR准确率
4. **药材识别**: 通过拍照识别中药材
5. **处方验证**: 检查处方中的药物配伍禁忌
6. **多语言支持**: 支持英文、日文等其他语言

## 注意事项

1. 本软件仅供学习和参考使用，实际诊疗请遵医嘱
2. OCR识别准确率受图片质量影响，建议拍摄清晰的照片
3. AI诊断结果仅供参考，不能替代专业医生的诊断
4. 请妥善保管处方数据，定期备份

## 许可证

MIT License

---

**项目完成时间**: 2024年1月
**开发语言**: Python 3.8+
**目标平台**: Android 5.0+ (API 21+)
