import ezdxf
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import dxf_gland #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ
from src.draw.terminal import dxf_terminal

class DxfTerminalQtCommunication(dxf_gland.DxfGlandQtCommunication):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        # Создаем выходной список, при изменении количества в listwidget
        self.add_button_terminal_listwidget.model().rowsInserted.connect(self.set_dict_dxf_terminals)
        self.add_button_terminal_listwidget.model().rowsRemoved.connect(self.set_dict_dxf_terminals)

        self.add_button_terminal_listwidget.model().rowsInserted.connect(self.check_possible_to_add_terminals)
        self.add_button_terminal_listwidget.model().rowsRemoved.connect(self.check_possible_to_add_terminals)

        self.Autohelper.clicked.connect(self.create_terminals_dxf_after_DIN_REYKA)
         # Тест, потом удалить

    def set_dict_dxf_terminals(self):
        self.list_terminal_dxf = list()
        if hasattr(self,'list_with_terminals'):
            if len(self.list_with_terminals) >0:
                for terminal_dxf_name in self.list_with_terminals:
                    current_terminal = dxf_terminal.TerminalDxf()
                    current_terminal.set_terminal_dxf_name(terminal_dxf_name=terminal_dxf_name)
                    current_terminal.set_doc_base(self.base_dxf.doc_base)
                    current_terminal.calculate_horizontal_length()
                    self.list_terminal_dxf.append(current_terminal)

    def check_possible_to_add_terminals(self):
        if hasattr(self,'list_terminal_dxf'):
            if len(self.list_terminal_dxf) >0:
                summary_terminal_len = dxf_terminal.define_len_terminals(list_terminal_dxf=self.list_terminal_dxf)
                if summary_terminal_len > 0.95 * self.withoutcapside_block.din_length:
                    self.list_terminal_dxf.clear()
                    self.list_with_terminals.clear()
                    self.add_button_terminal_listwidget.clear()
                    QMessageBox.critical(self, "Справка",
                                         f"Не поместяться все клеммы",
                                         QMessageBox.Ok)

    def delete_terminal_in_withoutcapside(self):
        if len(self.list_used_blocks_terminals) >0:
            for terminal_insert in self.list_used_blocks_terminals:
                self.base_dxf.doc_base.blocks[self.withoutcapside_block.shell_side_name].delete_entity(terminal_insert)
            self.list_used_blocks_terminals.clear()

    def create_terminals_dxf_after_DIN_REYKA(self):
        if hasattr(self,'list_terminal_dxf'):
            if len(self.list_terminal_dxf) >0:

                summary_terminal_len = dxf_terminal.define_len_terminals(list_terminal_dxf=self.list_terminal_dxf)
                if summary_terminal_len <= 0.95 * self.withoutcapside_block.din_length:

                    din_reyka_insert_coordinate = [0,0]
                    x_first_coordinate = din_reyka_insert_coordinate[0] - summary_terminal_len/2
                    y_first_coordinate = din_reyka_insert_coordinate[1]

                    self.delete_terminal_in_withoutcapside()

                    for terminal_dxf in self.list_terminal_dxf:
                        # Работаем с hatch
                        # block_terminal = doc_after_import.blocks[terminal_name]
                        # set_hatch_before_entity(block=block_terminal)

                        len_terminal = terminal_dxf.horizontal_length
                        x_insert = x_first_coordinate + len_terminal / 2
                        y_insert = y_first_coordinate
                        terminal_insert = self.base_dxf.doc_base.blocks[self.withoutcapside_block.shell_side_name].add_blockref(
                                                                         name = terminal_dxf.terminal_dxf_name,
                                                                         insert=(x_insert, y_insert))
                        x_first_coordinate += len_terminal
                        self.list_used_blocks_terminals.append(terminal_insert)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfTerminalQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())