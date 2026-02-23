"""
测试模块
测试中药处方识别整理软件的各项功能
"""

import os
import sys
import unittest
import tempfile
import shutil
from datetime import datetime

# 导入被测试的模块
from database import DatabaseManager
from ocr_engine import OCREngine
from excel_export import ExcelExporter
from llm_api import LLMAPI
from statistics_manager import StatisticsManager


class TestDatabaseManager(unittest.TestCase):
    """测试数据库管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_db_path = os.path.join(tempfile.gettempdir(), 'test_tcm.db')
        self.db = DatabaseManager(self.test_db_path)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_init_database(self):
        """测试数据库初始化"""
        # 验证表是否创建成功
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('prescriptions', tables)
        self.assertIn('herbs', tables)
        self.assertIn('formulas', tables)
        
        conn.close()
    
    def test_save_and_get_prescription(self):
        """测试保存和获取处方"""
        prescription = {
            'patient_name': '测试患者',
            'patient_age': '30',
            'patient_gender': '男',
            'formula_name': '四君子汤',
            'symptoms': '乏力、食欲不振',
            'diagnosis': '脾胃气虚',
            'herbs': '人参 10g，白术 10g，茯苓 10g，甘草 6g',
            'dosage': '7剂',
            'usage': '水煎服，每日一剂',
            'doctor_name': '测试医生',
            'hospital': '测试医院',
            'date': '2024-01-15',
            'notes': '测试备注'
        }
        
        # 保存处方
        prescription_id = self.db.save_prescription(prescription)
        self.assertIsNotNone(prescription_id)
        
        # 获取处方
        saved = self.db.get_prescription(prescription_id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved['patient_name'], '测试患者')
        self.assertEqual(saved['formula_name'], '四君子汤')
    
    def test_search_prescriptions(self):
        """测试搜索处方"""
        # 添加测试数据
        prescription1 = {
            'patient_name': '张三',
            'formula_name': '四君子汤',
            'symptoms': '乏力',
            'date': '2024-01-15'
        }
        prescription2 = {
            'patient_name': '李四',
            'formula_name': '四物汤',
            'symptoms': '面色苍白',
            'date': '2024-01-16'
        }
        
        self.db.save_prescription(prescription1)
        self.db.save_prescription(prescription2)
        
        # 搜索
        results = self.db.search_prescriptions('张三')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['patient_name'], '张三')
        
        results = self.db.search_prescriptions('四物汤')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['patient_name'], '李四')
    
    def test_delete_prescription(self):
        """测试删除处方"""
        prescription = {
            'patient_name': '测试删除',
            'formula_name': '测试方剂',
            'date': '2024-01-15'
        }
        
        prescription_id = self.db.save_prescription(prescription)
        
        # 删除
        self.db.delete_prescription(prescription_id)
        
        # 验证删除
        deleted = self.db.get_prescription(prescription_id)
        self.assertIsNone(deleted)
    
    def test_get_statistics(self):
        """测试获取统计"""
        # 添加测试数据
        for i in range(5):
            prescription = {
                'patient_name': f'患者{i}',
                'formula_name': f'方剂{i}',
                'date': '2024-01-15'
            }
            self.db.save_prescription(prescription)
        
        stats = self.db.get_statistics()
        
        self.assertEqual(stats['total'], 5)
        self.assertEqual(stats['patients'], 5)
        self.assertEqual(stats['formulas'], 5)


class TestOCREngine(unittest.TestCase):
    """测试OCR引擎"""
    
    def setUp(self):
        """测试前准备"""
        self.ocr = OCREngine()
    
    def test_parse_prescription(self):
        """测试解析处方文本"""
        text = """
        患者：张三
        性别：男  年龄：45岁
        日期：2024年1月15日
        
        症状：头痛、眩晕、失眠多梦
        
        诊断：肾阴虚，肝阳上亢
        
        方剂：六味地黄丸加减
        
        组成：
        熟地黄 24g
        山茱萸 12g
        山药 12g
        """
        
        prescription = self.ocr.parse_prescription(text)
        
        self.assertEqual(prescription['patient_name'], '张三')
        self.assertEqual(prescription['patient_age'], '45')
        self.assertEqual(prescription['patient_gender'], '男')
        self.assertEqual(prescription['date'], '2024年1月15日')
        self.assertEqual(prescription['formula_name'], '六味地黄丸')
        self.assertEqual(prescription['diagnosis'], '肾阴虚，肝阳上亢')
    
    def test_extract_herbs(self):
        """测试提取药材"""
        text = """
        熟地黄 24g
        山茱萸 12g
        山药 12g
        泽泻 9g
        茯苓 9g
        丹皮 9g
        """
        
        herbs = self.ocr._extract_herbs(text)
        
        self.assertIn('熟地黄 24g', herbs)
        self.assertIn('山茱萸 12g', herbs)
        self.assertIn('山药 12g', herbs)
    
    def test_extract_symptoms(self):
        """测试提取症状"""
        text = "症状：头痛、眩晕、失眠多梦、腰膝酸软"
        
        symptoms = self.ocr._extract_symptoms(text)
        
        self.assertIn('头痛', symptoms)
        self.assertIn('眩晕', symptoms)
        self.assertIn('失眠', symptoms)


class TestExcelExporter(unittest.TestCase):
    """测试Excel导出器"""
    
    def setUp(self):
        """测试前准备"""
        self.exporter = ExcelExporter()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_export(self):
        """测试导出功能"""
        prescriptions = [
            {
                'patient_name': '张三',
                'patient_age': '45',
                'patient_gender': '男',
                'date': '2024-01-15',
                'symptoms': '头痛、眩晕',
                'diagnosis': '肾阴虚',
                'formula_name': '六味地黄丸',
                'herbs': '熟地黄 24g，山茱萸 12g',
                'dosage': '7剂',
                'usage': '水煎服',
                'doctor_name': '李医生',
                'hospital': '中医院',
                'notes': ''
            },
            {
                'patient_name': '李四',
                'patient_age': '30',
                'patient_gender': '女',
                'date': '2024-01-16',
                'symptoms': '乏力、食欲不振',
                'diagnosis': '脾胃气虚',
                'formula_name': '四君子汤',
                'herbs': '人参 10g，白术 10g',
                'dosage': '7剂',
                'usage': '水煎服',
                'doctor_name': '王医生',
                'hospital': '中医院',
                'notes': ''
            }
        ]
        
        output_path = os.path.join(self.test_dir, 'test_export.xlsx')
        result = self.exporter.export(prescriptions, output_path)
        
        self.assertTrue(os.path.exists(result))
        self.assertEqual(result, output_path)
    
    def test_create_template(self):
        """测试创建模板"""
        output_path = os.path.join(self.test_dir, 'test_template.xlsx')
        result = self.exporter.create_template(output_path)
        
        self.assertTrue(os.path.exists(result))


class TestLLMAPI(unittest.TestCase):
    """测试大模型API"""
    
    def setUp(self):
        """测试前准备"""
        self.llm = LLMAPI()
    
    def test_diagnose(self):
        """测试诊断功能"""
        symptoms = "头痛、眩晕、失眠多梦、腰膝酸软"
        patient_info = {'name': '张三', 'age': '45', 'gender': '男'}
        
        result = self.llm.diagnose(symptoms, patient_info)
        
        self.assertIn('【辨证】', result)
        self.assertIn('【诊断】', result)
        self.assertIn('【处方】', result)
    
    def test_parse_diagnosis_result(self):
        """测试解析诊断结果"""
        result_text = """
        【辨证】患者头痛、眩晕...
        【诊断】肾阴虚，肝阳上亢
        【治法】滋阴补肾，平肝潜阳
        【处方】六味地黄丸加减
        药物组成：
        - 熟地黄 24g
        - 山茱萸 12g
        【用法】水煎服，每日一剂
        【医嘱】注意休息
        """
        
        prescription = self.llm.parse_diagnosis_result(result_text)
        
        self.assertEqual(prescription['formula_name'], '六味地黄丸加减')
        self.assertEqual(prescription['diagnosis'], '肾阴虚，肝阳上亢')
        self.assertIn('熟地黄 24g', prescription['herbs'])


class TestStatisticsManager(unittest.TestCase):
    """测试统计管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.test_db_path = os.path.join(tempfile.gettempdir(), 'test_stats.db')
        self.db = DatabaseManager(self.test_db_path)
        self.stats = StatisticsManager()
        
        # 添加测试数据
        self._add_test_data()
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def _add_test_data(self):
        """添加测试数据"""
        prescriptions = [
            {
                'patient_name': '张三',
                'patient_age': '45',
                'patient_gender': '男',
                'formula_name': '六味地黄丸',
                'symptoms': '头痛、眩晕',
                'herbs': '熟地黄 24g，山茱萸 12g',
                'date': '2024-01-15'
            },
            {
                'patient_name': '李四',
                'patient_age': '30',
                'patient_gender': '女',
                'formula_name': '四君子汤',
                'symptoms': '乏力、食欲不振',
                'herbs': '人参 10g，白术 10g',
                'date': '2024-01-16'
            },
            {
                'patient_name': '张三',
                'patient_age': '45',
                'patient_gender': '男',
                'formula_name': '六味地黄丸',
                'symptoms': '头痛、眩晕',
                'herbs': '熟地黄 24g，山茱萸 12g',
                'date': '2024-02-15'
            }
        ]
        
        for prescription in prescriptions:
            self.db.save_prescription(prescription)
    
    def test_get_overview(self):
        """测试获取概览"""
        overview = self.stats.get_overview()
        
        self.assertIn('total', overview)
        self.assertIn('patients', overview)
        self.assertIn('formulas', overview)
    
    def test_get_herb_statistics(self):
        """测试药材统计"""
        herb_stats = self.stats.get_herb_statistics()
        
        self.assertIsInstance(herb_stats, dict)
    
    def test_get_formula_statistics(self):
        """测试方剂统计"""
        formula_stats = self.stats.get_formula_statistics()
        
        self.assertIsInstance(formula_stats, dict)
    
    def test_get_patient_statistics(self):
        """测试患者统计"""
        patient_stats = self.stats.get_patient_statistics()
        
        self.assertIn('total_patients', patient_stats)
        self.assertIn('age_distribution', patient_stats)
        self.assertIn('gender_distribution', patient_stats)
    
    def test_generate_report(self):
        """测试生成报告"""
        report = self.stats.generate_report()
        
        self.assertIn('generated_at', report)
        self.assertIn('summary', report)
        self.assertIn('herb_usage', report)
        self.assertIn('formula_usage', report)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_db_path = os.path.join(tempfile.gettempdir(), 'test_integration.db')
        self.test_dir = tempfile.mkdtemp()
        
        self.db = DatabaseManager(self.test_db_path)
        self.ocr = OCREngine()
        self.excel = ExcelExporter()
        self.llm = LLMAPI()
        # 使用同一个数据库路径
        self.stats = StatisticsManager()
        self.stats.db = self.db
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 1. 模拟OCR识别
        ocr_text = self.ocr.recognize('dummy_path')
        prescription = self.ocr.parse_prescription(ocr_text)
        
        # 2. 保存到数据库
        prescription_id = self.db.save_prescription(prescription)
        self.assertIsNotNone(prescription_id)
        
        # 3. 直接从数据库获取统计数据
        stats = self.db.get_statistics()
        self.assertGreaterEqual(stats['total'], 1)
        
        # 4. 导出Excel
        prescriptions = self.db.get_all_prescriptions()
        output_path = os.path.join(self.test_dir, 'integration_test.xlsx')
        result = self.excel.export(prescriptions, output_path)
        self.assertTrue(os.path.exists(result))
        
        # 5. AI诊断
        symptoms = "头痛、眩晕、失眠多梦"
        diagnosis = self.llm.diagnose(symptoms, {'name': '测试', 'age': '40'})
        self.assertIn('【诊断】', diagnosis)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseManager))
    suite.addTests(loader.loadTestsFromTestCase(TestOCREngine))
    suite.addTests(loader.loadTestsFromTestCase(TestExcelExporter))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestStatisticsManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("=" * 60)
    print("中药处方识别整理软件 - 测试套件")
    print("=" * 60)
    
    success = run_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("所有测试通过！")
    else:
        print("部分测试失败！")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
