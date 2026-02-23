"""
统计管理模块
提供处方数据的可视化统计分析
"""

import json
import datetime
from collections import Counter
from database import DatabaseManager


class StatisticsManager:
    """统计管理器"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_overview(self):
        """获取概览统计"""
        return self.db.get_statistics()
    
    def get_detailed_stats(self):
        """获取详细统计"""
        stats = {
            'overview': self.get_overview(),
            'herb_stats': self.get_herb_statistics(),
            'formula_stats': self.get_formula_statistics(),
            'trend_stats': self.get_trend_statistics(),
            'patient_stats': self.get_patient_statistics(),
            'monthly_comparison': self.get_monthly_comparison(),
        }
        return stats
    
    def get_herb_statistics(self, top_n=20):
        """
        获取药材使用统计
        
        Args:
            top_n: 返回前N个最常用药材
        
        Returns:
            药材使用统计字典
        """
        herb_counts = self.db.get_herb_usage_stats()
        
        # 排序并取前N个
        sorted_herbs = sorted(herb_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_herbs[:top_n])
    
    def get_formula_statistics(self, top_n=20):
        """
        获取方剂使用统计
        
        Args:
            top_n: 返回前N个最常用方剂
        
        Returns:
            方剂使用统计字典
        """
        formula_counts = self.db.get_formula_usage_stats()
        
        # 排序并取前N个
        sorted_formulas = sorted(formula_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_formulas[:top_n])
    
    def get_trend_statistics(self, months=12):
        """
        获取趋势统计
        
        Args:
            months: 返回最近几个月的数据
        
        Returns:
            月度趋势字典
        """
        return self.db.get_monthly_trend(months)
    
    def get_patient_statistics(self):
        """获取患者统计"""
        prescriptions = self.db.get_all_prescriptions()
        
        # 患者就诊次数统计
        patient_visits = {}
        patient_ages = {}
        patient_genders = {'男': 0, '女': 0, '未知': 0}
        
        for prescription in prescriptions:
            name = prescription.get('patient_name', '未知')
            
            # 就诊次数
            patient_visits[name] = patient_visits.get(name, 0) + 1
            
            # 年龄统计
            age = prescription.get('patient_age', '')
            if age and age.isdigit():
                age_group = self._get_age_group(int(age))
                patient_ages[age_group] = patient_ages.get(age_group, 0) + 1
            
            # 性别统计
            gender = prescription.get('patient_gender', '未知')
            if gender in patient_genders:
                patient_genders[gender] += 1
            else:
                patient_genders['未知'] += 1
        
        # 复诊患者统计
        revisit_patients = {name: count for name, count in patient_visits.items() if count > 1}
        
        return {
            'total_patients': len(patient_visits),
            'revisit_patients': len(revisit_patients),
            'revisit_rate': len(revisit_patients) / len(patient_visits) * 100 if patient_visits else 0,
            'age_distribution': patient_ages,
            'gender_distribution': patient_genders,
            'top_patients': dict(sorted(patient_visits.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def _get_age_group(self, age):
        """获取年龄分组"""
        if age < 18:
            return '未成年(0-17)'
        elif age < 30:
            return '青年(18-29)'
        elif age < 40:
            return '青壮年(30-39)'
        elif age < 50:
            return '中年(40-49)'
        elif age < 60:
            return '中老年(50-59)'
        else:
            return '老年(60+)'
    
    def get_monthly_comparison(self):
        """获取月度对比数据"""
        current_date = datetime.datetime.now()
        
        comparisons = []
        
        for i in range(6):  # 最近6个月
            month_date = current_date - datetime.timedelta(days=30*i)
            month_str = month_date.strftime('%Y-%m')
            
            # 获取该月数据
            prescriptions = self.db.get_all_prescriptions()
            month_count = sum(1 for p in p.get('date', '').startswith(month_str) 
                            for p in prescriptions)
            
            comparisons.append({
                'month': month_str,
                'count': month_count
            })
        
        return comparisons
    
    def get_diagnosis_statistics(self):
        """获取诊断统计"""
        prescriptions = self.db.get_all_prescriptions()
        
        diagnosis_counts = {}
        
        for prescription in prescriptions:
            diagnosis = prescription.get('diagnosis', '')
            if diagnosis:
                # 简化诊断名称
                simplified = self._simplify_diagnosis(diagnosis)
                diagnosis_counts[simplified] = diagnosis_counts.get(simplified, 0) + 1
        
        return dict(sorted(diagnosis_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _simplify_diagnosis(self, diagnosis):
        """简化诊断名称"""
        # 去除常见修饰词
        modifiers = ['证', '型', '偏', '明显', '轻度', '重度', '急性', '慢性']
        
        simplified = diagnosis
        for modifier in modifiers:
            simplified = simplified.replace(modifier, '')
        
        return simplified.strip()
    
    def get_symptom_statistics(self, top_n=30):
        """获取症状统计"""
        prescriptions = self.db.get_all_prescriptions()
        
        symptom_counts = {}
        
        # 常见症状关键词
        common_symptoms = [
            '头痛', '头晕', '眩晕', '耳鸣', '失眠', '多梦', '心悸', '胸闷',
            '胸痛', '咳嗽', '咳痰', '气喘', '胃痛', '胃胀', '呕吐', '恶心',
            '腹痛', '腹胀', '腹泻', '便秘', '腰痛', '腰酸', '尿频', '尿急',
            '口干', '口苦', '口渴', '汗出', '发热', '恶寒', '怕冷', '乏力',
            '疲倦', '食欲不振', '消化不良', '便秘', '腹泻', '月经不调', '痛经'
        ]
        
        for prescription in prescriptions:
            symptoms_text = prescription.get('symptoms', '')
            
            for symptom in common_symptoms:
                if symptom in symptoms_text:
                    symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        
        # 排序并取前N个
        sorted_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_symptoms[:top_n])
    
    def get_doctor_statistics(self):
        """获取医生开方统计"""
        prescriptions = self.db.get_all_prescriptions()
        
        doctor_counts = {}
        
        for prescription in prescriptions:
            doctor = prescription.get('doctor_name', '未知')
            if doctor:
                doctor_counts[doctor] = doctor_counts.get(doctor, 0) + 1
        
        return dict(sorted(doctor_counts.items(), key=lambda x: x[1], reverse=True))
    
    def get_seasonal_statistics(self):
        """获取季节性统计"""
        prescriptions = self.db.get_all_prescriptions()
        
        seasonal_data = {
            '春季(3-5月)': {'count': 0, 'top_diagnoses': []},
            '夏季(6-8月)': {'count': 0, 'top_diagnoses': []},
            '秋季(9-11月)': {'count': 0, 'top_diagnoses': []},
            '冬季(12-2月)': {'count': 0, 'top_diagnoses': []},
        }
        
        seasonal_diagnoses = {
            '春季(3-5月)': [],
            '夏季(6-8月)': [],
            '秋季(9-11月)': [],
            '冬季(12-2月)': [],
        }
        
        for prescription in prescriptions:
            date_str = prescription.get('date', '')
            if date_str:
                try:
                    month = int(date_str.split('-')[1])
                    diagnosis = prescription.get('diagnosis', '')
                    
                    if 3 <= month <= 5:
                        seasonal_data['春季(3-5月)']['count'] += 1
                        seasonal_diagnoses['春季(3-5月)'].append(diagnosis)
                    elif 6 <= month <= 8:
                        seasonal_data['夏季(6-8月)']['count'] += 1
                        seasonal_diagnoses['夏季(6-8月)'].append(diagnosis)
                    elif 9 <= month <= 11:
                        seasonal_data['秋季(9-11月)']['count'] += 1
                        seasonal_diagnoses['秋季(9-11月)'].append(diagnosis)
                    else:
                        seasonal_data['冬季(12-2月)']['count'] += 1
                        seasonal_diagnoses['冬季(12-2月)'].append(diagnosis)
                
                except:
                    pass
        
        # 统计各季节常见诊断
        for season, diagnoses in seasonal_diagnoses.items():
            diagnosis_counts = Counter(diagnoses)
            seasonal_data[season]['top_diagnoses'] = dict(diagnosis_counts.most_common(5))
        
        return seasonal_data
    
    def generate_report(self, start_date=None, end_date=None):
        """
        生成统计报告
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            报告字典
        """
        report = {
            'generated_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'period': {
                'start': start_date or '全部',
                'end': end_date or '全部'
            },
            'summary': self.get_overview(),
            'herb_usage': self.get_herb_statistics(30),
            'formula_usage': self.get_formula_statistics(30),
            'monthly_trend': self.get_trend_statistics(12),
            'patient_analysis': self.get_patient_statistics(),
            'symptom_analysis': self.get_symptom_statistics(30),
            'diagnosis_analysis': self.get_diagnosis_statistics(),
            'seasonal_analysis': self.get_seasonal_statistics(),
        }
        
        return report
    
    def export_report_to_json(self, report, output_path):
        """导出报告为JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def get_chart_data(self):
        """获取图表数据"""
        return {
            'overview': self.get_overview(),
            'herb_stats': self.get_herb_statistics(10),
            'formula_stats': self.get_formula_statistics(10),
            'trend_stats': self.get_trend_statistics(6),
            'symptom_stats': self.get_symptom_statistics(10),
        }
