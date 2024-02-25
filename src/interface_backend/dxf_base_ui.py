import ezdxf
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from src.interface_backend import gland_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ

from config import dxf_config
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox
from src.draw import base,scale
from src.draw.shell_side import dxf_shell



class DxfQtCommunication(gland_ui.GlandInterface):

    def __init__(self):
        super(DxfQtCommunication, self).__init__()
        #ПОЛУЧЕНИЕ ПУТИ ДЛЯ БАЗЫ DXF
        self.connect_dxf_base()
        self.set_doc()
        self.set_scale_dxf()

        '''СОMBOBOX SHELL'''
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.set_shell_base_dxf)

    def connect_dxf_base(self):
        self.smb_specmash.get_base_dxf_path()

    @Qt.pyqtSlot()
    def set_doc(self):
        if hasattr(self.smb_specmash,'dxf_base_path'):
            self.base_dxf = base.DxfBase()
            self.base_dxf.set_dxf_base_path(dxf_base_path=self.smb_specmash.dxf_base_path)
            self.base_dxf.set_doc_dxf()
            self.base_dxf.delete_all_entities()
            self.base_dxf.give_all_blocks()



    @Qt.pyqtSlot()
    def set_shell_base_dxf(self):
        if hasattr(self,'shell_dict'):
            self.shell_base_dxf = dxf_shell.ShellBaseDxf(shell_dict=self.shell_dict)
            self.shell_base_dxf.set_russian_name_shell()
            self.shell_base_dxf.set_translit_name()


    def set_scale_dxf(self):
        self.scale_class = scale.ScaleBorder()






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())

