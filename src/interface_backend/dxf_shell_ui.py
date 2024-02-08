import ezdxf
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from src.interface_backend import dxf_base_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ

from config import dxf_config
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox,Shell_Error
from src.draw import base
from src.draw.shell_side import dxf_shell

class DxfShellQtCommunication(dxf_base_ui.DxfQtCommunication):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()


        '''COMBOBOX'''
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.check_possible_to_add_shell)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.set_shell_blocks)

        self.sideVListWidget.model().rowsInserted.connect(self.test_draw_glands_in_downside)
        self.sideVListWidget.model().rowsRemoved.connect(self.test_draw_glands_in_downside)




    def set_shell_blocks(self):
        self.set_shell_topside_block()
        self.set_shell_downside_block()

    def check_possible_to_add_shell(self):
        '''Проверка возможности добавления коробки
        Есть ли она в базе dxf'''
        if hasattr(self, 'shell_dict'):
            if hasattr(self, 'shell_base_dxf'):
                self.possible_shell_draw = self.base_dxf.check_shell(shell_translite_name=self.shell_base_dxf.shell_translit_name)
                if self.possible_shell_draw == False:
                    window_shellerror = Shell_Error.Ui_ShellError()
                    window_shellerror.call_shellerror()


    def set_shell_topside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.topside_block = dxf_shell.ShellTopSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                 doc_base=self.base_dxf.doc_base,
                                                                 glands_on_sides_dict=self.glands_on_sides_dict)


    def set_shell_downside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.downside_block = dxf_shell.ShellDownSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                   doc_base=self.base_dxf.doc_base,
                                                                   glands_on_sides_dict=self.glands_on_sides_dict)

    def test_draw_glands_in_downside(self):
        if hasattr(self,'downside_block'):
            self.downside_block.calculate_coordinate_glands_for_draw()
            print(self.glands_on_sides_dict)














if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfShellQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())



