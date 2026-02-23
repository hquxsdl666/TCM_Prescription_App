"""
数据库管理模块
使用SQLite存储处方数据
"""

import sqlite3
import json
import datetime
import os
from pathlib import Path


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # 默认数据库路径
            self.db_path = os.path.join(
                os.path.expanduser('~'),
                'tcm_prescriptions.db'
            )
        else:
            self.db_path = db_path
        
        self.init_database()
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 创建处方表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                patient_age TEXT,
                patient_gender TEXT,
                formula_name TEXT,
                symptoms TEXT,
                diagnosis TEXT,
                herbs TEXT,
                dosage TEXT,
                usage TEXT,
                doctor_name TEXT,
                hospital TEXT,
                date TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建药材表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS herbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                pinyin TEXT,
                category TEXT,
                properties TEXT,
                functions TEXT,
                usage_dosage TEXT,
                contraindications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建方剂表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS formulas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                pinyin TEXT,
                category TEXT,
                composition TEXT,
                functions TEXT,
                indications TEXT,
                usage TEXT,
                modifications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_prescriptions_name 
            ON prescriptions(patient_name)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_prescriptions_date 
            ON prescriptions(date)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_prescriptions_formula 
            ON prescriptions(formula_name)
        ''')
        
        conn.commit()
        conn.close()
        
        # 初始化基础数据
        self.init_base_data()
    
    def init_base_data(self):
        """初始化基础药材和方剂数据"""
        # 常用中药材
        common_herbs = [
            ('人参', 'renshen', '补气药', '甘、微苦，微温', '大补元气，复脉固脱，补脾益肺，生津养血，安神益智', '3-9g', '实证、热证忌服'),
            ('黄芪', 'huangqi', '补气药', '甘，微温', '补气升阳，固表止汗，利水消肿，生津养血', '9-30g', '表实邪盛、气滞湿阻忌服'),
            ('当归', 'danggui', '补血药', '甘、辛，温', '补血活血，调经止痛，润肠通便', '6-12g', '湿盛中满、大便溏泄忌服'),
            ('白术', 'baizhu', '补气药', '苦、甘，温', '健脾益气，燥湿利水，止汗，安胎', '6-12g', '阴虚燥渴、气滞胀闷忌服'),
            ('茯苓', 'fuling', '利水渗湿药', '甘、淡，平', '利水渗湿，健脾，宁心', '10-15g', '虚寒精滑忌服'),
            ('甘草', 'gancao', '补气药', '甘，平', '补脾益气，清热解毒，祛痰止咳，缓急止痛', '2-10g', '湿盛胀满、水肿者忌服'),
            ('川芎', 'chuanxiong', '活血化瘀药', '辛，温', '活血行气，祛风止痛', '3-10g', '阴虚火旺、舌红口干者忌服'),
            ('熟地黄', 'shudihuang', '补血药', '甘，微温', '补血滋阴，益精填髓', '9-15g', '脾胃虚弱、气滞痰多者忌服'),
            ('白芍', 'baishao', '补血药', '苦、酸，微寒', '养血调经，敛阴止汗，柔肝止痛', '6-15g', '虚寒腹痛泄泻者慎服'),
            ('党参', 'dangshen', '补气药', '甘，平', '健脾益肺，养血生津', '9-30g', '实证、热证忌服'),
        ]
        
        # 常用方剂
        common_formulas = [
            ('四君子汤', 'sijunzitang', '补气剂', '人参、白术、茯苓、甘草', '益气健脾', '脾胃气虚证', '水煎服'),
            ('四物汤', 'siwutang', '补血剂', '当归、川芎、白芍、熟地黄', '补血和血', '营血虚滞证', '水煎服'),
            ('六味地黄丸', 'liuweidihuangwan', '补阴剂', '熟地黄、山茱萸、山药、泽泻、茯苓、丹皮', '滋阴补肾', '肾阴虚证', '蜜丸，温水送服'),
            ('补中益气汤', 'buzhongyiqitang', '补气剂', '黄芪、人参、白术、甘草、当归、陈皮、升麻、柴胡', '补中益气，升阳举陷', '脾胃气虚、中气下陷', '水煎服'),
            ('当归补血汤', 'dangguibuxuetang', '补血剂', '黄芪、当归', '补气生血', '血虚发热证', '水煎服'),
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 插入药材数据
        for herb in common_herbs:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO herbs 
                    (name, pinyin, category, properties, functions, usage_dosage, contraindications)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', herb)
            except:
                pass
        
        # 插入方剂数据
        for formula in common_formulas:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO formulas 
                    (name, pinyin, category, composition, functions, indications, usage)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', formula)
            except:
                pass
        
        conn.commit()
        conn.close()
    
    def save_prescription(self, prescription):
        """保存处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO prescriptions 
            (patient_name, patient_age, patient_gender, formula_name, symptoms, 
             diagnosis, herbs, dosage, usage, doctor_name, hospital, date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            prescription.get('patient_name', ''),
            prescription.get('patient_age', ''),
            prescription.get('patient_gender', ''),
            prescription.get('formula_name', ''),
            prescription.get('symptoms', ''),
            prescription.get('diagnosis', ''),
            prescription.get('herbs', ''),
            prescription.get('dosage', ''),
            prescription.get('usage', ''),
            prescription.get('doctor_name', ''),
            prescription.get('hospital', ''),
            prescription.get('date', datetime.datetime.now().strftime('%Y-%m-%d')),
            prescription.get('notes', '')
        ))
        
        conn.commit()
        prescription_id = cursor.lastrowid
        conn.close()
        
        return prescription_id
    
    def get_prescription(self, prescription_id):
        """获取单个处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM prescriptions WHERE id = ?
        ''', (prescription_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row, cursor)
        return None
    
    def get_all_prescriptions(self, limit=None, offset=None):
        """获取所有处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM prescriptions ORDER BY created_at DESC'
        params = []
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        if offset:
            query += ' OFFSET ?'
            params.append(offset)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    def search_prescriptions(self, keyword):
        """搜索处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f'%{keyword}%'
        
        cursor.execute('''
            SELECT * FROM prescriptions 
            WHERE patient_name LIKE ? 
            OR formula_name LIKE ?
            OR symptoms LIKE ?
            OR diagnosis LIKE ?
            OR herbs LIKE ?
            ORDER BY created_at DESC
        ''', (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    def update_prescription(self, prescription_id, updates):
        """更新处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 构建更新语句
        fields = []
        values = []
        
        for key, value in updates.items():
            if key != 'id':
                fields.append(f'{key} = ?')
                values.append(value)
        
        values.append(prescription_id)
        
        query = f'''
            UPDATE prescriptions 
            SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def delete_prescription(self, prescription_id):
        """删除处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM prescriptions WHERE id = ?', (prescription_id,))
        
        conn.commit()
        conn.close()
    
    def clear_all(self):
        """清空所有处方"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM prescriptions')
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """获取统计数据"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 总处方数
        cursor.execute('SELECT COUNT(*) FROM prescriptions')
        total = cursor.fetchone()[0]
        
        # 患者数
        cursor.execute('SELECT COUNT(DISTINCT patient_name) FROM prescriptions')
        patients = cursor.fetchone()[0]
        
        # 方剂种类
        cursor.execute('SELECT COUNT(DISTINCT formula_name) FROM prescriptions')
        formulas = cursor.fetchone()[0]
        
        # 本月新增
        current_month = datetime.datetime.now().strftime('%Y-%m')
        cursor.execute('''
            SELECT COUNT(*) FROM prescriptions 
            WHERE date LIKE ?
        ''', (f'{current_month}%',))
        monthly = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'patients': patients,
            'formulas': formulas,
            'monthly': monthly
        }
    
    def get_herb_usage_stats(self):
        """获取药材使用统计"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT herbs FROM prescriptions')
        rows = cursor.fetchall()
        
        herb_counts = {}
        for row in rows:
            herbs_text = row[0]
            if herbs_text:
                # 简单的药材计数（实际应用中需要更精确的解析）
                herbs = herbs_text.split('，')
                for herb in herbs:
                    herb = herb.strip()
                    if herb:
                        herb_counts[herb] = herb_counts.get(herb, 0) + 1
        
        conn.close()
        
        return herb_counts
    
    def get_formula_usage_stats(self):
        """获取方剂使用统计"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT formula_name, COUNT(*) as count 
            FROM prescriptions 
            WHERE formula_name IS NOT NULL AND formula_name != ''
            GROUP BY formula_name
            ORDER BY count DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return {row[0]: row[1] for row in rows}
    
    def get_monthly_trend(self, months=12):
        """获取月度趋势"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT substr(date, 1, 7) as month, COUNT(*) as count
            FROM prescriptions
            WHERE date IS NOT NULL
            GROUP BY month
            ORDER BY month DESC
            LIMIT ?
        ''', (months,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return {row[0]: row[1] for row in rows}
    
    def _row_to_dict(self, row, cursor):
        """将数据库行转换为字典"""
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))
    
    def get_herb_info(self, herb_name):
        """获取药材信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM herbs WHERE name = ?', (herb_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row, cursor)
        return None
    
    def get_formula_info(self, formula_name):
        """获取方剂信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM formulas WHERE name = ?', (formula_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row, cursor)
        return None
    
    def search_formulas(self, keyword):
        """搜索方剂"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f'%{keyword}%'
        
        cursor.execute('''
            SELECT * FROM formulas 
            WHERE name LIKE ? 
            OR indications LIKE ?
            OR functions LIKE ?
        ''', (search_pattern, search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
