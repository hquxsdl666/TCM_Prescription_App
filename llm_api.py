"""
大模型API模块
接入大模型进行中医诊断和开方
"""

import os
import json
import sqlite3
from database import DatabaseManager


class LLMAPI:
    """大模型API接口"""
    
    def __init__(self, api_key=None, api_base=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', '')
        self.api_base = api_base or os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        self.db = DatabaseManager()
        
        # 中医知识库提示词
        self.tcm_system_prompt = """你是一位经验丰富的中医专家，精通中医理论和临床实践。
你需要根据患者的症状进行中医辨证论治，给出诊断结果和处方建议。

请按照以下格式输出：

【辨证】
分析患者的症状，给出中医辨证结果。

【诊断】
给出明确的中医诊断病名。

【治法】
说明治疗原则和方法。

【处方】
给出具体的方剂名称和药物组成，包括剂量。

【用法】
说明煎服方法和注意事项。

【医嘱】
给出生活调摄建议。
"""
    
    def diagnose(self, symptoms, patient_info=None):
        """
        AI诊断开方
        
        Args:
            symptoms: 症状描述
            patient_info: 患者信息（姓名、年龄等）
        
        Returns:
            诊断结果字符串
        """
        # 构建提示词
        prompt = self._build_diagnosis_prompt(symptoms, patient_info)
        
        # 调用大模型API
        # 在实际应用中，这里应该调用真实的API
        # 例如OpenAI API、文心一言、通义千问等
        
        # 返回模拟的诊断结果（用于演示）
        return self._simulate_diagnosis(symptoms, patient_info)
    
    def _build_diagnosis_prompt(self, symptoms, patient_info):
        """构建诊断提示词"""
        prompt = f"【患者信息】\n"
        
        if patient_info:
            if patient_info.get('name'):
                prompt += f"姓名：{patient_info['name']}\n"
            if patient_info.get('age'):
                prompt += f"年龄：{patient_info['age']}\n"
            if patient_info.get('gender'):
                prompt += f"性别：{patient_info['gender']}\n"
        
        prompt += f"\n【症状】\n{symptoms}\n"
        prompt += f"\n请根据以上信息进行中医辨证论治。"
        
        return prompt
    
    def _simulate_diagnosis(self, symptoms, patient_info):
        """模拟诊断结果（用于演示）"""
        
        # 根据症状关键词匹配简单的诊断逻辑
        symptoms_lower = symptoms.lower()
        
        # 分析症状
        has_headache = '头痛' in symptoms or '头疼' in symptoms
        has_dizziness = '眩晕' in symptoms or '头晕' in symptoms
        has_insomnia = '失眠' in symptoms or '多梦' in symptoms
        has_fever = '发热' in symptoms or '发烧' in symptoms
        has_cough = '咳嗽' in symptoms or '咳痰' in symptoms
        has_fatigue = '乏力' in symptoms or '疲倦' in symptoms or '神疲' in symptoms
        has_pale = '面色苍白' in symptoms or '面色萎黄' in symptoms
        has_red = '面红' in symptoms or '面色潮红' in symptoms
        has_dry = '口干' in symptoms or '口渴' in symptoms
        has_sweat = '汗出' in symptoms or '盗汗' in symptoms
        
        # 肾阴虚肝阳上亢证
        if has_headache and has_dizziness and has_insomnia:
            return """【辨证】
患者头痛、眩晕、失眠多梦，结合腰膝酸软，舌红少苔，脉细数，此为肾阴虚，肝阳上亢之证。
肾阴亏虚，水不涵木，肝阳上亢，故见头痛眩晕；阴虚火旺，心神不宁，故见失眠多梦；
腰为肾之府，肾虚则腰膝酸软；舌红少苔，脉细数，均为阴虚之象。

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
- 泽泻 9g（利水渗湿，泄热）
- 茯苓 9g（利水渗湿，健脾宁心）
- 丹皮 9g（清热凉血，活血化瘀）
- 枸杞子 15g（滋补肝肾，益精明目）
- 菊花 10g（疏散风热，平肝明目）
- 钩藤 15g（清热平肝，息风定惊）
- 石决明 30g（平肝潜阳，清肝明目）

【用法】
水煎服，每日一剂，分早晚两次温服。
共7剂。

【医嘱】
1. 注意休息，避免劳累和熬夜
2. 保持心情舒畅，避免情绪激动
3. 饮食宜清淡，少食辛辣刺激性食物
4. 忌烟酒
5. 适当进行体育锻炼，如太极拳、八段锦等
6. 一周后复诊，如有不适随时就诊"""
        
        # 风热感冒证
        elif has_fever and has_cough and has_headache:
            return """【辨证】
患者发热、咳嗽、头痛，此为风热犯表，肺失宣降之证。
风热之邪侵袭肌表，正邪相争，故见发热；风热上扰清空，故见头痛；
肺主皮毛，风热犯肺，肺失宣降，故见咳嗽；舌红苔薄黄，脉浮数，均为风热之象。

【诊断】
风热感冒

【治法】
辛凉解表，宣肺止咳

【处方】
银翘散加减

药物组成：
- 金银花 15g（清热解毒，疏散风热）
- 连翘 15g（清热解毒，消肿散结）
- 薄荷 6g（疏散风热，清利头目）
- 荆芥 10g（解表散风，透疹消疮）
- 淡豆豉 10g（解表，除烦）
- 牛蒡子 10g（疏散风热，宣肺透疹）
- 桔梗 10g（宣肺，利咽，祛痰）
- 甘草 6g（补脾益气，清热解毒）
- 竹叶 10g（清热除烦，生津利尿）
- 芦根 15g（清热生津，除烦止呕）
- 杏仁 10g（降气止咳平喘，润肠通便）
- 前胡 10g（降气化痰，散风清热）

【用法】
水煎服，每日一剂，分早晚两次温服。
共3剂。

【医嘱】
1. 注意休息，多饮水
2. 保持室内空气流通
3. 饮食宜清淡易消化
4. 忌食辛辣油腻食物
5. 注意保暖，避免再次受凉
6. 如症状加重或持续不退，请及时就诊"""
        
        # 气血两虚证
        elif has_fatigue and has_pale and has_dizziness:
            return """【辨证】
患者神疲乏力、面色苍白、头晕，此为气血两虚之证。
气虚则脏腑功能减退，故见神疲乏力；血虚不能上荣于面，故见面色苍白；
血虚脑髓失养，故见头晕；舌淡苔白，脉细弱，均为气血两虚之象。

【诊断】
气血两虚证

【治法】
益气养血

【处方】
八珍汤加减

药物组成：
- 人参 10g（大补元气，复脉固脱）
- 白术 10g（健脾益气，燥湿利水）
- 茯苓 10g（利水渗湿，健脾宁心）
- 甘草 6g（补脾益气，清热解毒）
- 当归 10g（补血活血，调经止痛）
- 川芎 6g（活血行气，祛风止痛）
- 白芍 10g（养血调经，敛阴止汗）
- 熟地黄 15g（滋阴补肾，填精益髓）
- 黄芪 15g（补气升阳，固表止汗）
- 肉桂 3g（补火助阳，引火归元）

【用法】
水煎服，每日一剂，分早晚两次温服。
共10剂。

【医嘱】
1. 注意休息，避免过度劳累
2. 加强营养，多食血肉有情之品
3. 可适当食用红枣、桂圆、山药等补益食物
4. 保持心情舒畅
5. 适当进行轻度体育锻炼
6. 十天后复诊"""
        
        # 默认诊断
        else:
            return """【辨证】
根据患者所述症状，需要进一步详细问诊和四诊合参，以明确辨证。
建议患者到正规医院进行详细检查，以便准确诊断和治疗。

【诊断】
待进一步检查明确

【治法】
暂不明确，待辨证后确定

【建议】
1. 建议到正规医院中医科就诊
2. 详细告知医生所有症状和病史
3. 配合医生进行必要的检查
4. 不要自行用药，以免延误病情

【注意事项】
1. 注意休息，避免劳累
2. 饮食宜清淡
3. 保持心情舒畅
4. 如有不适及时就医"""
    
    def learn_from_database(self):
        """
        从本地数据库学习方剂知识
        返回知识库文本
        """
        # 获取所有方剂数据
        formulas = self._get_all_formulas()
        
        # 获取所有处方数据
        prescriptions = self.db.get_all_prescriptions()
        
        # 构建知识库
        knowledge = []
        
        # 添加方剂知识
        knowledge.append("【方剂知识库】")
        for formula in formulas:
            knowledge.append(f"\n方剂：{formula.get('name', '')}")
            knowledge.append(f"组成：{formula.get('composition', '')}")
            knowledge.append(f"功效：{formula.get('functions', '')}")
            knowledge.append(f"主治：{formula.get('indications', '')}")
        
        # 添加处方案例
        knowledge.append("\n\n【临床案例】")
        for i, prescription in enumerate(prescriptions[:20], 1):  # 只取前20个案例
            knowledge.append(f"\n案例{i}：")
            knowledge.append(f"症状：{prescription.get('symptoms', '')}")
            knowledge.append(f"诊断：{prescription.get('diagnosis', '')}")
            knowledge.append(f"方剂：{prescription.get('formula_name', '')}")
            knowledge.append(f"用药：{prescription.get('herbs', '')}")
        
        return '\n'.join(knowledge)
    
    def _get_all_formulas(self):
        """获取所有方剂数据"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM formulas')
        columns = [description[0] for description in cursor.description]
        
        formulas = []
        for row in cursor.fetchall():
            formulas.append(dict(zip(columns, row)))
        
        conn.close()
        return formulas
    
    def parse_diagnosis_result(self, result_text):
        """解析诊断结果为结构化数据"""
        prescription = {
            'formula_name': '',
            'diagnosis': '',
            'symptoms': '',
            'herbs': '',
            'usage': '',
            'notes': ''
        }
        
        # 提取方剂名称
        if '【处方】' in result_text:
            lines = result_text.split('【处方】')[1].split('【')[0].strip().split('\n')
            for line in lines:
                if '汤' in line or '丸' in line or '散' in line:
                    prescription['formula_name'] = line.strip()
                    break
        
        # 提取诊断
        if '【诊断】' in result_text:
            diagnosis = result_text.split('【诊断】')[1].split('【')[0].strip()
            prescription['diagnosis'] = diagnosis
        
        # 提取症状
        if '【辨证】' in result_text:
            symptoms = result_text.split('【辨证】')[1].split('【')[0].strip()
            prescription['symptoms'] = symptoms[:200]  # 限制长度
        
        # 提取药物
        herbs = []
        if '药物组成：' in result_text:
            herbs_section = result_text.split('药物组成：')[1].split('【')[0]
            for line in herbs_section.split('\n'):
                line = line.strip()
                if line and ('g' in line or '克' in line):
                    # 提取药材和剂量
                    herbs.append(line.lstrip('- ').strip())
        
        prescription['herbs'] = '，'.join(herbs)
        
        # 提取用法
        if '【用法】' in result_text:
            usage = result_text.split('【用法】')[1].split('【')[0].strip()
            prescription['usage'] = usage
        
        # 提取医嘱作为备注
        if '【医嘱】' in result_text:
            notes = result_text.split('【医嘱】')[1].strip()
            prescription['notes'] = notes[:500]  # 限制长度
        
        return prescription
    
    def set_api_key(self, api_key):
        """设置API密钥"""
        self.api_key = api_key
    
    def set_api_base(self, api_base):
        """设置API基础URL"""
        self.api_base = api_base
    
    def call_openai_api(self, messages, model='gpt-4'):
        """
        调用OpenAI API
        
        Args:
            messages: 消息列表
            model: 模型名称
        
        Returns:
            API响应
        """
        try:
            import openai
            
            openai.api_key = self.api_key
            openai.api_base = self.api_base
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"API调用失败：{str(e)}"
    
    def call_local_model(self, prompt, model_path=None):
        """
        调用本地部署的大模型
        
        Args:
            prompt: 提示词
            model_path: 模型路径
        
        Returns:
            模型响应
        """
        # 这里可以实现调用本地模型的逻辑
        # 例如使用transformers库加载本地模型
        
        # 返回模拟响应
        return self._simulate_diagnosis(prompt, {})
