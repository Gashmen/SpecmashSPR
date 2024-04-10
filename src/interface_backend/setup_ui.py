import os
import sys
import ezdxf
import time
from PyQt5 import QtCore, QtGui, QtWidgets,Qt


from config import csv_config
from src.gui.py_ui import mainver03
from src.Widgets_Custom.Error import Ui_WidgetError
from src.smbconnect import smbconnect
from src.ldap_auth import backend_auth
from src.draw import BOM
from src.logger_sapr import logger_sapr


class SetupInterface(QtWidgets.QMainWindow, mainver03.Ui_MainWindow):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()
        self.connect_smb()  # получаем self.smb_specmash
        self.install_logger()
        QtCore.qInstallMessageHandler(self.qt_message_handler)


        self.setupUi(self)
        self.deletelastButton_2.setEnabled(False)

        '''Заполнение штампов'''
        self.task_number = ''      #Номер заявки
        self.position_number = ''  #Номер позиции
        self.designer_name = ''    #Имя разработчика

        self.pdf_files = list()

        '''Заполнение спецификации'''
        #УСТАНОВКА КЛАССА ДЛЯ ВСЕГО BOM
        self.BOM_general = BOM.BOM_GENERAL()

        self.stackedWidget.setCurrentIndex(0) #Устанавливает на оболочках stackedWidget
        self.set_manufacturers()

        '''Дополнительные окна при запуске'''
        self.error_window = Ui_WidgetError()

        '''КНОПКИ'''
        self.terminalButton_leftMenu.clicked.connect(self.set_terminal_page)
        self.optionsButton_leftMenu.clicked.connect(self.set_options_page)

        # self.pushButton_2.clicked.connect(self.error_window.call_error)
        self.welcomewindowButton.clicked.connect(self.home_window)

        self.stackedWidget.currentChanged.connect(self.updateButtonColors)
        self.shellButton_leftMenu.setStyleSheet("background-color: rgb(97, 149, 156);")


    def install_logger(self):
        self.logger = logger_sapr.LoggerSapr()

        self.logger_time = time.time()


    def qt_message_handler(self,mode, context, message):
        if mode == 4:
            mode = 'INFO'
        elif mode == 1:
            mode = 'WARNING'
        elif mode == 2:
            mode = 'CRITICAL'
        elif mode == 3:
            mode = 'FATAL'
        else:
            mode = 'DEBUG'
        self.logger.logger.info('qt_message_handler: line: %d, func: %s(), file: %s' % (
            context.line, context.function, context.file))
        self.logger.logger.info('  %s: %s\n' % (mode, message))
        self.logger.logger.info(time.time() - self.logger_time)

        self.smb_specmash.save_log(logger_path=self.logger.logger_path)

        # with open(self.logger.logger_path, 'r') as fr, open(f'{os.getlogin()}_{time.time()}.txt', 'w') as fw:
        #     for line in fr:
        #         fw.write(line)

        print('qt_message_handler: line: %d, func: %s(), file: %s' % (
            context.line, context.function, context.file))
        print('  %s: %s\n' % (mode, message))


    def set_authorization_information(self,
                                      task_number='',
                                      position_number='',
                                      designer_name='',
                                      userlogin=''):
        '''Установка параметров для заполнения дальнейшего:шильдов и тд'''
        self.task_number = task_number
        self.position_number = position_number
        self.designer_name = designer_name
        self.userlogin = userlogin

    def connect_smb(self):
        '''Установка соединения по SMB для получение информации'''
        self.smb_specmash = smbconnect.SMBCONNECT_SPECMASH_SERVER()
        self.smb_specmash.install_connect()
        #ДЛЯ ТЕСТА, ПОТОМ УДАЛИТЬ


    def set_manufacturers(self):
        # self.add_manufacturer_inputs_combobox()
        self.add_manufacturer_terminal_combobox()


    def set_terminal_page(self):
        '''Устанавливает 2 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 2:
            self.stackedWidget.setCurrentIndex(2)

    def add_manufacturer_terminal_combobox(self):
        self.manufacturer_terminal_combobox.clear()
        self.manufacturer_terminal_combobox.addItems(csv_config.TERMINAL_MANUFACTURER)

    def set_options_page(self):
        '''Устанавливает 3 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 3:
            self.stackedWidget.setCurrentIndex(3)

    def home_window(self):
        '''открытие окна дом'''
        self.home_window = backend_auth.AuthWindow()
        self.home_window.set_task_number(self.task_number)
        self.home_window.set_position_number(self.position_number)
        self.close()
        self.home_window.show()

    def closeEvent(self, event):
        try:
            self.smb_specmash.save_log(logger_path=self.logger.logger_path)
        except:
            pass

    def updateButtonColors(self, index):
        # Set button colors based on current page index
        if index == 0:
            self.shellButton_leftMenu.setStyleSheet("background-color: rgb(97, 149, 156);")
            self.inputsButton_leftMenu.setStyleSheet("background-color: none;")
            self.terminalButton_leftMenu.setStyleSheet("background-color: none;")
        elif index == 1:
            self.shellButton_leftMenu.setStyleSheet("background-color: none;")
            self.inputsButton_leftMenu.setStyleSheet("background-color: rgb(97, 149, 156);")
            self.terminalButton_leftMenu.setStyleSheet("background-color: none;")
        elif index == 2:
            self.shellButton_leftMenu.setStyleSheet("background-color: none;")
            self.inputsButton_leftMenu.setStyleSheet("background-color: none;")
            self.terminalButton_leftMenu.setStyleSheet("background-color: rgb(97, 149, 156);")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = SetupInterface()
    welcome_window.show()
    sys.exit(app.exec_())




