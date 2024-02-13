import os
import sys
import ezdxf
import time
from PyQt5 import QtCore, QtGui, QtWidgets,Qt


from config import csv_config
from src.gui.py_ui import mainver03
from src.Widgets_Custom.Error import Ui_WidgetError
from src.smbconnect import smbconnect

class SetupInterface(QtWidgets.QMainWindow, mainver03.Ui_MainWindow):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()
        QtCore.qInstallMessageHandler(self.qt_message_handler)
        self.connect_smb() #получаем self.smb_specmash

        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0) #Устанавливает на оболочках stackedWidget
        self.set_manufacturers()

        '''Дополнительные окна при запуске'''
        self.error_window = Ui_WidgetError()

        '''КНОПКИ'''
        self.terminalButton_leftMenu.clicked.connect(self.set_terminal_page)
        self.optionsButton_leftMenu.clicked.connect(self.set_options_page)

        self.pushButton_2.clicked.connect(self.error_window.call_error)

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
        self.add_manufacturer_inputs_combobox()
        self.add_manufacturer_terminal_combobox()

    def add_manufacturer_inputs_combobox(self):
        '''Пока поставим производителя только ВЗОР'''
        self.manufacturerInputsComboBox.clear()
        self.manufacturerInputsComboBox.addItems(csv_config.GLAND_MANUFACTURER)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = SetupInterface()
    welcome_window.show()
    sys.exit(app.exec_())




