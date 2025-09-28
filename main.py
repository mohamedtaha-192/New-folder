# -*- coding: utf-8 -*-
import os
import sys
import traceback

# إعداد مسار الإضافات لـ PyQt5
if getattr(sys, 'frozen', False):
    # تشغيل كملف تنفيذي
    application_path = sys._MEIPASS
else:
    # تشغيل كسكريبت
    application_path = os.path.dirname(os.path.abspath(__file__))

# إعداد مسارات Qt
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(application_path, 'PyQt5', 'Qt', 'plugins')
os.environ['QT_DEBUG_PLUGINS'] = '1'  # لطباعة معلومات تصحيح الأخطاء

# تعيين المسار الحالي كمسار للبحث عن الحزم
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# تكوين ملف السجل
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.info("جاري تحميل المكتبات الأساسية...")
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QMenuBar, 
                               QMenu, QAction, QMessageBox, QStatusBar)
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QIcon
    logger.info("تم تحميل PyQt5 بنجاح")
except ImportError as e:
    logger.error(f"خطأ في تحميل PyQt5: {str(e)}")
    print(f"خطأ في تحميل PyQt5: {str(e)}")
    input("اضغط Enter للإغلاق...")
    sys.exit(1)

# تعيين معالج الأخطاء العام
def exception_hook(exctype, value, tb):
    print('Exception:')
    print('Type:', exctype)
    print('Value:', value)
    print('Traceback:', ''.join(traceback.format_tb(tb)))
    sys.__excepthook__(exctype, value, tb)
    sys.exit(1)

sys.excepthook = exception_hook

try:
    from ui.widgets.dashboard_widget import DashboardWidget
    from ui.widgets.accounting_widget import AccountingWidget
    from ui.widgets.inventory_widget import InventoryWidget
    from ui.widgets.hr_widget import HRWidget
    from ui.widgets.reports_widget import ReportsWidget
    from ui.widgets.contacts_widget import ContactsWidget
    from database.db_config import init_database
except Exception as e:
    print(f"Error importing modules: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

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
    try:
        logger.info("بدء تشغيل البرنامج")
        
        # التحقق من وجود المجلدات المطلوبة
        required_folders = ['database', 'ui', 'utils', 'lang']
        for folder in required_folders:
            if not os.path.exists(os.path.join(current_dir, folder)):
                error_msg = f"المجلد المطلوب غير موجود: {folder}"
                logger.error(error_msg)
                print(error_msg)
                return 1

        # تهيئة قاعدة البيانات
        logger.info("جاري تهيئة قاعدة البيانات...")
        init_database()
        logger.info("تم تهيئة قاعدة البيانات بنجاح")
        
        # إنشاء التطبيق
        logger.info("جاري إنشاء تطبيق PyQt...")
        app = QApplication(sys.argv)
        
        # تعيين نمط التطبيق
        app.setStyle('Fusion')
        logger.info("تم تعيين نمط التطبيق")
        
        # إنشاء النافذة الرئيسية
        logger.info("جاري إنشاء النافذة الرئيسية...")
        main_window = MainWindow()
        main_window.show()
        logger.info("تم إنشاء وعرض النافذة الرئيسية")
        
        # تشغيل حلقة الأحداث
        logger.info("بدء تشغيل حلقة الأحداث")
        return app.exec_()
    except Exception as e:
        error_msg = f"خطأ في تشغيل البرنامج: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        print(error_msg)
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    try:
        print("بدء تشغيل البرنامج...")
        logger.info("بدء تشغيل البرنامج")
        
        # التحقق من المكتبات المطلوبة
        print("التحقق من المكتبات المطلوبة...")
        required_modules = {
            'PyQt5': 'واجهة المستخدم الرسومية',
            'pandas': 'معالجة البيانات',
            'openpyxl': 'التعامل مع ملفات Excel',
            'sqlite3': 'قاعدة البيانات'
        }
        
        for module_name, description in required_modules.items():
            try:
                __import__(module_name)
                print(f"✓ {module_name} موجود ({description})")
                logger.info(f"تم تحميل {module_name} بنجاح")
            except ImportError as e:
                error_msg = f"✗ {module_name} غير موجود ({description})"
                print(error_msg)
                logger.error(f"خطأ في تحميل {module_name}: {str(e)}")
                input("اضغط Enter للإغلاق...")
                sys.exit(1)
        
        print("بدء تشغيل التطبيق الرئيسي...")
        result = main()
        logger.info("إغلاق البرنامج")
        print("إغلاق البرنامج...")
        
        # حفظ السجل قبل الإغلاق
        logging.shutdown()
        
        sys.exit(result)
        
    except Exception as e:
        error_msg = f"حدث خطأ غير متوقع: {str(e)}"
        print(error_msg)
        logger.critical(error_msg)
        logger.critical(traceback.format_exc())
        print("تفاصيل الخطأ:")
        traceback.print_exc()
        
        print("\nيمكنك العثور على تفاصيل إضافية في ملف app.log")
        input("اضغط Enter للإغلاق...")
        sys.exit(1)
    
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
