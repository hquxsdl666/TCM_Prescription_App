#!/usr/bin/env python3
"""
中药处方识别整理软件 - 功能演示
"""

import os
import sys
import tempfile

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from ocr_engine import OCREngine
from excel_export import ExcelExporter
from llm_api import LLMAPI
from statistics_manager import StatisticsManager


def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_ocr():
    """演示OCR识别功能"""
    print_header("1. OCR识别功能演示")
    
    ocr = OCREngine()
    
    # 模拟处方文本
    prescription_text = """
    中医处方
    
    患者：张三
    性别：男  年龄：45岁
    日期：2024年1月15日
    
    症状：头痛、眩晕、失眠多梦、腰膝酸软、舌红少苔、脉细数
    
    诊断：肾阴虚，肝阳上亢
    
    方剂：六味地黄丸加减
    
    组成：
    熟地黄 24g
    山茱萸 12g
    山药 12g
    泽泻 9g
    茯苓 9g
    丹皮 9g
    枸杞子 15g
    菊花 10g
    
    用法：水煎服，每日一剂，早晚分服
    
    医师：李医生
    医院：中医院
    """
    
    print("原始处方文本：")
    print(prescription_text)
    
    print("\n解析结果：")
    prescription = ocr.parse_prescription(prescription_text)
    
    for key, value in prescription.items():
        if value:
            print(f"  {key}: {value}")
    
    return prescription


def demo_database(prescription):
    """演示数据库功能"""
    print_header("2. 数据库功能演示")
    
    # 使用临时数据库
    db_path = os.path.join(tempfile.gettempdir(), 'demo_tcm.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db = DatabaseManager(db_path)
    
    # 保存处方
    print("保存处方到数据库...")
    prescription_id = db.save_prescription(prescription)
    print(f"  处方ID: {prescription_id}")
    
    # 添加更多测试数据
    test_prescriptions = [
        {
            'patient_name': '李四',
            'patient_age': '32',
            'patient_gender': '女',
            'formula_name': '四物汤',
            'symptoms': '月经不调、面色苍白、头晕眼花',
            'diagnosis': '血虚证',
            'herbs': '当归 10g，川芎 6g，白芍 10g，熟地黄 15g',
            'dosage': '7剂',
            'usage': '水煎服，每日一剂',
            'doctor_name': '王医生',
            'hospital': '中医院',
            'date': '2024-01-16'
        },
        {
            'patient_name': '王五',
            'patient_age': '28',
            'patient_gender': '男',
            'formula_name': '四君子汤',
            'symptoms': '乏力、食欲不振、腹胀便溏',
            'diagnosis': '脾胃气虚',
            'herbs': '人参 10g，白术 10g，茯苓 10g，甘草 6g',
            'dosage': '10剂',
            'usage': '水煎服，每日一剂',
            'doctor_name': '李医生',
            'hospital': '中医院',
            'date': '2024-01-17'
        }
    ]
    
    for p in test_prescriptions:
        db.save_prescription(p)
    
    print(f"  共保存 {len(test_prescriptions) + 1} 个处方")
    
    # 查询所有处方
    print("\n查询所有处方：")
    all_prescriptions = db.get_all_prescriptions()
    for i, p in enumerate(all_prescriptions, 1):
        print(f"  {i}. {p['patient_name']} - {p['formula_name']} ({p['date']})")
    
    # 搜索功能
    print("\n搜索'张三'：")
    results = db.search_prescriptions('张三')
    for p in results:
        print(f"  - {p['patient_name']}: {p['diagnosis']}")
    
    # 获取统计
    print("\n数据库统计：")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    return db


def demo_excel(db):
    """演示Excel导出功能"""
    print_header("3. Excel导出功能演示")
    
    exporter = ExcelExporter()
    
    # 获取所有处方
    prescriptions = db.get_all_prescriptions()
    
    # 导出到Excel
    output_path = os.path.join(tempfile.gettempdir(), 'demo_prescriptions.xlsx')
    result = exporter.export(prescriptions, output_path)
    
    print(f"Excel文件已导出到: {result}")
    print(f"  包含 {len(prescriptions)} 个处方记录")
    
    # 创建模板
    template_path = os.path.join(tempfile.gettempdir(), 'demo_template.xlsx')
    exporter.create_template(template_path)
    print(f"\nExcel模板已创建: {template_path}")
    
    return result


def demo_statistics(db):
    """演示统计功能"""
    print_header("4. 统计分析功能演示")
    
    stats = StatisticsManager()
    stats.db = db
    
    # 概览统计
    print("概览统计：")
    overview = stats.get_overview()
    for key, value in overview.items():
        print(f"  {key}: {value}")
    
    # 药材统计
    print("\n常用药材（前5）：")
    herb_stats = stats.get_herb_statistics(5)
    for herb, count in herb_stats.items():
        print(f"  {herb}: {count}次")
    
    # 方剂统计
    print("\n常用方剂（前5）：")
    formula_stats = stats.get_formula_statistics(5)
    for formula, count in formula_stats.items():
        print(f"  {formula}: {count}次")
    
    # 患者统计
    print("\n患者统计：")
    patient_stats = stats.get_patient_statistics()
    print(f"  总患者数: {patient_stats['total_patients']}")
    print(f"  复诊患者: {patient_stats['revisit_patients']}")
    print(f"  复诊率: {patient_stats['revisit_rate']:.1f}%")
    
    # 生成完整报告
    print("\n生成统计报告...")
    report = stats.generate_report()
    print(f"  报告生成时间: {report['generated_at']}")
    
    return stats


def demo_ai_diagnosis():
    """演示AI诊断功能"""
    print_header("5. AI诊断功能演示")
    
    llm = LLMAPI()
    
    # 模拟症状
    symptoms = "头痛、眩晕、失眠多梦、腰膝酸软"
    patient_info = {
        'name': '测试患者',
        'age': '45',
        'gender': '男'
    }
    
    print(f"患者症状: {symptoms}")
    print(f"患者信息: {patient_info}")
    print("\nAI诊断结果：")
    
    result = llm.diagnose(symptoms, patient_info)
    print(result)
    
    # 解析诊断结果
    print("\n解析诊断结果为结构化数据：")
    prescription = llm.parse_diagnosis_result(result)
    for key, value in prescription.items():
        if value:
            print(f"  {key}: {value}")
    
    return result


def main():
    """主函数"""
    print("=" * 60)
    print("中药处方识别整理软件 - 功能演示")
    print("Traditional Chinese Medicine Prescription Manager")
    print("=" * 60)
    
    try:
        # 1. OCR识别
        prescription = demo_ocr()
        
        # 2. 数据库操作
        db = demo_database(prescription)
        
        # 3. Excel导出
        excel_path = demo_excel(db)
        
        # 4. 统计分析
        stats = demo_statistics(db)
        
        # 5. AI诊断
        diagnosis = demo_ai_diagnosis()
        
        # 总结
        print_header("演示完成")
        print("✅ 所有功能演示成功！")
        print(f"\n生成的文件：")
        print(f"  - 数据库: {tempfile.gettempdir()}\\demo_tcm.db")
        print(f"  - Excel: {excel_path}")
        print(f"  - 模板: {tempfile.gettempdir()}\\demo_template.xlsx")
        
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理
        print("\n清理临时文件...")
        db_path = os.path.join(tempfile.gettempdir(), 'demo_tcm.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"  已删除: {db_path}")


if __name__ == '__main__':
    main()
