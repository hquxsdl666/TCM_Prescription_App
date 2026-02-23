#!/usr/bin/env python3
"""
中药处方识别整理软件 - 启动脚本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import TCMPrescriptionApp

if __name__ == '__main__':
    print("=" * 60)
    print("中药处方识别整理软件")
    print("Traditional Chinese Medicine Prescription Manager")
    print("=" * 60)
    print("\n启动应用中...")
    
    try:
        TCMPrescriptionApp().run()
    except KeyboardInterrupt:
        print("\n\n应用已退出")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
