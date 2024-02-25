import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import dxf_base_ui

from config import csv_config
from src.Widgets_Custom.Error import Ui_WidgetError
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox, UI_BaseError

class TerminalUi(dxf_base_ui.DxfQtCommunication):

    def __init__(self):
        super(TerminalUi, self).__init__()
        #ПОЛУЧЕНИЕ ПУТИ ДЛЯ БАЗЫ DXF

        '''СОMBOBOX SHELL'''



    def define_typeof_terminal(self):
        '''Определяем тип клемм по dxf файлу'''
        self.mounttype_terminal_combobox.clear()
        if self.manufacturer_terminal_combobox.currentText() != '' and \
           self.manufacturer_terminal_combobox.currentText() != None:

            manufacturer_terminal = self.manufacturer_terminal_combobox.currentText()
            self.mounttype_terminal_combobox.addItem('')
            self.mounttype_terminal_combobox.addItems(TERMINAL_DB.define_type_of_terminal(
                                                    names_of_terminal=self.terminal_full_names,
                                                    manufacturer= manufacturer_terminal))


