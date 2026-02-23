"""
OCR识别引擎
支持手写中药处方识别
"""

import re
import os
from pathlib import Path


class OCREngine:
    """OCR识别引擎"""
    
    def __init__(self):
        # 常用中药材名称（用于提高识别准确性）
        self.common_herbs = [
            '人参', '黄芪', '当归', '白术', '茯苓', '甘草', '川芎', '熟地黄', '白芍', '党参',
            '麦冬', '五味子', '肉桂', '附子', '干姜', '大枣', '生姜', '葱白', '豆豉', '薄荷',
            '柴胡', '葛根', '升麻', '防风', '荆芥', '羌活', '独活', '白芷', '细辛', '藁本',
            '苍耳子', '辛夷', '香薷', '紫苏', '生姜', '葱白', '桂枝', '麻黄', '桑叶', '菊花',
            '薄荷', '牛蒡子', '蝉蜕', '淡豆豉', '葛根', '柴胡', '升麻', '蔓荆子', '浮萍', '木贼',
            '石膏', '知母', '芦根', '天花粉', '竹叶', '淡竹叶', '鸭跖草', '栀子', '夏枯草', '决明子',
            '谷精草', '密蒙花', '青葙子', '黄芩', '黄连', '黄柏', '龙胆', '秦皮', '苦参', '白鲜皮',
            '金银花', '连翘', '蒲公英', '紫花地丁', '野菊花', '穿心莲', '大青叶', '板蓝根', '青黛', '贯众',
            '生地', '玄参', '丹皮', '赤芍', '紫草', '水牛角', '青蒿', '白薇', '地骨皮', '银柴胡',
            '胡黄连', '大黄', '芒硝', '番泻叶', '芦荟', '火麻仁', '郁李仁', '甘遂', '京大戟', '芫花',
            '商陆', '牵牛子', '巴豆', '独活', '木瓜', '威灵仙', '蕲蛇', '乌梢蛇', '川乌', '草乌',
            '附子', '桂枝', '桑枝', '桑寄生', '五加皮', '香加皮', '千年健', '雪莲花', '鹿衔草', '石楠叶',
            '藿香', '佩兰', '苍术', '厚朴', '砂仁', '白豆蔻', '草豆蔻', '草果', '茯苓', '薏苡仁',
            '泽泻', '猪苓', '车前子', '滑石', '木通', '通草', '瞿麦', '萹蓄', '地肤子', '海金沙',
            '石韦', '冬葵子', '灯心草', '茵陈', '金钱草', '虎杖', '垂盆草', '鸡骨草', '珍珠草', '附子',
            '干姜', '肉桂', '吴茱萸', '小茴香', '丁香', '高良姜', '花椒', '胡椒', '荜茇', '荜澄茄',
            '陈皮', '青皮', '枳实', '枳壳', '木香', '香附', '乌药', '沉香', '檀香', '川楝子',
            '荔枝核', '佛手', '香橼', '玫瑰花', '绿萼梅', '娑罗子', '薤白', '天仙藤', '大腹皮', '甘松',
            '山楂', '神曲', '麦芽', '谷芽', '莱菔子', '鸡内金', '使君子', '苦楝皮', '槟榔', '南瓜子',
            '鹤草芽', '雷丸', '鹤虱', '榧子', '大蓟', '小蓟', '地榆', '槐花', '侧柏叶', '白茅根',
            '苎麻根', '三七', '茜草', '蒲黄', '花蕊石', '降香', '白及', '仙鹤草', '紫珠叶', '棕榈炭',
            '血余炭', '藕节', '炮姜', '艾叶', '川芎', '延胡索', '郁金', '姜黄', '乳香', '没药',
            '五灵脂', '丹参', '红花', '桃仁', '益母草', '泽兰', '牛膝', '鸡血藤', '王不留行', '月季花',
            '凌霄花', '土鳖虫', '自然铜', '苏木', '骨碎补', '血竭', '儿茶', '刘寄奴', '莪术', '三棱',
            '水蛭', '虻虫', '斑蝥', '穿山甲', '半夏', '天南星', '白附子', '白芥子', '皂荚', '旋覆花',
            '白前', '猫爪草', '川贝母', '浙贝母', '瓜蒌', '竹茹', '竹沥', '天竺黄', '海藻', '昆布',
            '黄药子', '海蛤壳', '海浮石', '瓦楞子', '礞石', '杏仁', '紫苏子', '百部', '紫菀', '款冬花',
            '马兜铃', '枇杷叶', '桑白皮', '葶苈子', '白果', '矮地茶', '洋金花', '华山参', '罗汉果', '满山红',
            '朱砂', '磁石', '龙骨', '琥珀', '酸枣仁', '柏子仁', '远志', '合欢皮', '首乌藤', '灵芝',
            '缬草', '首乌藤', '麝香', '冰片', '苏合香', '石菖蒲', '蟾酥', '樟脑', '牛黄', '珍珠',
            '天麻', '钩藤', '石决明', '决明子', '谷精草', '刺蒺藜', '罗布麻叶', '珍珠母', '牡蛎', '赭石',
            '羚羊角', '牛黄', '珍珠', '钩藤', '天麻', '地龙', '全蝎', '蜈蚣', '僵蚕', '水牛角'
        ]
        
        # 常用方剂名称
        self.common_formulas = [
            '四君子汤', '四物汤', '六味地黄丸', '补中益气汤', '当归补血汤',
            '归脾汤', '炙甘草汤', '生脉散', '玉屏风散', '参苓白术散',
            '理中丸', '小建中汤', '大建中汤', '吴茱萸汤', '四逆汤',
            '当归四逆汤', '黄芪桂枝五物汤', '阳和汤', '小柴胡汤', '大柴胡汤',
            '逍遥散', '加味逍遥散', '半夏泻心汤', '白虎汤', '清营汤',
            '黄连解毒汤', '凉膈散', '普济消毒饮', '导赤散', '龙胆泻肝汤',
            '清胃散', '玉女煎', '芍药汤', '白头翁汤', '青蒿鳖甲汤',
            '香薷散', '六一散', '清暑益气汤', '理中丸', '小建中汤',
            '吴茱萸汤', '四逆汤', '当归四逆汤', '黄芪桂枝五物汤', '阳和汤',
            '麻黄汤', '桂枝汤', '小青龙汤', '大青龙汤', '九味羌活汤',
            '银翘散', '桑菊饮', '麻黄杏仁甘草石膏汤', '败毒散', '再造散',
            '加减葳蕤汤', '大承气汤', '小承气汤', '调胃承气汤', '大黄牡丹汤',
            '温脾汤', '麻子仁丸', '济川煎', '十枣汤', '黄龙汤',
            '小柴胡汤', '大柴胡汤', '蒿芩清胆汤', '达原饮', '四逆散',
            '逍遥散', '加味逍遥散', '半夏泻心汤', '白虎汤', '清营汤',
            '黄连解毒汤', '凉膈散', '普济消毒饮', '导赤散', '龙胆泻肝汤',
            '清胃散', '玉女煎', '芍药汤', '白头翁汤', '青蒿鳖甲汤',
            '香薷散', '六一散', '清暑益气汤', '理中丸', '小建中汤',
            '吴茱萸汤', '四逆汤', '当归四逆汤', '黄芪桂枝五物汤', '阳和汤'
        ]
        
        # 症状关键词
        self.symptom_keywords = [
            '头痛', '头晕', '眩晕', '耳鸣', '耳聋', '目赤', '目昏', '目涩',
            '鼻塞', '流涕', '喷嚏', '咽痛', '咽痒', '咳嗽', '咳痰', '气喘',
            '胸闷', '胸痛', '心悸', '心慌', '失眠', '多梦', '健忘', '嗜睡',
            '口渴', '口干', '口苦', '口臭', '口疮', '牙痛', '牙龈肿痛',
            '胃痛', '胃胀', '呕吐', '恶心', '反酸', '嗳气', '食欲不振',
            '腹痛', '腹胀', '腹泻', '便秘', '便血', '痔疮', '脱肛',
            '腰痛', '腰酸', '腰重', '腰冷', '尿频', '尿急', '尿痛', '尿血',
            '遗精', '早泄', '阳痿', '性欲减退', '月经不调', '痛经', '闭经',
            '带下', '不孕', '乳房胀痛', '乳癖', '中风', '半身不遂', '口眼歪斜',
            '发热', '恶寒', '怕冷', '畏寒', '汗出', '无汗', '自汗', '盗汗',
            '身重', '身痛', '关节痛', '肌肉酸痛', '麻木', '抽搐', '震颤',
            '烦躁', '易怒', '抑郁', '焦虑', '神疲', '乏力', '倦怠', '嗜卧',
            '面色萎黄', '面色苍白', '面色潮红', '面色晦暗', '黄褐斑', '痤疮',
            '舌淡', '舌红', '舌紫', '苔白', '苔黄', '苔腻', '脉浮', '脉沉',
            '脉迟', '脉数', '脉虚', '脉实', '脉滑', '脉涩', '脉弦', '脉细'
        ]
    
    def recognize(self, image_path):
        """
        识别图片中的文字
        在实际应用中，这里应该调用Tesseract、Google Vision API或其他OCR服务
        """
        if not os.path.exists(image_path):
            return "错误：图片文件不存在"
        
        # 模拟OCR识别结果
        # 在实际应用中，这里应该调用真实的OCR引擎
        # 例如：
        # import pytesseract
        # from PIL import Image
        # image = Image.open(image_path)
        # text = pytesseract.image_to_string(image, lang='chi_sim')
        
        # 返回模拟的识别结果（用于演示）
        return self._simulate_recognition()
    
    def _simulate_recognition(self):
        """模拟识别结果（用于演示）"""
        return """
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
    
    def parse_prescription(self, text):
        """解析处方文本"""
        prescription = {
            'patient_name': self._extract_patient_name(text),
            'patient_age': self._extract_age(text),
            'patient_gender': self._extract_gender(text),
            'date': self._extract_date(text),
            'symptoms': self._extract_symptoms(text),
            'diagnosis': self._extract_diagnosis(text),
            'formula_name': self._extract_formula_name(text),
            'herbs': self._extract_herbs(text),
            'dosage': self._extract_dosage(text),
            'usage': self._extract_usage(text),
            'doctor_name': self._extract_doctor(text),
            'hospital': self._extract_hospital(text),
            'notes': ''
        }
        
        return prescription
    
    def _extract_patient_name(self, text):
        """提取患者姓名"""
        patterns = [
            r'患者[：:]\s*(\S+)',
            r'姓名[：:]\s*(\S+)',
            r'病人[：:]\s*(\S+)',
        ]
        return self._extract_by_patterns(text, patterns) or '未知'
    
    def _extract_age(self, text):
        """提取年龄"""
        patterns = [
            r'年龄[：:]\s*(\d+)',
            r'(\d+)\s*岁',
        ]
        return self._extract_by_patterns(text, patterns) or ''
    
    def _extract_gender(self, text):
        """提取性别"""
        patterns = [
            r'性别[：:]\s*([男女])',
            r'([男女])\s*[性]?',
        ]
        return self._extract_by_patterns(text, patterns) or ''
    
    def _extract_date(self, text):
        """提取日期"""
        patterns = [
            r'日期[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日)',
            r'日期[：:]\s*(\d{4}-\d{2}-\d{2})',
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{4}-\d{2}-\d{2})',
        ]
        return self._extract_by_patterns(text, patterns) or ''
    
    def _extract_symptoms(self, text):
        """提取症状"""
        # 查找症状部分
        patterns = [
            r'症状[：:]\s*([^\n]+)',
            r'主诉[：:]\s*([^\n]+)',
            r'现病史[：:]\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        # 如果没有明确标记，尝试从文本中提取症状关键词
        found_symptoms = []
        for symptom in self.symptom_keywords:
            if symptom in text:
                found_symptoms.append(symptom)
        
        return '、'.join(found_symptoms) if found_symptoms else ''
    
    def _extract_diagnosis(self, text):
        """提取诊断"""
        patterns = [
            r'诊断[：:]\s*([^\n]+)',
            r'中医诊断[：:]\s*([^\n]+)',
            r'辨证[：:]\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return ''
    
    def _extract_formula_name(self, text):
        """提取方剂名称"""
        # 首先查找明确标记的方剂
        patterns = [
            r'方剂[：:]\s*([^\n]+)',
            r'方名[：:]\s*([^\n]+)',
            r'处方[：:]\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                formula = match.group(1).strip()
                # 清理方剂名称
                formula = re.sub(r'[加减].*$', '', formula)
                return formula
        
        # 尝试匹配常见方剂
        for formula in self.common_formulas:
            if formula in text:
                return formula
        
        return ''
    
    def _extract_herbs(self, text):
        """提取药材列表"""
        herbs = []
        
        # 查找药材和剂量的模式
        # 例如：熟地黄 24g 或 熟地黄24g
        pattern = r'([\u4e00-\u9fa5]{2,4})\s*(\d+(?:\.\d+)?)\s*[克g]'
        matches = re.findall(pattern, text)
        
        for herb_name, dosage in matches:
            # 验证是否是常见药材
            if herb_name in self.common_herbs or len(herb_name) >= 2:
                herbs.append(f"{herb_name} {dosage}g")
        
        return '，'.join(herbs) if herbs else ''
    
    def _extract_dosage(self, text):
        """提取剂量信息"""
        patterns = [
            r'剂量[：:]\s*([^\n]+)',
            r'共([\d]+)剂',
            r'([\d]+)剂',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return '1剂'
    
    def _extract_usage(self, text):
        """提取用法"""
        patterns = [
            r'用法[：:]\s*([^\n]+)',
            r'水煎服[，,]?\s*([^\n]*)',
            r'每日[：:]?\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                usage = match.group(0).strip()
                return usage
        
        return '水煎服，每日一剂'
    
    def _extract_doctor(self, text):
        """提取医生姓名"""
        patterns = [
            r'医师[：:]\s*(\S+)',
            r'医生[：:]\s*(\S+)',
            r'处方医师[：:]\s*(\S+)',
        ]
        return self._extract_by_patterns(text, patterns) or ''
    
    def _extract_hospital(self, text):
        """提取医院名称"""
        patterns = [
            r'医院[：:]\s*(\S+)',
            r'诊所[：:]\s*(\S+)',
            r'医疗机构[：:]\s*(\S+)',
        ]
        return self._extract_by_patterns(text, patterns) or ''
    
    def _extract_by_patterns(self, text, patterns):
        """使用多个模式提取信息"""
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return ''
    
    def batch_recognize(self, image_paths):
        """批量识别多张图片"""
        results = []
        for path in image_paths:
            text = self.recognize(path)
            prescription = self.parse_prescription(text)
            results.append(prescription)
        return results
