import ezdxf
import os
import sys

import time

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from src.interface_backend import gland_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ

from config import dxf_config
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox
from src.draw import base,scale,BOM

import copy
from src.draw.shell_side import dxf_shell



class DxfQtCommunication(gland_ui.GlandInterface):

    def __init__(self):
        super(DxfQtCommunication, self).__init__()
        #ПОЛУЧЕНИЕ ПУТИ ДЛЯ БАЗЫ DXF
        self.connect_dxf_base()
        time_setdoc = time.time()
        self.set_doc()
        print('self.set_doc: ', time_setdoc - time.time())
        self.set_scale_dxf()


        #УСТАНОВКА ХЭШ СЛОВАРЕЙ ДЛЯ ПОТОМ УДАЛЕНИЯ БЛОКОВ ИЗ ОБЩЕЙ БАЗЫ И ИЗ БЛОКОВ
        self.set_list_used_blocks_shell()
        self.set_list_used_blocks_terminals()

        #УСТАНОВКА КЛАССА ДЛЯ ВСЕГО BOM
        self.BOM_general = BOM.BOM_GENERAL()

        '''СОMBOBOX SHELL'''

    def connect_dxf_base(self):
        self.smb_specmash.get_base_dxf_path()

    @Qt.pyqtSlot()
    def set_doc(self):
        if hasattr(self.smb_specmash,'dxf_base_path'):
            self.base_dxf = base.DxfBase()
            self.base_dxf.set_dxf_base_path(dxf_base_path=self.smb_specmash.dxf_base_path)
            self.base_dxf.set_doc_dxf()
            # self.base_dxf.doc_base = copy.deepcopy(self.base_dxf.doc_for_update)
            self.base_dxf.delete_all_entities()
            self.base_dxf.give_all_blocks()

    # def create_doc_copy(self):
    #     self.base_dxf.doc_base = copy.deepcopy(self.base_dxf.doc_for_update)

    def set_scale_dxf(self):
        self.scale_class = scale.ScaleBorder()


    def set_list_used_blocks_shell(self):
        self.list_used_blocks_shell = list()


    def set_list_used_blocks_terminals(self):
        self.list_used_blocks_terminals = list()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())

