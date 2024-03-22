import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from src.interface_backend import setup_ui

from config import csv_config
from src.gui.py_ui import mainver02
from src.Widgets_Custom.Error import Ui_WidgetError
from src.csv import shell_csv
from src.draw import BOM

class ShellInterface(setup_ui.SetupInterface):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        '''Установка класса для получения информации по оболочкам'''
        self.install_shell_csv()
        self.install_enabled_widgets()

        '''Добавление производителя'''
        self.add_manufacturer_shell_combobox()
        '''Добавление взрывозащиты'''
        self.add_explosion_protections_shell()
        '''КНОПКИ'''
        self.shellButton_leftMenu.clicked.connect(self.set_shell_page)

        '''COMBOBOXES'''
        '''ПРОИЗВОДИТЕЛЬ'''

        self.manufactureComboboxWidget_shellpage.currentTextChanged.connect(self.install_shell_manufacturer_combobox)

        '''ТИП ВЗРЫВОЗАЩИТЫ'''

        self.safefactortypeCombobox_shellpage.currentTextChanged.connect(self.install_shell_explosion_protection_combobox)

        '''СЕРИЯ'''
        self.serialCombobox_shellpage.currentTextChanged.connect(self.set_shell_series)
        self.serialCombobox_shellpage.currentTextChanged.connect(self.install_enabled_size)
        self.serialCombobox_shellpage.currentTextChanged.connect(self.give_size_type)

        '''РАЗМЕР'''
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.set_shell_size)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.set_dict_shell_information)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.set_dict_shell_BOM)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.install_enabled_marking_explosion)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.define_all_marking_explosion_protection)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.install_enabled_gas_mark)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.install_enabled_dust_mark)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.install_enabled_ore_mark)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.give_marking_explosion)

        '''МАРКИРОВКА ВЗРЫВОЗАЩИТЫ'''
        self.gasdustoreComboBox_shellpage.currentTextChanged.connect(self.set_marking_explosion_protection)
        self.gasdustoreComboBox_shellpage.currentTextChanged.connect(self.install_enabled_temrepature)

        '''РАДИО БАТОНЫ'''
        self.gas_mark_RadioButton_shellpage.toggled.connect(self.give_marking_explosion)
        self.dust_mark_RadioButton_shellpage.toggled.connect(self.give_marking_explosion)
        self.ore_mark_RadioButton_shellpage.toggled.connect(self.give_marking_explosion)

        '''ТЕМПЕРАТУРА'''
        self.gas_mark_RadioButton_shellpage.toggled.connect(self.give_T_class_and_maxT)
        self.dust_mark_RadioButton_shellpage.toggled.connect(self.give_T_class_and_maxT)
        self.ore_mark_RadioButton_shellpage.toggled.connect(self.give_T_class_and_maxT)
        self.maxtempLineedit_shellpage_3.editingFinished.connect(self.give_T_class_and_maxT)



    @Qt.pyqtSlot()
    def install_shell_csv(self):
        self.smb_specmash.get_shell_csv_path()
        self.shell_information = shell_csv.Shell_csv(shell_csv_path=self.smb_specmash.shell_csv_path)

    @Qt.pyqtSlot()
    def install_enabled_widgets(self):
        self.serialCombobox_shellpage.setEnabled(False)
        self.sizeCombobox_shellpage.setEnabled(False)
        self.gasdustoreComboBox_shellpage.setEnabled(False)
        self.dust_mark_RadioButton_shellpage.setEnabled(False)
        self.gas_mark_RadioButton_shellpage.setEnabled(False)
        self.ore_mark_RadioButton_shellpage.setEnabled(False)
        self.temperature_class_comboBox_shellpage.setEnabled(False)


    @Qt.pyqtSlot()
    def set_shell_page(self):
        '''Устанавливает при запуске всегда первую страницу StackedWidget '''
        if self.stackedWidget.count() != 0:
            self.stackedWidget.setCurrentIndex(0)

    def add_manufacturer_shell_combobox(self):
        '''Пока поставим производителя только ВЗОР'''
        self.manufactureComboboxWidget_shellpage.clear()
        self.manufactureComboboxWidget_shellpage.addItems(['',*csv_config.SHELL_MANUFACTURER])

    def add_explosion_protections_shell(self):
        '''Установка типа взрывозащиты'''
        self.safefactortypeCombobox_shellpage.clear()
        self.safefactortypeCombobox_shellpage.addItems(['', *csv_config.EXPLOSION_PROTECTION])

    @Qt.pyqtSlot()
    def install_shell_manufacturer_combobox(self):
        self.set_shell_manufacturer()
        if hasattr(self,'shell_manufacturer') and hasattr(self,'shell_explosion_protection'):
            if self.shell_manufacturer != '' and self.shell_explosion_protection != '':
                self.install_enabled_serial()
                self.give_serial_type()


    def set_shell_manufacturer(self):
        self.shell_manufacturer = self.manufactureComboboxWidget_shellpage.currentText()
        self.shell_information.set_manufacturer(manufacturer=self.shell_manufacturer)
    def install_enabled_serial(self):
        # self.serialCombobox_shellpage.clear()
        if hasattr(self, 'shell_manufacturer') and hasattr(self, 'shell_explosion_protection'):
            if self.shell_manufacturer != '' and self.shell_explosion_protection != '':
                self.serialCombobox_shellpage.setEnabled(True)
            else:
                self.serialCombobox_shellpage.setEnabled(False)
        else:
            self.serialCombobox_shellpage.setEnabled(False)
    def give_serial_type(self):
        '''
        Добавляет виды оболочек
        '''
        self.serialCombobox_shellpage.clear()
        self.shell_information.get_unique_series()
        self.serialCombobox_shellpage.addItems(['',*self.shell_information.unique_series])

    @Qt.pyqtSlot()
    def install_shell_explosion_protection_combobox(self):
        self.set_explosion_protection()
        if hasattr(self, 'shell_manufacturer') and hasattr(self, 'shell_explosion_protection'):
            if self.shell_manufacturer != '' and self.shell_explosion_protection != '':
                self.install_enabled_serial()
                self.give_serial_type()

    def set_explosion_protection(self):
        self.shell_explosion_protection = self.safefactortypeCombobox_shellpage.currentText()
        self.shell_information.set_explosion_protection(explosion_protection=self.shell_explosion_protection)

    def set_shell_series(self):
        self.shell_series = self.serialCombobox_shellpage.currentText()
        self.shell_information.set_series(shell_series=self.shell_series)

    @Qt.pyqtSlot()
    def install_enabled_size(self):
        # self.sizeCombobox_shellpage.clear()
        if self.serialCombobox_shellpage.isEnabled():
            if hasattr(self, 'shell_series'):
                if self.shell_series != '':
                    self.sizeCombobox_shellpage.setEnabled(True)
                else:
                    self.sizeCombobox_shellpage.setEnabled(False)
            else:
                self.sizeCombobox_shellpage.setEnabled(False)

    @Qt.pyqtSlot()
    def give_size_type(self):
        self.sizeCombobox_shellpage.clear()
        if self.serialCombobox_shellpage.isEnabled():
            if hasattr(self,'shell_series'):
                if self.shell_series !='':
                    self.shell_information.get_unique_sizes()
                    self.sizeCombobox_shellpage.addItems(['', *self.shell_information.unique_sizes])

    @Qt.pyqtSlot()
    def set_shell_size(self):
        self.shell_size = self.sizeCombobox_shellpage.currentText()
        self.shell_information.set_size(shell_size=self.shell_size)

    @Qt.pyqtSlot()
    def set_dict_shell_information(self):
        if hasattr(self,'shell_size'):
            if self.shell_size != '':
                self.shell_information.set_shell_dict()
                if hasattr(self.shell_information,'shell_dict'):
                    self.shell_dict = self.shell_information.shell_dict

    @Qt.pyqtSlot()
    def set_dict_shell_BOM(self):
        if hasattr(self,'shell_size'):
            if self.shell_size != '':
                self.shell_information.set_shell_dict()
                if hasattr(self.shell_information,'shell_dict'):
                    self.shell_information.set_BOM_shell(BOM_CLASS=BOM.BOM_SHELL())
                    self.shell_information.BOM_shell.get_shell_information(shell_dict=self.shell_dict)
                    self.shell_information.BOM_shell.set_vrpt_name()
                    self.shell_information.BOM_shell.set_fullname()
                    self.shell_information.BOM_shell.set_property()
                    self.shell_information.BOM_shell.set_production_cost()
                    self.shell_information.BOM_shell.set_work_cost()
                    self.shell_information.BOM_shell.give_bom_dict()
                    self.BOM_general.add_bom_list_elements(BOM=self.shell_information.BOM_shell.bom_dict)

    @Qt.pyqtSlot()
    def define_all_marking_explosion_protection(self):
        if hasattr(self,'shell_dict'):
            self.shell_information.define_marking_explosion_protections()
            self.marking_explosion_dict = self.shell_information.marking_dict

    @Qt.pyqtSlot()
    def install_enabled_marking_explosion(self):
        if hasattr(self,'shell_dict'):
            if self.shell_size != '':
                self.gasdustoreComboBox_shellpage.setEnabled(True)
            else:
                self.gasdustoreComboBox_shellpage.setEnabled(False)
        else:
            self.gasdustoreComboBox_shellpage.setEnabled(False)

    @Qt.pyqtSlot()
    def install_enabled_gas_mark(self):
        if hasattr(self,'marking_explosion_dict'):
            if self.shell_size != '':
                if len(self.marking_explosion_dict['gas']) >0:
                    self.gas_mark_RadioButton_shellpage.setEnabled(True)
                else:
                    self.gas_mark_RadioButton_shellpage.setChecked(False)
                    self.gas_mark_RadioButton_shellpage.setEnabled(False)
            else:
                self.gas_mark_RadioButton_shellpage.setChecked(False)
                self.gas_mark_RadioButton_shellpage.setEnabled(False)

    @Qt.pyqtSlot()
    def install_enabled_dust_mark(self):
        if hasattr(self, 'marking_explosion_dict'):
            if self.shell_size != '':
                if len(self.marking_explosion_dict['dust']) > 0:
                    self.dust_mark_RadioButton_shellpage.setEnabled(True)
                else:
                    self.dust_mark_RadioButton_shellpage.setChecked(False)
                    self.dust_mark_RadioButton_shellpage.setEnabled(False)
            else:
                self.dust_mark_RadioButton_shellpage.setChecked(False)
                self.dust_mark_RadioButton_shellpage.setEnabled(False)

    @Qt.pyqtSlot()
    def install_enabled_ore_mark(self):
        if hasattr(self, 'marking_explosion_dict'):
            if self.shell_size != '':
                if len(self.marking_explosion_dict['ore']) > 0:
                    self.ore_mark_RadioButton_shellpage.setEnabled(True)
                else:
                    self.ore_mark_RadioButton_shellpage.setChecked(False)
                    self.ore_mark_RadioButton_shellpage.setEnabled(False)
            else:
                self.ore_mark_RadioButton_shellpage.setChecked(False)
                self.ore_mark_RadioButton_shellpage.setEnabled(False)

    @Qt.pyqtSlot()
    def give_marking_explosion(self):
        '''Добавление типов '''
        self.gasdustoreComboBox_shellpage.clear()
        if hasattr(self,'marking_explosion_dict'):
            if self.gas_mark_RadioButton_shellpage.isChecked():
                self.gasdustoreComboBox_shellpage.addItems(['',*self.marking_explosion_dict['gas']])
            elif self.dust_mark_RadioButton_shellpage.isChecked():
                self.gasdustoreComboBox_shellpage.addItems(['', *self.marking_explosion_dict['dust']])
            elif self.ore_mark_RadioButton_shellpage.isChecked():
                self.gasdustoreComboBox_shellpage.addItems(['', *self.marking_explosion_dict['ore']])

    @Qt.pyqtSlot()
    def set_marking_explosion_protection(self):
        self.marking_explosion_protection = self.gasdustoreComboBox_shellpage.currentText()
        self.shell_information.set_marking_explosion_protection(marking_explosion_protection=
                                                                self.marking_explosion_protection)

    @Qt.pyqtSlot()
    def install_enabled_temrepature(self):
        if hasattr(self, 'marking_explosion_protection'):
            if self.marking_explosion_protection != '':
                self.temperature_class_comboBox_shellpage.setEnabled(True)
            else:
                self.temperature_class_comboBox_shellpage.setEnabled(False)

    @Qt.pyqtSlot()
    def give_T_class_and_maxT(self):
        '''Определяет Т класс в зависимости от указанного температурного диапазона'''
        self.temperature_class_comboBox_shellpage.clear()
        T_class = ['', 'T3', 'T4', 'T5', 'T6']

        def define_deleted_Tclass(max_T: int) -> list:
            if max_T <= 40:
                return ['', 'T3', 'T4', 'T5', 'T6']
            elif max_T <= 55 and max_T > 40:
                return ['', 'T3', 'T4', 'T5']
            elif max_T <= 100 and max_T > 55:
                return ['', 'T3', 'T4']
            elif max_T <= 130 and max_T > 100:
                return ['', 'T3']
            else:
                return ['Не проходит по Т классу']

        if self.gas_mark_RadioButton_shellpage.isChecked():
            self.t_class_widget_shellpage.setEnabled(True)
            self.using_temperatureWidget_shellpage.setEnabled(True)
            self.mintempLabel_shellpage_3.setEnabled(True)
            self.mintempLineEdit_shellpage_3.setEnabled(True)
            self.maxtempLabel_shellpage_3.setEnabled(True)
            self.maxtempLineedit_shellpage_3.setEnabled(True)
            self.t_class_widget_shellpage.setEnabled(True)
            self.using_temperatureLabel_shellpage_3.setText('Температура окружающей среды')
            self.temperature_class_comboBox_shellpage.addItems(
                define_deleted_Tclass(int(self.maxtempLineedit_shellpage_3.text())))
        elif self.dust_mark_RadioButton_shellpage.isChecked():
            self.using_temperatureWidget_shellpage.setEnabled(True)
            self.mintempLabel_shellpage_3.setEnabled(False)
            self.mintempLineEdit_shellpage_3.setEnabled(False)
            self.t_class_widget_shellpage.setEnabled(False)
            self.maxtempLabel_shellpage_3.setEnabled(True)
            self.maxtempLineedit_shellpage_3.setEnabled(True)
            self.using_temperatureLabel_shellpage.setText('Максимальная температура поверхности')
        elif self.ore_mark_RadioButton_shellpage.isChecked():
            self.t_class_widget_shellpage.setEnabled(False)
            self.using_temperatureWidget_shellpage.setEnabled(False)
            self.using_temperatureLabel_shellpage_3.setText(' ')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = ShellInterface()
    welcome_window.show()
    sys.exit(app.exec_())
