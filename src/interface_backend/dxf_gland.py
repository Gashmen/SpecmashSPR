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
        self.addButton_2.clicked.connect(self.calculate_max_length_glands)
        self.addButton_2.clicked.connect(self.calculate_scale)
        self.addButton_2.clicked.connect(self.topside_draw_glands)
        self.addButton_2.clicked.connect(self.upside_draw_glands)
        self.addButton_2.clicked.connect(self.downside_draw_glands)
        self.addButton_2.clicked.connect(self.leftside_draw_glands)
        self.addButton_2.clicked.connect(self.cutside_draw_glands)
        self.addButton_2.clicked.connect(self.rightside_draw_glands)
        self.addButton_2.clicked.connect(self.withoutcapside_din)
        self.addButton_2.clicked.connect(self.withoutcapside_draw_glands)
        self.addButton_2.clicked.connect(self.draw_rightside_insert)
        self.addButton_2.clicked.connect(self.draw_topside_insert)
        self.addButton_2.clicked.connect(self.draw_leftside_insert)
        self.addButton_2.clicked.connect(self.draw_cutside_insert)
        self.addButton_2.clicked.connect(self.draw_withoutcapside_insert)
        self.addButton_2.clicked.connect(self.draw_upside_insert)
        self.addButton_2.clicked.connect(self.draw_downside_insert)
        self.addButton_2.clicked.connect(self.draw_installation_insert)


    def set_dict_dxf_glands(self):
        if hasattr(self.upside_block,'two_row_calculate'):
            self.glands_on_sides_dxf_dict = dict()
            for side_rus_name in self.glands_on_sides_dict:
                self.glands_on_sides_dxf_dict[side_rus_name] = list()
                for gland_csv_current in self.glands_on_sides_dict[side_rus_name]:
                    gland_dxf = dxf_gland.GlandDxfCircle()
                    gland_dxf.set_gland_csv_information(gland_csv_information=gland_csv_current)
                    gland_block = self.base_dxf.doc_base.blocks[gland_csv_current.gland_dxf_name + '_' + gland_csv_current.side]
                    gland_dxf.set_gland_dxf_block(block=gland_block)
                    gland_dxf.calculate_length()
                    self.glands_on_sides_dxf_dict[side_rus_name].append(gland_dxf)

    def calculate_max_length_glands(self):
        if hasattr(self,'glands_on_sides_dxf_dict'):
            self.scale_class.calculate_len0_x(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len2_x(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len4_x(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len6_x()
            self.scale_class.calculate_len8_x()
            self.scale_class.calculate_len9_x()
            self.scale_class.calculate_len11_x()

            self.scale_class.calculate_len0_y()
            self.scale_class.calculate_len2_y(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len4_y(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len6_y()

    def calculate_scale(self):
        if hasattr(self,'scale_class'):
            self.scale_class.calculate_scale()

    def topside_draw_glands(self):
        if hasattr(self, 'topside_block'):
            self.topside_block.draw_topside_exe_glands()
            if hasattr(self, 'rightside_block'):
                self.topside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self, 'leftside_block'):
                self.topside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self,'upside_block'):
                self.topside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self,'downside_block'):
                self.topside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
    def upside_draw_glands(self):
        if hasattr(self,'upside_block'):
            # self.rightside_block.draw_glands_in_block()
            self.upside_block.draw_upside_exe_glands()
            if hasattr(self,'rightside_block'):
                self.upside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self,'leftside_block'):
                self.upside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.upside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def downside_draw_glands(self):
        if hasattr(self,'downside_block'):
            # self.rightside_block.draw_glands_in_block()
            self.downside_block.draw_downside_exe_glands()
            if hasattr(self,'rightside_block'):
                self.downside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self,'leftside_block'):
                self.downside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.downside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def rightside_draw_glands(self):
        if hasattr(self,'rightside_block'):
            # self.rightside_block.draw_glands_in_block()
            self.rightside_block.draw_rightside_exe_glands()
            if hasattr(self,'upside_block'):
                self.rightside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self,'downside_block'):
                self.rightside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
            if hasattr(self,'topside_block'):
                self.rightside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def leftside_draw_glands(self):
        if hasattr(self, 'leftside_block'):
            # self.rightside_block.draw_glands_in_block()
            self.leftside_block.draw_leftside_exe_glands()
            if hasattr(self, 'upside_block'):
                self.leftside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self, 'downside_block'):
                self.leftside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.leftside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def cutside_draw_glands(self):
        if hasattr(self, 'cutside_block'):
            self.cutside_block.set_dict_glands_all_sizes(glands_on_sides_dict=self.glands_on_sides_dict)
            if hasattr(self, 'upside_block'):
                self.cutside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self, 'downside_block'):
                self.cutside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.cutside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def withoutcapside_din(self):
        if hasattr(self, 'withoutcapside_block'):
            self.withoutcapside_block.draw_din()

    def withoutcapside_draw_glands(self):
        if hasattr(self,'withoutcapside_block'):
            self.withoutcapside_block.set_dict_glands_all_sizes(glands_on_sides_dict=self.glands_on_sides_dict)
            if hasattr(self, 'rightside_block'):
                self.withoutcapside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self, 'leftside_block'):
                self.withoutcapside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self,'upside_block'):
                self.withoutcapside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self,'downside_block'):
                self.withoutcapside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)



    def save_doc(self):#тест, потом удалить
        self.base_dxf.doc_base.saveas('check.dxf')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfGlandQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())





