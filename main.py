"""
中药手写处方识别整理软件
TCM Prescription Recognition and Management App

功能：
1. 识别手写处方并整理为Excel
2. 方剂数据库存储和可视化统计
3. 接入大模型API进行中医诊断开方剂
"""

import os
import json
import sqlite3
import datetime
from pathlib import Path

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.camera import Camera
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.utils import platform

# 数据库管理
from database import DatabaseManager
# OCR识别
from ocr_engine import OCREngine
# Excel导出
from excel_export import ExcelExporter
# 大模型API
from llm_api import LLMAPI
# 统计分析
from statistics_manager import StatisticsManager

# 设置窗口大小（用于桌面测试）
Window.size = (400, 700)


class BaseScreen(Screen):
    """基础屏幕类"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.ocr = OCREngine()
        self.excel = ExcelExporter()
        self.llm = LLMAPI()
        self.stats = StatisticsManager()


class HomeScreen(BaseScreen):
    """主屏幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        with layout.canvas.before:
            Color(0.2, 0.6, 0.4, 1)  # 中医绿色
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        title = Label(
            text='中药处方识别整理系统',
            font_size='28sp',
            size_hint_y=0.15,
            color=(1, 1, 1, 1),
            bold=True
        )
        layout.add_widget(title)
        
        subtitle = Label(
            text='Traditional Chinese Medicine Prescription Manager',
            font_size='14sp',
            size_hint_y=0.05,
            color=(0.9, 0.9, 0.9, 1)
        )
        layout.add_widget(subtitle)
        
        # 功能按钮区域
        btn_layout = GridLayout(cols=1, spacing=15, padding=20, size_hint_y=0.6)
        
        btn_scan = Button(
            text='📷 扫描处方',
            font_size='18sp',
            size_hint_y=0.25,
            background_color=(0.3, 0.7, 0.5, 1),
            on_press=lambda x: self.manager.current = 'scan'
        )
        btn_layout.add_widget(btn_scan)
        
        btn_history = Button(
            text='📋 处方记录',
            font_size='18sp',
            size_hint_y=0.25,
            background_color=(0.3, 0.7, 0.5, 1),
            on_press=lambda x: self.manager.current = 'history'
        )
        btn_layout.add_widget(btn_history)
        
        btn_stats = Button(
            text='📊 统计分析',
            font_size='18sp',
            size_hint_y=0.25,
            background_color=(0.3, 0.7, 0.5, 1),
            on_press=lambda x: self.manager.current = 'statistics'
        )
        btn_layout.add_widget(btn_stats)
        
        btn_diagnosis = Button(
            text='🤖 AI诊断开方',
            font_size='18sp',
            size_hint_y=0.25,
            background_color=(0.3, 0.7, 0.5, 1),
            on_press=lambda x: self.manager.current = 'diagnosis'
        )
        btn_layout.add_widget(btn_diagnosis)
        
        layout.add_widget(btn_layout)
        
        # 底部信息
        footer = Label(
            text='智能中医辅助系统 v1.0',
            font_size='12sp',
            size_hint_y=0.1,
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class ScanScreen(BaseScreen):
    """扫描处方屏幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_path = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            on_press=lambda x: self.manager.current = 'home'
        )
        header.add_widget(back_btn)
        
        title = Label(
            text='处方扫描识别',
            font_size='20sp',
            size_hint_x=0.6
        )
        header.add_widget(title)
        
        spacer = Label(size_hint_x=0.2)
        header.add_widget(spacer)
        
        layout.add_widget(header)
        
        # 图像显示区域
        self.image_widget = Image(
            source='',
            size_hint_y=0.35,
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.image_widget)
        
        # 识别结果区域
        result_label = Label(
            text='识别结果：',
            font_size='14sp',
            size_hint_y=0.05,
            halign='left',
            text_size=(None, None)
        )
        layout.add_widget(result_label)
        
        self.result_input = TextInput(
            multiline=True,
            size_hint_y=0.25,
            font_size='14sp',
            hint_text='识别结果将显示在这里...'
        )
        layout.add_widget(self.result_input)
        
        # 按钮区域
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        
        camera_btn = Button(
            text='📷 拍照',
            font_size='16sp',
            background_color=(0.3, 0.6, 0.9, 1),
            on_press=self.take_photo
        )
        btn_layout.add_widget(camera_btn)
        
        gallery_btn = Button(
            text='🖼️ 相册',
            font_size='16sp',
            background_color=(0.3, 0.6, 0.9, 1),
            on_press=self.open_gallery
        )
        btn_layout.add_widget(gallery_btn)
        
        recognize_btn = Button(
            text='🔍 识别',
            font_size='16sp',
            background_color=(0.9, 0.6, 0.3, 1),
            on_press=self.recognize_text
        )
        btn_layout.add_widget(recognize_btn)
        
        save_btn = Button(
            text='💾 保存',
            font_size='16sp',
            background_color=(0.3, 0.8, 0.4, 1),
            on_press=self.save_prescription
        )
        btn_layout.add_widget(save_btn)
        
        layout.add_widget(btn_layout)
        
        # 批量处理按钮
        batch_btn = Button(
            text='📁 批量处理处方',
            font_size='16sp',
            size_hint_y=0.08,
            background_color=(0.6, 0.4, 0.8, 1),
            on_press=self.batch_process
        )
        layout.add_widget(batch_btn)
        
        self.add_widget(layout)
    
    def take_photo(self, instance):
        """拍照功能"""
        # 在实际设备上使用相机API
        # 这里模拟选择一张图片
        self.show_popup('提示', '相机功能在移动设备上可用')
    
    def open_gallery(self, instance):
        """打开相册"""
        # 创建文件选择器
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg']
        )
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=0.1)
        select_btn = Button(text='选择')
        cancel_btn = Button(text='取消')
        
        popup = Popup(title='选择图片', content=content, size_hint=(0.9, 0.9))
        
        def on_select(instance):
            if filechooser.selection:
                self.image_path = filechooser.selection[0]
                self.image_widget.source = self.image_path
                popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def recognize_text(self, instance):
        """识别文字"""
        if not self.image_path:
            self.show_popup('错误', '请先选择图片')
            return
        
        # 调用OCR引擎
        result = self.ocr.recognize(self.image_path)
        self.result_input.text = result
    
    def save_prescription(self, instance):
        """保存处方"""
        text = self.result_input.text
        if not text:
            self.show_popup('错误', '没有识别结果可保存')
            return
        
        # 解析处方信息
        prescription = self.ocr.parse_prescription(text)
        
        # 保存到数据库
        self.db.save_prescription(prescription)
        
        self.show_popup('成功', '处方已保存到数据库')
    
    def batch_process(self, instance):
        """批量处理"""
        self.manager.current = 'batch'
    
    def show_popup(self, title, message):
        """显示弹窗"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class BatchProcessScreen(BaseScreen):
    """批量处理屏幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_files = []
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            on_press=lambda x: self.manager.current = 'scan'
        )
        header.add_widget(back_btn)
        
        title = Label(
            text='批量处理处方',
            font_size='20sp',
            size_hint_x=0.6
        )
        header.add_widget(title)
        
        spacer = Label(size_hint_x=0.2)
        header.add_widget(spacer)
        
        layout.add_widget(header)
        
        # 文件列表
        self.file_label = Label(
            text='未选择文件',
            font_size='14sp',
            size_hint_y=0.1
        )
        layout.add_widget(self.file_label)
        
        # 进度显示
        self.progress_label = Label(
            text='进度: 0/0',
            font_size='14sp',
            size_hint_y=0.1
        )
        layout.add_widget(self.progress_label)
        
        # 结果显示
        self.result_text = TextInput(
            multiline=True,
            readonly=True,
            size_hint_y=0.4,
            hint_text='处理结果...'
        )
        layout.add_widget(self.result_text)
        
        # 按钮区域
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        select_btn = Button(
            text='📁 选择文件',
            font_size='16sp',
            on_press=self.select_files
        )
        btn_layout.add_widget(select_btn)
        
        process_btn = Button(
            text='▶️ 开始处理',
            font_size='16sp',
            background_color=(0.3, 0.7, 0.5, 1),
            on_press=self.start_processing
        )
        btn_layout.add_widget(process_btn)
        
        export_btn = Button(
            text='📊 导出Excel',
            font_size='16sp',
            background_color=(0.9, 0.6, 0.3, 1),
            on_press=self.export_excel
        )
        btn_layout.add_widget(export_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def select_files(self, instance):
        """选择多个文件"""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg'],
            multiselect=True
        )
        content.add_widget(filechooser)
        
        btn_layout = BoxLayout(size_hint_y=0.1)
        select_btn = Button(text='选择')
        cancel_btn = Button(text='取消')
        
        popup = Popup(title='选择图片（可多选）', content=content, size_hint=(0.9, 0.9))
        
        def on_select(instance):
            if filechooser.selection:
                self.selected_files = filechooser.selection
                self.file_label.text = f'已选择 {len(self.selected_files)} 个文件'
                popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def start_processing(self, instance):
        """开始批量处理"""
        if not self.selected_files:
            self.show_popup('错误', '请先选择文件')
            return
        
        results = []
        total = len(self.selected_files)
        
        for i, file_path in enumerate(self.selected_files):
            self.progress_label.text = f'进度: {i+1}/{total}'
            
            # 识别文字
            text = self.ocr.recognize(file_path)
            
            # 解析处方
            prescription = self.ocr.parse_prescription(text)
            
            # 保存到数据库
            self.db.save_prescription(prescription)
            
            results.append(prescription)
        
        # 显示结果
        self.result_text.text = json.dumps(results, ensure_ascii=False, indent=2)
        self.show_popup('完成', f'已处理 {total} 个处方')
    
    def export_excel(self, instance):
        """导出Excel"""
        if not self.selected_files:
            self.show_popup('错误', '没有可导出的数据')
            return
        
        # 获取所有处方数据
        prescriptions = self.db.get_all_prescriptions()
        
        # 导出为Excel
        output_path = os.path.join(os.path.expanduser('~'), 'prescriptions.xlsx')
        self.excel.export(prescriptions, output_path)
        
        self.show_popup('成功', f'Excel已保存到: {output_path}')
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class HistoryScreen(BaseScreen):
    """历史记录屏幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            on_press=lambda x: self.manager.current = 'home'
        )
        header.add_widget(back_btn)
        
        title = Label(
            text='处方记录',
            font_size='20sp',
            size_hint_x=0.6
        )
        header.add_widget(title)
        
        refresh_btn = Button(
            text='🔄',
            size_hint_x=0.2,
            on_press=self.load_records
        )
        header.add_widget(refresh_btn)
        
        layout.add_widget(header)
        
        # 搜索栏
        search_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        self.search_input = TextInput(
            hint_text='搜索患者姓名或方剂...',
            size_hint_x=0.7,
            font_size='14sp'
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(
            text='🔍 搜索',
            size_hint_x=0.3,
            on_press=self.search_records
        )
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # 记录列表
        self.records_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.records_layout.bind(minimum_height=self.records_layout.setter('height'))
        
        scroll = ScrollView(size_hint_y=0.74)
        scroll.add_widget(self.records_layout)
        layout.add_widget(scroll)
        
        # 底部按钮
        footer = BoxLayout(size_hint_y=0.08, spacing=10)
        
        export_btn = Button(
            text='📊 导出Excel',
            on_press=self.export_to_excel
        )
        footer.add_widget(export_btn)
        
        delete_btn = Button(
            text='🗑️ 清空',
            background_color=(0.9, 0.3, 0.3, 1),
            on_press=self.clear_all
        )
        footer.add_widget(delete_btn)
        
        layout.add_widget(footer)
        
        self.add_widget(layout)
        
        # 加载记录
        Clock.schedule_once(lambda dt: self.load_records(None), 0.5)
    
    def load_records(self, instance):
        """加载记录"""
        self.records_layout.clear_widgets()
        
        records = self.db.get_all_prescriptions()
        
        if not records:
            label = Label(
                text='暂无记录',
                size_hint_y=None,
                height=50
            )
            self.records_layout.add_widget(label)
            return
        
        for record in records:
            item = self.create_record_item(record)
            self.records_layout.add_widget(item)
    
    def create_record_item(self, record):
        """创建记录项"""
        item = BoxLayout(size_hint_y=None, height=80, padding=5)
        
        with item.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            rect = Rectangle(size=item.size, pos=item.pos)
            item.bind(size=lambda obj, val: setattr(rect, 'size', val))
            item.bind(pos=lambda obj, val: setattr(rect, 'pos', val))
        
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        
        name_label = Label(
            text=f"患者: {record.get('patient_name', '未知')}",
            font_size='14sp',
            halign='left',
            text_size=(None, None)
        )
        info_layout.add_widget(name_label)
        
        formula_label = Label(
            text=f"方剂: {record.get('formula_name', '未命名')}",
            font_size='12sp',
            halign='left',
            text_size=(None, None),
            color=(0.5, 0.5, 0.5, 1)
        )
        info_layout.add_widget(formula_label)
        
        date_label = Label(
            text=f"日期: {record.get('date', '未知')}",
            font_size='11sp',
            halign='left',
            text_size=(None, None),
            color=(0.6, 0.6, 0.6, 1)
        )
        info_layout.add_widget(date_label)
        
        item.add_widget(info_layout)
        
        # 操作按钮
        btn_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=2)
        
        view_btn = Button(
            text='查看',
            font_size='12sp',
            on_press=lambda x, r=record: self.view_record(r)
        )
        btn_layout.add_widget(view_btn)
        
        delete_btn = Button(
            text='删除',
            font_size='12sp',
            background_color=(0.9, 0.4, 0.4, 1),
            on_press=lambda x, r=record: self.delete_record(r)
        )
        btn_layout.add_widget(delete_btn)
        
        item.add_widget(btn_layout)
        
        return item
    
    def search_records(self, instance):
        """搜索记录"""
        keyword = self.search_input.text
        if not keyword:
            self.load_records(None)
            return
        
        self.records_layout.clear_widgets()
        records = self.db.search_prescriptions(keyword)
        
        for record in records:
            item = self.create_record_item(record)
            self.records_layout.add_widget(item)
    
    def view_record(self, record):
        """查看记录详情"""
        content = BoxLayout(orientation='vertical', padding=10)
        
        details = TextInput(
            text=json.dumps(record, ensure_ascii=False, indent=2),
            multiline=True,
            readonly=True,
            font_size='12sp'
        )
        content.add_widget(details)
        
        close_btn = Button(
            text='关闭',
            size_hint_y=0.1,
            on_press=lambda x: popup.dismiss()
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='处方详情',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def delete_record(self, record):
        """删除记录"""
        self.db.delete_prescription(record.get('id'))
        self.load_records(None)
    
    def export_to_excel(self, instance):
        """导出到Excel"""
        records = self.db.get_all_prescriptions()
        if not records:
            self.show_popup('提示', '没有可导出的记录')
            return
        
        output_path = os.path.join(os.path.expanduser('~'), 'prescriptions_export.xlsx')
        self.excel.export(records, output_path)
        self.show_popup('成功', f'已导出到: {output_path}')
    
    def clear_all(self, instance):
        """清空所有记录"""
        self.db.clear_all()
        self.load_records(None)
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class StatisticsScreen(BaseScreen):
    """统计分析屏幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            on_press=lambda x: self.manager.current = 'home'
        )
        header.add_widget(back_btn)
        
        title = Label(
            text='统计分析',
            font_size='20sp',
            size_hint_x=0.6
        )
        header.add_widget(title)
        
        refresh_btn = Button(
            text='🔄',
            size_hint_x=0.2,
            on_press=self.load_statistics
        )
        header.add_widget(refresh_btn)
        
        layout.add_widget(header)
        
        # 统计概览
        self.overview_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.25)
        
        self.total_label = Label(
            text='总处方数: 0',
            font_size='16sp'
        )
        self.overview_layout.add_widget(self.total_label)
        
        self.patients_label = Label(
            text='患者数: 0',
            font_size='16sp'
        )
        self.overview_layout.add_widget(self.patients_label)
        
        self.formulas_label = Label(
            text='方剂种类: 0',
            font_size='16sp'
        )
        self.overview_layout.add_widget(self.formulas_label)
        
        self.monthly_label = Label(
            text='本月新增: 0',
            font_size='16sp'
        )
        self.overview_layout.add_widget(self.monthly_label)
        
        layout.add_widget(self.overview_layout)
        
        # 详细统计
        self.stats_text = TextInput(
            multiline=True,
            readonly=True,
            size_hint_y=0.47,
            font_size='12sp',
            hint_text='统计详情...'
        )
        layout.add_widget(self.stats_text)
        
        # 图表按钮
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        herb_btn = Button(
            text='🌿 药材使用统计',
            on_press=self.show_herb_stats
        )
        btn_layout.add_widget(herb_btn)
        
        formula_btn = Button(
            text='📋 方剂使用统计',
            on_press=self.show_formula_stats
        )
        btn_layout.add_widget(formula_btn)
        
        trend_btn = Button(
            text='📈 趋势分析',
            on_press=self.show_trend_stats
        )
        btn_layout.add_widget(trend_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
        
        # 加载统计
        Clock.schedule_once(lambda dt: self.load_statistics(None), 0.5)
    
    def load_statistics(self, instance):
        """加载统计数据"""
        stats = self.stats.get_overview()
        
        self.total_label.text = f"总处方数: {stats.get('total', 0)}"
        self.patients_label.text = f"患者数: {stats.get('patients', 0)}"
        self.formulas_label.text = f"方剂种类: {stats.get('formulas', 0)}"
        self.monthly_label.text = f"本月新增: {stats.get('monthly', 0)}"
        
        # 详细统计
        details = self.stats.get_detailed_stats()
        self.stats_text.text = json.dumps(details, ensure_ascii=False, indent=2)
    
    def show_herb_stats(self, instance):
        """显示药材统计"""
        stats = self.stats.get_herb_statistics()
        self.show_stats_popup('药材使用统计', stats)
    
    def show_formula_stats(self, instance):
        """显示方剂统计"""
        stats = self.stats.get_formula_statistics()
        self.show_stats_popup('方剂使用统计', stats)
    
    def show_trend_stats(self, instance):
        """显示趋势统计"""
        stats = self.stats.get_trend_statistics()
        self.show_stats_popup('趋势分析', stats)
    
    def show_stats_popup(self, title, stats):
        """显示统计弹窗"""
        content = BoxLayout(orientation='vertical', padding=10)
        
        text = TextInput(
            text=json.dumps(stats, ensure_ascii=False, indent=2),
            multiline=True,
            readonly=True,
            font_size='12sp'
        )
        content.add_widget(text)
        
        close_btn = Button(
            text='关闭',
            size_hint_y=0.1,
            on_press=lambda x: popup.dismiss()
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()


class DiagnosisScreen(BaseScreen):
    """AI诊断屏幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题栏
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(
            text='← 返回',
            size_hint_x=0.2,
            on_press=lambda x: self.manager.current = 'home'
        )
        header.add_widget(back_btn)
        
        title = Label(
            text='AI中医诊断',
            font_size='20sp',
            size_hint_x=0.6
        )
        header.add_widget(title)
        
        spacer = Label(size_hint_x=0.2)
        header.add_widget(spacer)
        
        layout.add_widget(header)
        
        # 症状输入
        symptom_label = Label(
            text='请输入症状：',
            font_size='14sp',
            size_hint_y=0.05,
            halign='left'
        )
        layout.add_widget(symptom_label)
        
        self.symptom_input = TextInput(
            multiline=True,
            size_hint_y=0.25,
            font_size='14sp',
            hint_text='例如：头痛、发热、咳嗽、舌苔白...'
        )
        layout.add_widget(self.symptom_input)
        
        # 患者信息
        info_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.12)
        
        info_layout.add_widget(Label(text='患者姓名:', font_size='14sp'))
        self.name_input = TextInput(font_size='14sp', hint_text='姓名')
        info_layout.add_widget(self.name_input)
        
        info_layout.add_widget(Label(text='年龄:', font_size='14sp'))
        self.age_input = TextInput(font_size='14sp', hint_text='年龄', input_filter='int')
        info_layout.add_widget(self.age_input)
        
        layout.add_widget(info_layout)
        
        # 诊断按钮
        diagnose_btn = Button(
            text='🤖 AI诊断开方',
            font_size='18sp',
            size_hint_y=0.1,
            background_color=(0.3, 0.7, 0.5, 1),
            on_press=self.ai_diagnosis
        )
        layout.add_widget(diagnose_btn)
        
        # 诊断结果
        result_label = Label(
            text='诊断结果：',
            font_size='14sp',
            size_hint_y=0.05,
            halign='left'
        )
        layout.add_widget(result_label)
        
        self.result_input = TextInput(
            multiline=True,
            readonly=True,
            size_hint_y=0.25,
            font_size='13sp',
            hint_text='AI诊断结果将显示在这里...'
        )
        layout.add_widget(self.result_input)
        
        # 保存按钮
        save_btn = Button(
            text='💾 保存处方',
            font_size='16sp',
            size_hint_y=0.08,
            background_color=(0.3, 0.6, 0.9, 1),
            on_press=self.save_diagnosis
        )
        layout.add_widget(save_btn)
        
        self.add_widget(layout)
    
    def ai_diagnosis(self, instance):
        """AI诊断"""
        symptoms = self.symptom_input.text
        if not symptoms:
            self.show_popup('错误', '请输入症状')
            return
        
        # 获取患者信息
        patient_info = {
            'name': self.name_input.text or '未知',
            'age': self.age_input.text or '未知'
        }
        
        # 调用大模型API
        result = self.llm.diagnose(symptoms, patient_info)
        
        self.result_input.text = result
    
    def save_diagnosis(self, instance):
        """保存诊断结果"""
        result = self.result_input.text
        if not result:
            self.show_popup('错误', '没有可保存的诊断结果')
            return
        
        # 解析诊断结果
        prescription = self.llm.parse_diagnosis_result(result)
        prescription['patient_name'] = self.name_input.text or '未知'
        prescription['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 保存到数据库
        self.db.save_prescription(prescription)
        
        self.show_popup('成功', '诊断处方已保存')
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class TCMPrescriptionApp(App):
    """中药处方识别整理应用"""
    
    def build(self):
        # 加载KV文件
        self.load_kv('tcmapp.kv')
        
        # 创建数据库
        db = DatabaseManager()
        db.init_database()
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加各个屏幕
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ScanScreen(name='scan'))
        sm.add_widget(BatchProcessScreen(name='batch'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(StatisticsScreen(name='statistics'))
        sm.add_widget(DiagnosisScreen(name='diagnosis'))
        
        return sm


if __name__ == '__main__':
    TCMPrescriptionApp().run()
