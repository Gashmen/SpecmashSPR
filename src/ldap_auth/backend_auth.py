import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QDialog

import logging
import tempfile

from src.ldap_auth import frontend_auth
from src.ldap_auth import ldap_auth
from src.scripts import scripts_start

class AuthWindow(QtWidgets.QMainWindow, frontend_auth.Ui_WelcomeWindow):

    def __init__(self):
        '''ИНИЦИАЛИЗАЦИЯ'''

        super().__init__()
        self.setupUi(self)
        self.authorization()

        '''PUSH BUTTONS ACTION'''
        self.junction_boxes_pushButton.clicked.connect(self.show_jb_qt)
        self.scripts_pushButton.clicked.connect(self.show_window_scripts)

    def authorization(self):
        self.set_ldap_connect()
        self.set_username()

    def set_ldap_connect(self):
        '''
        Подключение по LDAP окна запуска
        :return:
        '''
        self.ldap_auth = ldap_auth.LDAP_AUTH()
        self.ldap_auth.connect()
        self.ldap_auth.give_employees_information()
        ### Для получения словаря с пользователями self.ldap_auth.authorization_information
        print(self.ldap_auth.authorization_information)

    def set_username(self):
        '''Устанавливаем того, кто использует программу'''
        pc_username = os.getlogin()
        if (pc_username != '' and pc_username != 'admin'):
            if self.ldap_auth.authorization_information.get(pc_username, False) != False:
                self.username_QLineEdit.insert(self.ldap_auth.authorization_information[pc_username])
                self.username_QLineEdit.setEnabled(False)
            else:
                return False

    def return_username(self):
        '''Возвращает username'''
        return self.username_QLineEdit.text()

    def return_task_number(self):
        '''Возвращает номер заявки'''
        return self.number_task_QLineEdit.text()

    def return_position_number(self):
        '''Возвращает номер заявки'''
        return self.position_number_QLineEdit.text()

    def set_task_number(self,task_number):
        '''Устанавливает номер задачи'''
        self.number_task_QLineEdit.setText(task_number)

    def set_position_number(self,position_number):
        '''Устанавливает номер задачи'''
        self.position_number_QLineEdit.setText(position_number)

    def return_userlogin(self):
        '''Возвращаем os.getlogin() если есть self.position_number_QLineEdit.text()'''
        if self.position_number_QLineEdit.text() != '':
            return os.getlogin()

    def show_window_scripts(self):
        self.scripts_window = scripts_start.ScriptsMainWindow()
        self.close()
        self.scripts_window.show()

    def show_jb_qt(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    authWindow = AuthWindow()
    authWindow.show()
    sys.exit(app.exec_())