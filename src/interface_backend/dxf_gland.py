import ezdxf
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import dxf_shell_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ
from src.draw.gland import dxf_gland


from config import dxf_config
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox,UI_BaseError
from src.draw import base
from src.draw.shell_side import dxf_shell


class DxfGlandQtCommunication(dxf_shell_ui.DxfShellQtCommunication):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        self.addButton_2.clicked.connect(self.set_dict_dxf_glands)

        self.Autohelper.clicked.connect(self.save_doc)#Тест, потом удалить


    def set_dict_dxf_glands(self):
        if hasattr(self.upside_block,'two_row_calculate'):
            glands_on_sides_dxf_dict = dict()
            for side_rus_name in self.glands_on_sides_dict:
                glands_on_sides_dxf_dict[side_rus_name] = list()
                for gland_csv_current in self.glands_on_sides_dict[side_rus_name]:
                    gland_dxf = dxf_gland.GlandDxfCircle()
                    gland_dxf.set_gland_csv_information(gland_csv_information=gland_csv_current)
                    gland_block = self.base_dxf.doc_base.blocks[gland_csv_current.gland_dxf_name + '_' + gland_csv_current.side]
                    gland_dxf.set_gland_dxf_block(block=gland_block)
                    gland_dxf.calculate_length()
                    glands_on_sides_dxf_dict[side_rus_name].append(gland_dxf)

    def save_doc(self):#тест, потом удалить
        block_name = [block.dxf.name for block in self.base_dxf.doc_base.blocks if '*' not in block.dxf.name]
        for block in block_name:
            try:
                self.base_dxf.doc_base.blocks.delete_block(name=block)
            except:
                continue
        self.base_dxf.doc_base.saveas('check.dxf')






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfGlandQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())





