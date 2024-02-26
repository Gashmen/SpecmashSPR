import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import dxf_base_ui
from src.terminal import TERMINAL_DB

from config import csv_config
from src.Widgets_Custom.Error import Ui_WidgetError
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox, UI_BaseError

class TerminalUi(dxf_base_ui.DxfQtCommunication):

    def __init__(self):
        super(TerminalUi, self).__init__()
        #ПОЛУЧЕНИЕ ПУТИ ДЛЯ БАЗЫ DXF

        '''СОMBOBOX SHELL'''
        #Перемещение в ComboBox
        self.define_manufacturer_terminal()
        # Получения типа клемм после изменения производителя
        self.manufacturer_terminal_combobox.currentTextChanged.connect(self.define_typeof_terminal)
        # Получение назначения клемм после изменения типа
        self.mounttype_terminal_combobox.currentTextChanged.connect(self.define_appointment_terminal)
        # Получение их сечений, после назначения клеммы
        self.appointment_terminal_combobox.currentTextChanged.connect(self.define_conductorsection_terminal)
        # Добавляем клеммы
        self.add_button_terminal_button.clicked.connect(self.add_terminal)
        # Удаляем клемму
        self.delete_button_teminal_button.clicked.connect(self.delete_terminal)
        # Перемещаем клемму вверх
        self.up_button_terminal.clicked.connect(self.click_up_terminal)
        # Перемещаем клемму вниз
        self.down_button_terminal.clicked.connect(self.click_down_terminal)
        # Добавляем в list widget end_stop and end_plate
        self.end_plate_terminal_button.clicked.connect(self.add_end_plate_terminal)
        self.stop_plate_terminal_button.clicked.connect(self.add_end_stop_terminal)
        # Создаем выходной список, при изменении количества в listwidget
        self.add_button_terminal_listwidget.model().rowsInserted.connect(self.create_list_with_terminals)
        self.add_button_terminal_listwidget.model().rowsRemoved.connect(self.create_list_with_terminals)
    def define_manufacturer_terminal(self):
        '''Определяем производителей клемм по dxf файлу'''
        self.manufacturer_terminal_combobox.clear()
        self.terminal_full_names = TERMINAL_DB.define_names_terminal(doc_dict_blocks=self.base_dxf.doc_dict_blocks)
        self.manufacturer_terminal_combobox.addItem('')
        self.manufacturer_terminal_combobox.addItems(list(TERMINAL_DB.define_manufacturer(self.terminal_full_names)))

    def define_typeof_terminal(self):
        '''Определяем тип клемм по dxf файлу'''
        self.mounttype_terminal_combobox.clear()
        if self.manufacturer_terminal_combobox.currentText() != '' and \
                self.manufacturer_terminal_combobox.currentText() != None:
            manufacturer_terminal = self.manufacturer_terminal_combobox.currentText()
            self.mounttype_terminal_combobox.addItem('')
            self.mounttype_terminal_combobox.addItems(TERMINAL_DB.define_type_of_terminal(
                names_of_terminal=self.terminal_full_names,
                manufacturer=manufacturer_terminal))

    def define_appointment_terminal(self):
        '''Добавляем в Combobox назначение клеммы в соответсвии с типом и базой в dxf L,N,PE'''
        self.appointment_terminal_combobox.clear()
        if self.mounttype_terminal_combobox.currentText() != '' and \
                self.mounttype_terminal_combobox.currentText() != None:
            manufacturer_terminal = self.manufacturer_terminal_combobox.currentText()
            type_of_terminal = self.mounttype_terminal_combobox.currentText()
            self.appointment_terminal_combobox.addItem('')
            self.appointment_terminal_combobox.addItems(TERMINAL_DB.define_appointment_of_terminal(
                names_of_terminal=self.terminal_full_names,
                manufacturer=manufacturer_terminal,
                type_of_terminal=type_of_terminal
            ))

    def define_conductorsection_terminal(self):
        # НАДО СДЕЛАТЬ СОРТИРОВКУ ПО ДИАММЕТРАМ

        self.conductorsection_terminal_combobox.clear()
        if self.appointment_terminal_combobox.currentText() != '' and \
                self.appointment_terminal_combobox.currentText() != None:
            manufacturer_terminal = self.manufacturer_terminal_combobox.currentText()
            type_of_terminal = self.mounttype_terminal_combobox.currentText()
            appointment_of_terminal = self.appointment_terminal_combobox.currentText()
            self.conductorsection_terminal_combobox.addItem('')
            self.conductorsection_terminal_combobox.addItems(TERMINAL_DB.define_conductorsection_terminal(
                names_of_terminal=self.terminal_full_names,
                manufacturer=manufacturer_terminal,
                type_of_terminal=type_of_terminal,
                appointment_of_terminal=appointment_of_terminal
            ))

    def add_terminal(self):
        '''Добавляет Terminal в add_button_terminal_listwidget'''
        if self.manufacturer_terminal_combobox.currentText() and \
                self.mounttype_terminal_combobox.currentText() and \
                self.appointment_terminal_combobox.currentText() and \
                self.conductorsection_terminal_combobox.currentText():
            if self.count_terminal_spinbox.text() != 0:
                manufacturer_terminal = self.manufacturer_terminal_combobox.currentText()
                type_of_terminal = self.mounttype_terminal_combobox.currentText()
                appointment_of_terminal = self.appointment_terminal_combobox.currentText()
                conductorsectionvalue_of_terminal = self.conductorsection_terminal_combobox.currentText()
                terminal = f'{manufacturer_terminal}_{type_of_terminal}_{appointment_of_terminal}_{conductorsectionvalue_of_terminal}'
                self.add_button_terminal_listwidget.addItems([terminal] * int(self.count_terminal_spinbox.text()))

    def delete_terminal(self):
        '''Удаляет терминал из ListWidget'''
        rowIndex = self.add_button_terminal_listwidget.currentRow()
        currentItem = self.add_button_terminal_listwidget.takeItem(rowIndex)

    def click_up_terminal(self):
        '''Поднятие ввода наверх для составления последовательности'''
        rowIndex = self.add_button_terminal_listwidget.currentRow()
        currentItem = self.add_button_terminal_listwidget.takeItem(rowIndex)
        self.add_button_terminal_listwidget.insertItem(rowIndex - 1, currentItem)
        self.add_button_terminal_listwidget.setCurrentRow(rowIndex - 1)

    def click_down_terminal(self):
        '''Поднятия кабельного ввода вниз для составления последовательности'''
        rowIndex = self.add_button_terminal_listwidget.currentRow()
        currentItem = self.add_button_terminal_listwidget.takeItem(rowIndex)
        self.add_button_terminal_listwidget.insertItem(rowIndex + 1, currentItem)
        self.add_button_terminal_listwidget.setCurrentRow(rowIndex + 1)

    def add_end_stop_terminal(self):
        '''Добавления концевого стопора'''
        self.add_button_terminal_listwidget.addItem('Концевой стопор')

    def add_end_plate_terminal(self):
        '''Добавления концевая пластина'''
        self.add_button_terminal_listwidget.addItem('Концевая пластина')

    def create_list_with_terminals(self):
        '''Создаем выходной список по элементам которые есть, для дальнейшего построения в dxf '''
        if self.add_button_terminal_listwidget.count() != 0:
            self.list_from_terminal_listwidget = [self.add_button_terminal_listwidget.item(i).text()
                                                  for i in range(0, self.add_button_terminal_listwidget.count())]

            self.list_with_terminals = list(
                map(TERMINAL_DB.change_name_from_to, self.list_from_terminal_listwidget))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = TerminalUi()
    welcome_window.show()
    sys.exit(app.exec_())







