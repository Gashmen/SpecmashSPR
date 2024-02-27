import ezdxf
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import dxf_terminal_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ


class MainPageDxfQtCommunication(dxf_terminal_ui.DxfTerminalQtCommunication):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()
        self.Autohelper.clicked.connect(self.create_border)
        self.Autohelper.clicked.connect(self.save_doc)

    def create_border(self):
        '''Создает рамку относительно '''
        block_border = self.base_dxf.doc_base.blocks['Border_A3']
        values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
        self.border_insert = self.base_dxf.doc_base.modelspace().add_blockref(name='Border_A3',
                                                                              insert=(0,0))
        self.border_insert.add_auto_attribs(values)

    def create_dimension(self):
        '''Создаем размер'''







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = MainPageDxfQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())