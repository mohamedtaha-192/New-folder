# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Union
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QMenuBar, 
                           QMenu, QAction, QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ui.widgets.dashboard_widget import DashboardWidget
from ui.widgets.accounting_widget import AccountingWidget
from ui.widgets.inventory_widget import InventoryWidget
from ui.widgets.hr_widget import HRWidget
from ui.widgets.reports_widget import ReportsWidget
from ui.widgets.contacts_widget import ContactsWidget
from database.db_config import init_database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        # إعداد النافذة الرئيسية
        self.setWindowTitle('نظام المحاسبة المتكامل')
        self.setGeometry(100, 100, 1200, 800)
        self.setLayoutDirection(Qt.RightToLeft)
        
        # إنشاء شريط القوائم
        self.create_menu_bar()
        
        # إنشاء شريط الحالة
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('جاهز')
        
        # إنشاء مجموعة التبويبات
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # إضافة لوحة المعلومات
        self.dashboard = DashboardWidget()
        self.tab_widget.addTab(self.dashboard, 'لوحة المعلومات')
        
        # إضافة تبويب المحاسبة
        self.accounting = AccountingWidget()
        self.tab_widget.addTab(self.accounting, 'المحاسبة')
        
        # إضافة تبويب المخزون
        self.inventory = InventoryWidget()
        self.tab_widget.addTab(self.inventory, 'المخزون')
        
        # إضافة تبويب الموارد البشرية
        self.hr = HRWidget()
        self.tab_widget.addTab(self.hr, 'الموارد البشرية')
        
        # إضافة تبويب التقارير
        self.reports = ReportsWidget()
        self.tab_widget.addTab(self.reports, 'التقارير')

        # إضافة تبويب جهات الاتصال
        self.contacts = ContactsWidget()
        self.tab_widget.addTab(self.contacts, 'جهات الاتصال')
        
        self.show()
    
    def create_menu_bar(self):
        """إنشاء شريط القوائم"""
        menubar = self.menuBar()
        
        # قائمة ملف
        file_menu = menubar.addMenu('ملف')
        
        # إضافة عناصر قائمة ملف
        new_action = QAction('جديد', self)
        new_action.setShortcut('Ctrl+N')
        file_menu.addAction(new_action)
        
        save_action = QAction('حفظ', self)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('خروج', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # قائمة تحرير
        edit_menu = menubar.addMenu('تحرير')
        
        # قائمة عرض
        view_menu = menubar.addMenu('عرض')
        
        # قائمة أدوات
        tools_menu = menubar.addMenu('أدوات')
        
        # قائمة مساعدة
        help_menu = menubar.addMenu('مساعدة')
        about_action = QAction('حول البرنامج', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

def main():
    """تشغيل البرنامج"""
    # تهيئة قاعدة البيانات
    init_database()
    
    # إنشاء التطبيق
    app = QApplication(sys.argv)
    
    # تعيين نمط التطبيق
    app.setStyle('Fusion')
    
    # تعيين اتجاه الكتابة من اليمين إلى اليسار
    app.setLayoutDirection(Qt.RightToLeft)
    
    # إنشاء النافذة الرئيسية
    window = MainWindow()
    
    # تشغيل التطبيق
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    main()
