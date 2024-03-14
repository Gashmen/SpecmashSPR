import ezdxf
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import terminal_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ

from config import dxf_config
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox,UI_BaseError
from src.draw import base
from src.draw.shell_side import dxf_shell

class DxfShellQtCommunication(terminal_ui.TerminalUi):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()


    @Qt.pyqtSlot()
    def set_shell_base_dxf(self):
        if hasattr(self,'shell_dict'):
            self.shell_base_dxf = dxf_shell.ShellBaseDxf(shell_dict=self.shell_dict)
            self.shell_base_dxf.set_russian_name_shell()
            self.shell_base_dxf.set_translit_name()

    @Qt.pyqtSlot()
    def set_shell_blocks(self):
        if hasattr(self, 'shell_dict'):
            if hasattr(self, 'shell_base_dxf'):
                if hasattr(self,'possible_shell_draw'):
                    if self.possible_shell_draw == True:
                        self.set_shell_topside_block()
                        self.set_shell_downside_block()
                        self.set_shell_leftside_block()
                        self.set_shell_upside_block()
                        self.set_shell_rightside_block()
                        self.set_shell_cutside_block()
                        self.set_shell_withoutcapside_block()
                        self.withoutcapside_din()
                        self.set_shell_installation_block()

    @Qt.pyqtSlot()
    def check_possible_to_add_shell(self):
        '''Проверка возможности добавления коробки
        Есть ли она в базе dxf'''
        if hasattr(self, 'shell_dict'):
            if hasattr(self, 'shell_base_dxf'):
                self.possible_shell_draw = self.base_dxf.check_shell(shell_translite_name=self.shell_base_dxf.shell_translit_name)
                if self.possible_shell_draw == False:
                    QMessageBox.critical(self, "Ошибка",
                                         f"В базе для отрисовки нет всех необходимых блоков для построения оболочки",
                                         QMessageBox.Ok)
                    delattr(self,'shell_dict')
                    self.sizeCombobox_shellpage.setCurrentIndex(0)


    def set_shell_topside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.topside_block = dxf_shell.ShellTopSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                 doc_base=self.base_dxf.doc_base,
                                                                 glands_on_sides_dict=self.glands_on_sides_dict)
                self.topside_block.define_extreme_lines()
                self.scale_class.calculate_len3_x(topside_extreme_lines=self.topside_block.extreme_lines)
                self.scale_class.calculate_len3_y(topside_extreme_lines=self.topside_block.extreme_lines)

    def set_shell_upside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.upside_block = dxf_shell.ShellUpSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                   doc_base=self.base_dxf.doc_base,
                                                                   glands_on_sides_dict=self.glands_on_sides_dict)
                self.upside_block.define_extreme_lines()
                self.scale_class.calculate_len1_y(upside_extreme_lines=self.upside_block.extreme_lines)
    def set_shell_downside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.downside_block = dxf_shell.ShellDownSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                   doc_base=self.base_dxf.doc_base,
                                                                   glands_on_sides_dict=self.glands_on_sides_dict)
                self.downside_block.define_extreme_lines()


    def set_shell_leftside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.leftside_block = dxf_shell.ShellLeftSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                   doc_base=self.base_dxf.doc_base,
                                                                   glands_on_sides_dict=self.glands_on_sides_dict)
                self.leftside_block.define_extreme_lines()
                self.scale_class.calculate_len5_x(leftside_extreme_lines=self.leftside_block.extreme_lines)

    def set_shell_rightside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.rightside_block = dxf_shell.ShellRightSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                     doc_base=self.base_dxf.doc_base,
                                                                     glands_on_sides_dict=self.glands_on_sides_dict)
                self.rightside_block.define_extreme_lines()
                self.scale_class.calculate_len1_x(rightside_extreme_lines=self.rightside_block.extreme_lines)

    def set_shell_installation_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self, 'shell_base_dxf'):
                self.installation_block = dxf_shell.ShellInstallationBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                           doc_base=self.base_dxf.doc_base)
                self.installation_block.define_extreme_lines()
                self.scale_class.calculate_len5_y(installation_extreme_lines=self.installation_block.extreme_lines)

    def set_shell_cutside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self, 'shell_base_dxf'):
                self.cutside_block = dxf_shell.ShellCutSideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                 doc_base=self.base_dxf.doc_base)
                self.cutside_block.define_extreme_lines()
                self.scale_class.calculate_len7_x()

    def set_shell_withoutcapside_block(self):
        if hasattr(self,'shell_dict'):
            if hasattr(self,'shell_base_dxf'):
                self.withoutcapside_block = dxf_shell.ShellWithoutcapsideBlock(translit_name=self.shell_base_dxf.shell_translit_name,
                                                                               doc_base=self.base_dxf.doc_base)
                self.withoutcapside_block.define_extreme_lines()
                self.scale_class.calculate_len10_x()
                # self.withoutcapside_din()

    def draw_rightside_insert(self):
        x_coordinate_rightside = 0
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_rightside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len0_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_rightside += self.scale_class.len0_x / self.scale_class.scale
        if hasattr(self,'rightside_block'):
            x_coordinate_rightside += self.rightside_block.extreme_lines['y_max'] / self.scale_class.scale

        y_coordinate_rightside = 0
        if hasattr(self.scale_class,'free_space_y'):
            y_coordinate_rightside += self.scale_class.free_space_y/4
        if hasattr(self.scale_class,'len0_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_rightside += self.scale_class.len0_y /self.scale_class.scale
        if hasattr(self.scale_class,'len1_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_rightside += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class,'len2_y') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_rightside += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_rightside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_rightside += self.scale_class.free_space_y / 4
        if hasattr(self, 'rightside_block'):
            y_coordinate_rightside += -self.rightside_block.extreme_lines['x_min'] / self.scale_class.scale

        self.rightside_insert = self.base_dxf.doc_base.modelspace().add_blockref(name=self.rightside_block.shell_side_name,
                                                                                    insert=(x_coordinate_rightside,
                                                                                            y_coordinate_rightside))
        self.rightside_insert.dxf.rotation = 90
        self.rightside_insert.dxf.xscale = 1/ self.scale_class.scale
        self.rightside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.rightside_insert.dxf.zscale = 1 / self.scale_class.scale

    def draw_topside_insert(self):
        x_coordinate_topside = 0
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_topside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len0_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_topside += self.scale_class.len0_x /  self.scale_class.scale
        if hasattr(self.scale_class,'len1_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_topside += self.scale_class.len1_x /  self.scale_class.scale
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_topside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len2_x') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_topside += 1.5 * self.scale_class.len2_x /  self.scale_class.scale
            else:
                x_coordinate_topside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self,'topside_block'):
            x_coordinate_topside += (-self.topside_block.extreme_lines['x_min']) / self.scale_class.scale

        y_coordinate_topside = 0
        if hasattr(self.scale_class,'free_space_y'):
            y_coordinate_topside += self.scale_class.free_space_y/4
        if hasattr(self.scale_class,'len0_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_topside += self.scale_class.len0_y /self.scale_class.scale
        if hasattr(self.scale_class,'len1_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_topside += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class,'len2_y') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_topside += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_topside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_topside += self.scale_class.free_space_y / 4
        if hasattr(self, 'topside_block'):
            y_coordinate_topside += (-self.topside_block.extreme_lines['y_min']) / self.scale_class.scale

        self.topside_insert = self.base_dxf.doc_base.modelspace().add_blockref(name=self.topside_block.shell_side_name,
                                                                                    insert=(x_coordinate_topside,
                                                                                            y_coordinate_topside))
        self.topside_insert.dxf.rotation = 0
        self.topside_insert.dxf.xscale = 1/self.scale_class.scale
        self.topside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.topside_insert.dxf.zscale = 1 / self.scale_class.scale



    def draw_leftside_insert(self):
        x_coordinate_leftside = 0
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_leftside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len0_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_leftside += self.scale_class.len0_x /  self.scale_class.scale
        if hasattr(self.scale_class,'len1_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_leftside += self.scale_class.len1_x /  self.scale_class.scale
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_leftside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len2_x') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_leftside += 1.5 * self.scale_class.len2_x /  self.scale_class.scale
            else:
                x_coordinate_leftside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self.scale_class,'len3_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_leftside += self.scale_class.len3_x / self.scale_class.scale
        if hasattr(self.scale_class,'len4_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_leftside += self.scale_class.len4_x / self.scale_class.scale
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_leftside += self.scale_class.free_space_x/6
        if hasattr(self,'leftside_block'):
            x_coordinate_leftside += (-self.leftside_block.extreme_lines['y_min']) / self.scale_class.scale

        y_coordinate_leftside = 0
        if hasattr(self.scale_class,'free_space_y'):
            y_coordinate_leftside += self.scale_class.free_space_y/4
        if hasattr(self.scale_class,'len0_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_leftside += self.scale_class.len0_y /self.scale_class.scale
        if hasattr(self.scale_class,'len1_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_leftside += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class,'len2_y') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_leftside += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_leftside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_leftside += self.scale_class.free_space_y / 4
        if hasattr(self, 'leftside_block'):
            y_coordinate_leftside += self.leftside_block.extreme_lines['x_max'] / self.scale_class.scale

        self.leftside_insert = self.base_dxf.doc_base.modelspace().add_blockref(name=self.leftside_block.shell_side_name,
                                                                                    insert=(x_coordinate_leftside,
                                                                                            y_coordinate_leftside))
        self.leftside_insert.dxf.rotation = 270
        self.leftside_insert.dxf.xscale = 1 / self.scale_class.scale
        self.leftside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.leftside_insert.dxf.zscale = 1 / self.scale_class.scale


    def draw_cutside_insert(self):
        x_coordinate_cutside = 0
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_cutside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len0_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_cutside += self.scale_class.len0_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_cutside += self.scale_class.len1_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_cutside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len2_x') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_cutside += 1.5 * self.scale_class.len2_x / self.scale_class.scale
            else:
                x_coordinate_cutside += 1.5 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'len3_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_cutside += self.scale_class.len3_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len4_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_cutside += self.scale_class.len4_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_cutside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len5_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_cutside += self.scale_class.len5_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len6_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_cutside += self.scale_class.len6_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_cutside += self.scale_class.free_space_x / 6
        if hasattr(self, 'cutside_block'):
            x_coordinate_cutside += (-self.cutside_block.extreme_lines['y_min']) / self.scale_class.scale

        y_coordinate_cutside = 0
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_cutside += self.scale_class.free_space_y / 4
        if hasattr(self.scale_class, 'len0_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_cutside += self.scale_class.len0_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_cutside += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len2_y') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_cutside += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_cutside += 1.5 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_cutside += self.scale_class.free_space_y / 4

        if hasattr(self, 'cutside_block'):
            y_coordinate_cutside += self.cutside_block.extreme_lines['x_max'] / self.scale_class.scale

        self.cutside_insert = self.base_dxf.doc_base.modelspace().add_blockref(
            name=self.cutside_block.shell_side_name,
            insert=(x_coordinate_cutside,
                    y_coordinate_cutside))
        self.cutside_insert.dxf.rotation = 270
        self.cutside_insert.dxf.xscale = 1 / self.scale_class.scale
        self.cutside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.cutside_insert.dxf.zscale = 1 / self.scale_class.scale
    def withoutcapside_din(self):
        if hasattr(self, 'withoutcapside_block'):
            self.withoutcapside_block.draw_din()
    def draw_withoutcapside_insert(self):
        x_coordinate_withoutcapside = 0
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_withoutcapside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len0_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len0_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len1_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_withoutcapside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len2_x') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_withoutcapside += 1.5 * self.scale_class.len2_x / self.scale_class.scale
            else:
                x_coordinate_withoutcapside += 1.5 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'len3_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len3_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len4_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len4_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_withoutcapside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len5_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len5_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len6_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len6_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len7_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len7_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_withoutcapside += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len8_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len8_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len9_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_withoutcapside += self.scale_class.len9_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_withoutcapside += self.scale_class.free_space_x / 6
        if hasattr(self, 'withoutcapside_block'):
            x_coordinate_withoutcapside += (-self.withoutcapside_block.extreme_lines['x_min']) / self.scale_class.scale

        y_coordinate_withoutcapside = 0
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_withoutcapside += self.scale_class.free_space_y / 4
        if hasattr(self.scale_class, 'len0_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_withoutcapside += self.scale_class.len0_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_withoutcapside += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len2_y') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_withoutcapside += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_withoutcapside += 1.5 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_withoutcapside += self.scale_class.free_space_y / 4

        if hasattr(self, 'withoutcapside_block'):
            y_coordinate_withoutcapside += -self.withoutcapside_block.extreme_lines['y_min'] / self.scale_class.scale

        self.withoutcapside_insert = self.base_dxf.doc_base.modelspace().add_blockref(
            name=self.withoutcapside_block.shell_side_name,
            insert=(x_coordinate_withoutcapside,
                    y_coordinate_withoutcapside))
        self.withoutcapside_insert.dxf.rotation = 0
        self.withoutcapside_insert.dxf.xscale = 1 / self.scale_class.scale
        self.withoutcapside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.withoutcapside_insert.dxf.zscale = 1 / self.scale_class.scale

    def draw_upside_insert(self):
        x_coordinate_upside = 0
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_upside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len0_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_upside += self.scale_class.len0_x /  self.scale_class.scale
        if hasattr(self.scale_class,'len1_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_upside += self.scale_class.len1_x /self.scale_class.scale
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_upside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len2_x') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_upside += 1.5 * self.scale_class.len2_x /  self.scale_class.scale
            else:
                x_coordinate_upside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self,'upside_block'):
            x_coordinate_upside += (self.upside_block.extreme_lines['x_max']) / self.scale_class.scale

        y_coordinate_upside = 0
        if hasattr(self.scale_class,'free_space_y'):
            y_coordinate_upside += self.scale_class.free_space_y/4
        if hasattr(self.scale_class,'len0_y') and hasattr(self.scale_class,'scale'):
            y_coordinate_upside += self.scale_class.len0_y /self.scale_class.scale
        if hasattr(self, 'upside_block'):
            y_coordinate_upside += (self.upside_block.extreme_lines['y_max']) / self.scale_class.scale

        self.upside_insert = self.base_dxf.doc_base.modelspace().add_blockref(name=self.upside_block.shell_side_name,
                                                                                    insert=(x_coordinate_upside,
                                                                                            y_coordinate_upside))
        self.upside_insert.dxf.rotation = 180
        self.upside_insert.dxf.xscale = 1/self.scale_class.scale
        self.upside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.upside_insert.dxf.zscale = 1 / self.scale_class.scale

    def draw_downside_insert(self):
        x_coordinate_downside = 0
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_downside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len0_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_downside += self.scale_class.len0_x /  self.scale_class.scale
        if hasattr(self.scale_class,'len1_x') and hasattr(self.scale_class,'scale'):
            x_coordinate_downside += self.scale_class.len1_x /self.scale_class.scale
        if hasattr(self.scale_class,'free_space_x'):
            x_coordinate_downside += self.scale_class.free_space_x/6
        if hasattr(self.scale_class,'len2_x') and hasattr(self.scale_class,'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_downside += 1.5 * self.scale_class.len2_x /  self.scale_class.scale
            else:
                x_coordinate_downside += 1.5 * max([self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,self.scale_class.len4_x])/ self.scale_class.scale
        if hasattr(self,'downside_block'):
            x_coordinate_downside += (-self.downside_block.extreme_lines['x_min']) / self.scale_class.scale

        y_coordinate_downside = 0
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_downside += self.scale_class.free_space_y / 4
        if hasattr(self.scale_class, 'len0_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_downside += self.scale_class.len0_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_downside += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len2_y') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_downside += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_downside += 1.5 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_downside += self.scale_class.free_space_y / 4
        if hasattr(self.scale_class, 'len3_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_downside += self.scale_class.len3_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len4_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_downside += self.scale_class.len4_y / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_downside += self.scale_class.free_space_y / 4

        if hasattr(self, 'downside_block'):
            y_coordinate_downside += -self.downside_block.extreme_lines['y_min'] / self.scale_class.scale

        self.downside_insert = self.base_dxf.doc_base.modelspace().add_blockref(name=self.downside_block.shell_side_name,
                                                                                    insert=(x_coordinate_downside,
                                                                                            y_coordinate_downside))
        self.downside_insert.dxf.rotation = 0
        self.downside_insert.dxf.xscale = 1/self.scale_class.scale
        self.downside_insert.dxf.yscale = 1 / self.scale_class.scale
        self.downside_insert.dxf.zscale = 1 / self.scale_class.scale

    def draw_installation_insert(self):
        x_coordinate_installation = 0
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_installation += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len0_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len0_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len1_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_installation += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len2_x') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_x) != 0:
                x_coordinate_installation += 1.50 * self.scale_class.len2_x / self.scale_class.scale
            else:
                x_coordinate_installation += 1.50 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'len3_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len3_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len4_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len4_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_installation += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len5_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len5_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len6_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len6_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len7_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len7_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_installation += self.scale_class.free_space_x / 6
        if hasattr(self.scale_class, 'len8_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len8_x / self.scale_class.scale
        if hasattr(self.scale_class, 'len9_x') and hasattr(self.scale_class, 'scale'):
            x_coordinate_installation += self.scale_class.len9_x / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_x'):
            x_coordinate_installation += self.scale_class.free_space_x / 6
        if hasattr(self, 'withoutcapside_block'):
            x_coordinate_installation += (-self.withoutcapside_block.extreme_lines['x_min']) / self.scale_class.scale

        y_coordinate_installation = 0
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_installation += self.scale_class.free_space_y / 4
        if hasattr(self.scale_class, 'len0_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_installation += self.scale_class.len0_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len1_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_installation += self.scale_class.len1_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len2_y') and hasattr(self.scale_class, 'scale'):
            if int(self.scale_class.len2_y) != 0:
                y_coordinate_installation += 1.5 * self.scale_class.len2_y / self.scale_class.scale
            else:
                y_coordinate_installation += 1.5 * max(
                    [self.scale_class.len2_y, self.scale_class.len4_y, self.scale_class.len2_x,
                     self.scale_class.len4_x]) / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_installation += self.scale_class.free_space_y / 4
        if hasattr(self.scale_class, 'len3_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_installation += self.scale_class.len3_y / self.scale_class.scale
        if hasattr(self.scale_class, 'len4_y') and hasattr(self.scale_class, 'scale'):
            y_coordinate_installation += self.scale_class.len4_y / self.scale_class.scale
        if hasattr(self.scale_class, 'free_space_y'):
            y_coordinate_installation += self.scale_class.free_space_y / 4

        if hasattr(self, 'installation_block'):
            y_coordinate_installation += -self.installation_block.extreme_lines['y_min'] / self.scale_class.scale

        self.installation_insert = self.base_dxf.doc_base.modelspace().add_blockref(
            name=self.installation_block.shell_side_name,
            insert=(x_coordinate_installation,
                    y_coordinate_installation))
        self.installation_insert.dxf.rotation = 0
        self.installation_insert.dxf.xscale = 1 / self.scale_class.scale
        self.installation_insert.dxf.yscale = 1 / self.scale_class.scale
        self.installation_insert.dxf.zscale = 1 / self.scale_class.scale

    def delete_shell_dxf(self):
        self.list_used_blocks_shell.clear()

    def add_used_shell_insert(self):
        self.list_used_blocks_shell.append(self.rightside_insert)
        self.list_used_blocks_shell.append(self.leftside_insert)
        self.list_used_blocks_shell.append(self.upside_insert)
        self.list_used_blocks_shell.append(self.downside_insert)
        self.list_used_blocks_shell.append(self.topside_insert)
        self.list_used_blocks_shell.append(self.cutside_insert)
        self.list_used_blocks_shell.append(self.withoutcapside_block.din_insert)
        self.list_used_blocks_shell.append(self.withoutcapside_insert)
        self.list_used_blocks_shell.append(self.installation_insert)

    @Qt.pyqtSlot()
    def draw_shells_inserts(self):
        self.base_dxf.doc_base.modelspace().delete_all_entities()
        if hasattr(self, 'shell_dict'):
            if hasattr(self, 'shell_base_dxf'):
                if hasattr(self, 'possible_shell_draw'):
                    if self.possible_shell_draw:
                        self.delete_shell_dxf()
                        self.draw_rightside_insert()
                        self.draw_topside_insert()
                        self.draw_leftside_insert()
                        self.draw_cutside_insert()
                        self.draw_withoutcapside_insert()
                        self.draw_upside_insert()
                        self.draw_downside_insert()
                        self.draw_installation_insert()
                        self.add_used_shell_insert()

    def calculate_scale_shell(self):
        self.scale_class.calculate_scale()

    def set_zero_max_glands_length(self):
        if self.sideAListWidget.count() == 0 and\
                self.sideBListWidget.count()==0 and\
                self.sideVListWidget.count()==0 and\
                self.sideGListWidget.count()==0 and\
                self.CoverListWidget.count()==0:
                    self.scale_class.set_zero_len_without_glands()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfShellQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())



