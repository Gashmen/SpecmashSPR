import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox

from src.interface_backend import shell_ui

from config import csv_config
from src.Widgets_Custom.Error import Ui_WidgetError
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox, UI_BaseError


class GlandInterface(shell_ui.ShellInterface):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        self.glands_on_sides_dict = {"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}

        self.install_gland_csv()
        self.gland_information.set_main_dict(main_path=self.gland_information.gland_csv_path)

        '''Установка разрешения видимости'''
        self.set_gland_enabled()
        '''ОБНОВЛЕНИЕ ВИДЖЕТОВ, УСТАНОВКА НОВОГО COMBOBOX WIDGET'''
        self.improve_choose_widget()

        '''RADIO BUTTONS'''
        self.gland_from_allRadioButton.toggled.connect(self.install_choose_gland_widget_enabled)
        self.gland_from_propertiesRadioButton.toggled.connect(self.install_gland_designation_widget_enabled)
        self.gland_from_allRadioButton.toggled.connect(self.give_gland_all_names_vzor)
        self.gland_from_propertiesRadioButton.toggled.connect(self.give_gland_all_names_vzor)

        self.VZradioButton.toggled.connect(self.add_vz_in_gland)
        self.VZeradioButton.toggled.connect(self.add_vz_in_gland)

        '''BUTTONS'''
        self.inputsButton_leftMenu.clicked.connect(self.set_gland_page)

        # Добавление имен в siteA

        self.addButton_2.clicked.connect(self.add_gland_side_A)
        self.addButton_2.clicked.connect(self.check_to_add_biggest_gland_side_A)
        self.addButton_2.clicked.connect(self.check_to_add_all_area_glands_side_A)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_one_row_A)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_two_row_A)
        # Добавление имен в siteB
        self.addButton_2.clicked.connect(self.add_gland_side_B)
        self.addButton_2.clicked.connect(self.check_to_add_biggest_gland_side_B)
        self.addButton_2.clicked.connect(self.check_to_add_all_area_glands_side_B)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_one_row_B)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_two_row_B)
        # Добавление имен в siteV
        self.addButton_2.clicked.connect(self.add_gland_side_V)
        self.addButton_2.clicked.connect(self.check_to_add_biggest_gland_side_V)
        self.addButton_2.clicked.connect(self.check_to_add_all_area_glands_side_V)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_one_row_V)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_two_row_V)
        # Добавление имен в siteG
        self.addButton_2.clicked.connect(self.add_gland_side_G)
        self.addButton_2.clicked.connect(self.check_to_add_biggest_gland_side_G)
        self.addButton_2.clicked.connect(self.check_to_add_all_area_glands_side_G)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_one_row_G)
        self.addButton_2.clicked.connect(self.check_to_possible_to_create_all_glands_in_two_row_G)
        # Добавление имен в Cover
        self.addButton_2.clicked.connect(self.add_gland_side_Cover)
        # Обнуление SpinBox
        self.addButton_2.clicked.connect(self.clear_ABVG_spinbox_afted_add_button)

        '''COMBOBOX'''
        self.vzorglandcomboBox.currentTextChanged.connect(self.set_current_gland_from_all_names)

        self.gland_designationcomboBox.currentTextChanged.connect(self.set_gland_designation)
        self.gland_designationcomboBox.currentTextChanged.connect(self.install_gland_material_enabled)

        self.gland_materialcomboBox.currentTextChanged.connect(self.set_gland_material)
        self.gland_materialcomboBox.currentTextChanged.connect(self.install_gland_cabletype_enabled)

        self.gland_cabletypecomboBox.currentTextChanged.connect(self.set_gland_cabletype)
        self.gland_cabletypecomboBox.currentTextChanged.connect(self.install_gland_threadtype_enabled)

        self.gland_threadtypecomboBox.currentTextChanged.connect(self.set_gland_thread)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.install_gland_ckeckdiam_enabled)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.install_gland_g_npt_enabled)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.install_gland_options_enabled)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.set_dict_for_calculate_gland_diam)


        self.gland_additionalmarkingcomboBox.currentTextChanged.connect(self.set_gland_additional_marking)
        self.gland_additionalmarkingcomboBox.currentTextChanged.connect(self.install_gland_type_mr_marking_enabled)
        self.gland_additionalmarkingcomboBox.currentTextChanged.connect(self.give_gland_tube_mr_modification)

        self.gland_tube_mr_markingcomboBox.currentTextChanged.connect(self.set_gland_tube_mr_modification)
        self.gland_tube_mr_markingcomboBox.currentTextChanged.connect(self.set_key_gland)

        '''LINE EDIT'''
        self.gland_checkdiam_minlineedit.editingFinished.connect(self.set_min_diam_qt)
        self.gland_checkdiam_minlineedit.editingFinished.connect(self.set_max_diam_qt)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.set_max_diam_qt)

        self.gland_checkdiam_minlineedit.editingFinished.connect(self.calculate_diam_modification_for_M_thread)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.calculate_diam_modification_for_M_thread)

        self.gland_checkdiam_minlineedit.editingFinished.connect(self.set_gland_without_modification)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.set_gland_without_modification)

        self.gland_checkdiam_minlineedit.editingFinished.connect(self.install_gland_additional_marking_enabled)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.install_gland_additional_marking_enabled)

        '''CHECKBOX'''
        self.protectiveCoverCheckBox.stateChanged.connect(self.add_ch_in_gland)
        self.groovedwasherCheckBox.stateChanged.connect(self.add_gsh_in_gland)
        self.locknutCheckBox.stateChanged.connect(self.add_kg_in_gland)
        self.fluttedWasherCheckBox.stateChanged.connect(self.add_kz_in_gland)

        '''Удаление и перемещение кнопками '''
        # Удалить все
        self.deleteallButton_2.clicked.connect(self.clear_all_list_widget)

        # Кнопка Up
        self.sideAupButton.clicked.connect(self.click_up_button_A)
        self.sideBupButton.clicked.connect(self.click_up_button_B)
        self.sideVupButton.clicked.connect(self.click_up_button_V)
        self.sideGupButton.clicked.connect(self.click_up_button_G)
        self.CoverupButton.clicked.connect(self.click_up_button_cover)

        # Кнопка Down
        self.sideAdownButton.clicked.connect(self.click_down_button_A)
        self.sideBdownButton.clicked.connect(self.click_down_button_B)
        self.sideVdownButton.clicked.connect(self.click_down_button_V)
        self.sideGdownButton.clicked.connect(self.click_down_button_G)
        self.CoverdownButton.clicked.connect(self.click_down_button_cover)

        # Кнопка delete
        self.sideAdeleteButton.clicked.connect(self.click_delete_button_A)
        self.sideBdeleteButton.clicked.connect(self.click_delete_button_B)
        self.sideVdeleteButton.clicked.connect(self.click_delete_button_V)
        self.sideGdeleteButton.clicked.connect(self.click_delete_button_G)
        self.CoverdeleteButton.clicked.connect(self.click_delete_button_cover)


    def add_manufacturer_inputs_combobox(self):
        '''Пока поставим производителя только ВЗОР'''
        self.manufacturerInputsComboBox.clear()
        self.manufacturerInputsComboBox.addItems(csv_config.GLAND_MANUFACTURER)

    def improve_choose_widget(self):
        '''ИЗМЕНЕНИЕ КЛАССА COMBOBOX WIDGET'''
        self.vzorglandcomboBox.deleteLater()
        self.vzorglandcomboBox = ExtendedCombobox.ExtendedComboBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vzorglandcomboBox.sizePolicy().hasHeightForWidth())
        self.vzorglandcomboBox.setSizePolicy(sizePolicy)
        self.vzorglandcomboBox.setObjectName("vzorglandcomboBox")
        self.verticalLayout_14.addWidget(self.vzorglandcomboBox)

    @Qt.pyqtSlot()
    def set_gland_page(self):
        '''Устанавливает 1 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 5:
            self.stackedWidget.setCurrentIndex(5)

    def install_gland_csv(self):
        self.smb_specmash.get_gland_csv_path()

        self.gland_information = gland_csv.GlandMainDictQt(gland_csv_path=self.smb_specmash.gland_csv_path)

    def set_gland_enabled(self):
        '''Поставить disabled изначально'''
        self.b_vzorglandWidget.setEnabled(False)
        self.c_gland_designationWidget.setEnabled(False)
        self.d_gland_materialWidget.setEnabled(False)
        self.e_gland_cabletypeWidget.setEnabled(False)
        self.f_gland_threadtypeWidget.setEnabled(False)
        self.g_gland_checkdiamWidget.setEnabled(False)
        self.h_gland_mr_or_tubeWidget.setEnabled(False)
        self.i_gland_additionalmarkingWidget.setEnabled(False)
        self.j_gland_tube_mr_markingWidget.setEnabled(False)
        self.k_gland_optionsWidget.setEnabled(False)

    @Qt.pyqtSlot()
    def install_choose_gland_widget_enabled(self):
        if self.gland_from_allRadioButton.isChecked():
            self.b_vzorglandWidget.setEnabled(True)
        else:
            self.b_vzorglandWidget.setEnabled(False)

    @Qt.pyqtSlot()
    def give_gland_all_names_vzor(self):
        self.vzorglandcomboBox.clear()
        if self.gland_from_allRadioButton.isChecked():
            self.gland_information.get_all_glands()
            self.vzorglandcomboBox.addItems(['',*list(self.gland_information.gland_all_names.keys())])

    @Qt.pyqtSlot()
    def set_current_gland_from_all_names(self):
        if self.vzorglandcomboBox.isEnabled():
            if self.vzorglandcomboBox.count() !=0:
                if self.vzorglandcomboBox.currentText() != '':
                    shell_name = self.vzorglandcomboBox.currentText()
                    if shell_name in self.gland_information.gland_all_names:
                        self.key_gland = self.gland_information.gland_all_names[shell_name]

    @Qt.pyqtSlot()
    def install_gland_designation_widget_enabled(self):
        if self.gland_from_propertiesRadioButton.isChecked():
            self.c_gland_designationWidget.setEnabled(True)
            self.give_gland_designation()
        else:
            self.c_gland_designationWidget.setEnabled(False)
            self.gland_designationcomboBox.clear()


    def give_gland_designation(self):
        if self.c_gland_designationWidget.isEnabled():
            self.gland_designationcomboBox.clear()
            self.gland_information.get_unique_designation()
            self.gland_designationcomboBox.addItems(['',*self.gland_information.gland_unique_designation])

    @Qt.pyqtSlot()
    def set_gland_designation(self):
        self.gland_designation = self.gland_designationcomboBox.currentText()
        self.gland_information.set_gland_designation(gland_designation=self.gland_designation)

    @Qt.pyqtSlot()
    def install_gland_material_enabled(self):
        if hasattr(self, 'gland_designation'):
            if self.gland_designation == 'Кабельный ввод':
                self.d_gland_materialWidget.setEnabled(True)
                self.give_gland_material()
            else:
                self.d_gland_materialWidget.setEnabled(False)
        else:
            self.d_gland_materialWidget.setEnabled(False)

    @Qt.pyqtSlot()
    def give_gland_material(self):
        if self.d_gland_materialWidget.isEnabled():
            self.gland_materialcomboBox.clear()
            self.gland_information.get_unique_material()
            self.gland_materialcomboBox.addItems(['',*self.gland_information.gland_unique_material])

    @Qt.pyqtSlot()
    def set_gland_material(self):
        self.gland_material = self.gland_materialcomboBox.currentText()
        self.gland_information.set_gland_material(gland_material=self.gland_material)

    @Qt.pyqtSlot()
    def install_gland_cabletype_enabled(self):
        if hasattr(self,'gland_material'):
            if self.gland_material != '':
                self.e_gland_cabletypeWidget.setEnabled(True)
                self.give_gland_calbetype()
            else:
                self.e_gland_cabletypeWidget.setEnabled(False)
        else:
            self.e_gland_cabletypeWidget.setEnabled(False)

    def give_gland_calbetype(self):
        if self.e_gland_cabletypeWidget.isEnabled():
            self.gland_cabletypecomboBox.clear()
            self.gland_information.get_unique_cable_type()
            self.gland_cabletypecomboBox.addItems(['',*self.gland_information.gland_unique_cable_type])

    @Qt.pyqtSlot()
    def set_gland_cabletype(self):
        self.gland_cabletype = self.gland_cabletypecomboBox.currentText()
        self.gland_information.set_cable_type(gland_cable_type=self.gland_cabletype)

    def install_gland_threadtype_enabled(self):
        if hasattr(self,'gland_cabletype'):
            if self.gland_cabletype != '':
                self.f_gland_threadtypeWidget.setEnabled(True)
                self.give_gland_threadtype()
            else:
                self.f_gland_threadtypeWidget.setEnabled(False)
        else:
            self.f_gland_threadtypeWidget.setEnabled(False)

    def give_gland_threadtype(self):
        if self.f_gland_threadtypeWidget.isEnabled():
            self.gland_threadtypecomboBox.clear()
            self.gland_information.get_unique_thread()
            self.gland_threadtypecomboBox.addItems(['',*self.gland_information.gland_unique_thread])

    @Qt.pyqtSlot()
    def set_gland_thread(self):
        self.gland_threadtype = self.gland_threadtypecomboBox.currentText()
        self.gland_information.set_gland_thread(gland_thread=self.gland_threadtype)

    @Qt.pyqtSlot()
    def install_gland_ckeckdiam_enabled(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype == 'М':
                self.g_gland_checkdiamWidget.setEnabled(True)
            else:
                self.g_gland_checkdiamWidget.setEnabled(False)
        else:
            self.g_gland_checkdiamWidget.setEnabled(False)

    def set_min_diam_qt(self):
        if self.g_gland_checkdiamWidget.isEnabled():
            if self.gland_checkdiam_minlineedit.text() != '':
                min_diam_qt = gland_csv.set_correct_number(number=self.gland_checkdiam_minlineedit.text())
                if min_diam_qt <0:
                    self.gland_checkdiam_minlineedit.setText('0')
                    min_diam_qt = 0
                self.min_diam_qt =min_diam_qt

    def set_max_diam_qt(self):
        if self.g_gland_checkdiamWidget.isEnabled():
            if self.gland_checkdiam_maxlineedit.text() != '':
                max_diam_qt = gland_csv.set_correct_number(number=self.gland_checkdiam_maxlineedit.text())
                if max_diam_qt <0:
                    self.gland_checkdiam_maxlineedit.setText(self.gland_checkdiam_minlineedit.text())
                    max_diam_qt = 0
                if self.gland_checkdiam_minlineedit.text() != '':
                    min_diam_qt = gland_csv.set_correct_number(number=self.gland_checkdiam_minlineedit.text())
                    if max_diam_qt < min_diam_qt:
                        max_diam_qt = min_diam_qt
                        self.gland_checkdiam_maxlineedit.setText(self.gland_checkdiam_minlineedit.text())
                self.max_diam_qt = max_diam_qt

    @Qt.pyqtSlot()
    def install_gland_g_npt_enabled(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype == 'NPT' or self.gland_threadtype == 'G':
                self.h_gland_mr_or_tubeWidget.setEnabled(True)
            else:
                self.h_gland_mr_or_tubeWidget.setEnabled(False)
        else:
            self.h_gland_mr_or_tubeWidget.setEnabled(False)

    @Qt.pyqtSlot()
    def set_dict_for_calculate_gland_diam(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype != '':
                self.gland_information.set_dict_for_calculate_gland_diam()

    def install_gland_additional_marking_enabled(self):
        if hasattr(self.gland_information, 'dict_for_choose_modification_cable'):
            if self.gland_information.dict_for_choose_modification_cable != {}:
                self.i_gland_additionalmarkingWidget.setEnabled(True)
            else:
                self.i_gland_additionalmarkingWidget.setEnabled(False)
        else:
            self.i_gland_additionalmarkingWidget.setEnabled(False)

    def calculate_diam_modification_for_M_thread(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype == 'М':
                if self.gland_checkdiam_minlineedit.text() !='' and self.gland_checkdiam_maxlineedit.text() !='':
                    if hasattr(self,'min_diam_qt') and hasattr(self,'max_diam_qt'):
                        self.gland_information.give_possible_glands_for_calculate(min_diam_from_qt=self.min_diam_qt,
                                                                                  max_diam_from_qt=self.max_diam_qt)
                        #На выходе self.dict_for_choose_modification_cable со значениями тех ключей и данных по вводам
                        #Которые по диаметру проходят
                        self.give_gland_additional_marking()

    def set_gland_without_modification(self):
        if hasattr(self.gland_information, 'dict_for_choose_modification_cable'):
            self.gland_information.set_gland_without_modification_tube_mr()
            self.gland = gland_csv.CableGlandInformation(
                gland_dict=self.gland_information.gland_main_dict[self.gland_information.key_gland])

    def give_gland_additional_marking(self):
        self.gland_additionalmarkingcomboBox.clear()
        if hasattr(self.gland_information, 'dict_for_choose_modification_cable'):
            if self.gland_information.dict_for_choose_modification_cable != {}:
                self.gland_information.give_modification_for_calculated_diam()
                if self.gland_information.list_with_modifications_name != []:
                    self.gland_additionalmarkingcomboBox.addItems(
                        ['',*self.gland_information.list_with_modifications_name])

    @Qt.pyqtSlot()
    def set_gland_additional_marking(self):
        if self.i_gland_additionalmarkingWidget.isEnabled():
            if self.gland_additionalmarkingcomboBox.count() != 0:
                if self.gland_additionalmarkingcomboBox.currentText() != '':
                    self.gland_additionalmarking = self.gland_additionalmarkingcomboBox.currentText()
                    self.gland_information.set_gland_additional_marking(
                        gland_additional_marking=self.gland_additionalmarking
                    )

    @Qt.pyqtSlot()
    def install_gland_type_mr_marking_enabled(self):
        if self.gland_additionalmarkingcomboBox.isEnabled():
            if self.gland_additionalmarkingcomboBox.currentText() != '':
                self.j_gland_tube_mr_markingWidget.setEnabled(True)
            else:
                self.j_gland_tube_mr_markingWidget.setEnabled(False)
        else:
            self.j_gland_tube_mr_markingWidget.setEnabled(False)

    @Qt.pyqtSlot()
    def give_gland_tube_mr_modification(self):
        self.gland_tube_mr_markingcomboBox.clear()
        if self.gland_additionalmarkingcomboBox.isEnabled():
            if self.gland_additionalmarkingcomboBox.currentText() != '':
                self.gland_information.get_uniqie_tube_mr_modification()
                self.gland_tube_mr_markingcomboBox.addItems(['',*self.gland_information.unique_tube_mr_modification])
                if self.gland_information.gland_additional_marking == 'МР':
                    self.gland_tube_mr_markinglabel.setText('Металлорукав')
                elif self.gland_information.gland_additional_marking == 'Т':
                    self.gland_tube_mr_markinglabel.setText('Трубная')

    def set_gland_tube_mr_modification(self):
        if self.gland_tube_mr_markingcomboBox.isEnabled():
            if self.gland_tube_mr_markingcomboBox.currentText() != '':
                self.gland_tube_mr_modification = self.gland_tube_mr_markingcomboBox.currentText()
                self.gland_information.set_gland_tube_mr_modification(
                    gland_tube_mr_modification= self.gland_tube_mr_modification)

    @Qt.pyqtSlot()
    def set_key_gland(self):
        '''Установка ключа кабельнного ввода при выборе модификаций'''
        if hasattr(self,'gland_tube_mr_modification'):
            if self.gland_tube_mr_markingcomboBox.currentText() != '':
                    self.gland_information.set_gland()
                    self.key_gland = self.gland_information.key_gland

    @Qt.pyqtSlot()
    def install_gland_options_enabled(self):
        '''Установка возможности получения опций для кабельнного ввода'''
        if self.i_gland_additionalmarkingWidget.isEnabled() or self.h_gland_mr_or_tubeWidget.isEnabled():
            self.k_gland_optionsWidget.setEnabled(True)
            self.set_vz_radiobutton()
        else:
            self.k_gland_optionsWidget.setEnabled(False)

    @Qt.pyqtSlot()
    def set_vz_radiobutton(self):
        self.VZeradioButton.setChecked(False)
        self.VZradioButton.setChecked(False)

        if self.k_gland_optionsWidget.isEnabled():
            if hasattr(self,'shell_explosion_protection'):
                if self.shell_explosion_protection == 'Exe':
                    self.VZeradioButton.setChecked(True)
                    self.VZradioButton.setChecked(False)
                else:
                    self.VZeradioButton.setChecked(False)
                    self.VZradioButton.setChecked(True)
        else:
            self.VZeradioButton.setChecked(False)
            self.VZradioButton.setChecked(False)

    def add_vz_in_gland(self):
        '''Добавляет в класс кабельного ввода аттрибут о наличии ВЗ-ВЗ или ВЗ-ВЗе'''
        if hasattr(self,'gland'):
            if self.VZradioButton.isChecked():
                self.gland.vz_vz = True
                self.gland.vz_vze = False
            if self.VZeradioButton.isChecked():
                self.gland.vz_vz = False
                self.gland.vz_vze = True

    def add_ch_in_gland(self):
        '''Добавляет защитных кожух в self.gland'''
        if hasattr(self, 'gland'):
            if self.protectiveCoverCheckBox.isChecked():
                self.gland.ch = True
            else:
                self.gland.ch = False

    def add_gsh_in_gland(self):
        '''Добавляет рифленную шайбу в self.gland'''
        if hasattr(self, 'gland'):
            if self.groovedwasherCheckBox.isChecked():
                self.gland.gsh = True
            else:
                self.gland.gsh = False

    def add_kg_in_gland(self):
        '''Добавляет контргайку в self.gland'''
        if hasattr(self, 'gland'):
            if self.locknutCheckBox.isChecked():
                self.gland.kg = True
            else:
                self.gland.kg = False

    def add_kz_in_gland(self):
        '''Добавляет кольцо заземления в self.gland'''
        if hasattr(self,'gland'):
            if self.fluttedWasherCheckBox.isChecked():
                self.gland.kz = True
            else:
                self.gland.kz = False

    @Qt.pyqtSlot()
    def add_options_to_gland(self):
        if hasattr(self,'gland'):
            self.add_vz_in_gland()
            self.add_ch_in_gland()
            self.add_gsh_in_gland()
            self.add_kg_in_gland()
            self.add_kz_in_gland()

    @Qt.pyqtSlot()
    def add_gland_side_A(self):
        if hasattr(self,'key_gland'):
            if self.siteASpinBox_2.text() != '0':
                for _ in range(0, int(self.siteASpinBox_2.text())):
                    self.gland = gland_csv.CableGlandInformation(
                        gland_dict=self.gland_information.gland_main_dict[self.key_gland])
                    self.add_options_to_gland()
                    self.gland.side = 'upside'
                    self.glands_on_sides_dict['А'].append(self.gland)
                    self.sideAListWidget.addItem(self.gland.gland_russian_name)
                    if self.base_dxf.check_gland(gland_translite_name=self.gland.gland_dxf_name):
                        continue
                    else:
                        QMessageBox.critical(self, "Ошибка",
                                             f"{self.gland.gland_russian_name} не добавлен в базу DXF",
                                             QMessageBox.Ok)
    @Qt.pyqtSlot()
    def check_to_add_biggest_gland_side_A(self):
        if hasattr(self, 'upside_block'):
            self.upside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.upside_block.check_possible_to_add_biggest_gland() == False:
                biggest_cable_gland = sorted(self.glands_on_sides_dict['А'], key=lambda x:x.diametr,reverse=True)[0]
                QMessageBox.critical(self, "Ошибка",
                                     f"{biggest_cable_gland.gland_russian_name} не помещается кабельный ввод на сторону А",
                                     QMessageBox.Ok)
                self.sideAListWidget.clear()
                self.glands_on_sides_dict['А'].clear()
                self.upside_block.glands_on_sides_dict['А'].clear()

    @Qt.pyqtSlot()
    def check_to_add_all_area_glands_side_A(self):
        if hasattr(self, 'upside_block'):
            self.upside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.upside_block.check_possible_to_add_all_gland() == False:
                QMessageBox.critical(self, "Ошибка",
                                     f"Невозможно поместить эти кабельные вводы",
                                     QMessageBox.Ok)
                self.sideAListWidget.clear()
                self.glands_on_sides_dict['А'].clear()
                self.upside_block.glands_on_sides_dict['А'].clear()

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_one_row_A(self):
        if hasattr(self, 'upside_block'):
            self.upside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.upside_block.check_possible_to_add_in_one_row() == False:
                QMessageBox.critical(self, "Справка",
                                     f"На сторону А в один ряд НЕ помещаются кабельные вводы",
                                     QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Справка",
                                     f"На сторону А в один ряд ПОМЕЩАЮТСЯ кабельные вводы",
                                     QMessageBox.Ok)

                # self.sideAListWidget.clear()
                # self.glands_on_sides_dict['А'].clear()
                # self.upside_block.glands_on_sides_dict['А'].clear()

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_two_row_A(self):
        if hasattr(self, 'upside_block'):
            self.upside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if hasattr(self.upside_block,'one_row_check'):
                # if self.upside_block.one_row_check.status_add_in_one_row == False:
                    try:
                         self.upside_block.calculate_coordinates_glands_two_row()
                         if self.upside_block.list_glands != []:
                             QMessageBox.critical(self, "Справка",
                                                  f"Невозможно добавить {[_.gland_russian_name for _ in self.upside_block.list_glands]}",
                                                  QMessageBox.Ok)
                    except:
                        QMessageBox.critical(self, "Справка",
                                             f"Невозможно создать в два ряда",
                                             QMessageBox.Ok)
                        self.sideAListWidget.clear()
                        self.glands_on_sides_dict['А'].clear()
                        self.upside_block.glands_on_sides_dict['А'].clear()

    @Qt.pyqtSlot()
    def add_gland_side_B(self):
        if hasattr(self,'key_gland'):
            if self.siteBSpinBox_2.text() != '0':
                for _ in range(0, int(self.siteBSpinBox_2.text())):
                    self.gland = gland_csv.CableGlandInformation(
                        gland_dict=self.gland_information.gland_main_dict[self.key_gland])
                    self.add_options_to_gland()
                    self.gland.side = 'rightside'
                    self.glands_on_sides_dict['Б'].append(self.gland)
                    self.sideBListWidget.addItem(self.gland.gland_russian_name)

    @Qt.pyqtSlot()
    def check_to_add_biggest_gland_side_B(self):
        if hasattr(self, 'rightside_block'):
            self.rightside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.rightside_block.check_possible_to_add_biggest_gland() == False:
                biggest_cable_gland = self.glands_on_sides_dict['Б'][0]
                QMessageBox.critical(self, "Ошибка",
                                     f"{biggest_cable_gland.gland_russian_name} не помещается кабельный ввод на сторону Б",
                                     QMessageBox.Ok)
                self.sideBListWidget.clear()
                self.glands_on_sides_dict['Б'].clear()
                self.rightside_block.glands_on_sides_dict['Б'].clear()

    @Qt.pyqtSlot()
    def check_to_add_all_area_glands_side_B(self):
        if hasattr(self, 'rightside_block'):
            self.rightside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.rightside_block.check_possible_to_add_all_gland() == False:
                QMessageBox.critical(self, "Ошибка",
                                     f"Невозможно поместить эти кабельные вводы",
                                     QMessageBox.Ok)
                self.sideBListWidget.clear()
                self.glands_on_sides_dict['Б'].clear()
                self.rightside_block.glands_on_sides_dict['Б'].clear()

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_one_row_B(self):
        if hasattr(self, 'rightside_block'):
            self.rightside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.rightside_block.check_possible_to_add_in_one_row() == False:
                QMessageBox.critical(self, "Справка",
                                     f"На сторону Б в один ряд НЕ помещаются кабельные вводы",
                                     QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Справка",
                                     f"На сторону Б в один ряд ПОМЕЩАЮТСЯ кабельные вводы",
                                     QMessageBox.Ok)

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_two_row_B(self):
        if hasattr(self, 'rightside_block'):
            self.rightside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if hasattr(self.rightside_block,'one_row_check'):
                # if self.rightside_block.one_row_check.status_add_in_one_row == False:
                    try:
                         self.rightside_block.calculate_coordinates_glands_two_row()
                         if self.rightside_block.list_glands != []:
                             QMessageBox.critical(self, "Справка",
                                                  f"Невозможно добавить {[_.gland_russian_name for _ in self.rightside_block.list_glands]}",
                                                  QMessageBox.Ok)
                    except:
                        QMessageBox.critical(self, "Справка",
                                             f"Невозможно создать в два ряда",
                                             QMessageBox.Ok)
                        self.sideBListWidget.clear()
                        self.glands_on_sides_dict['Б'].clear()
                        self.rightside_block.glands_on_sides_dict['Б'].clear()

    @Qt.pyqtSlot()
    def add_gland_side_V(self):
        if hasattr(self,'key_gland'):
            if self.siteVSpinBox_2.text() != '0':
                for _ in range(0, int(self.siteVSpinBox_2.text())):
                    self.gland = gland_csv.CableGlandInformation(
                        gland_dict=self.gland_information.gland_main_dict[self.key_gland])
                    self.add_options_to_gland()
                    self.gland.side = 'downside'
                    self.glands_on_sides_dict['В'].append(self.gland)
                    self.sideVListWidget.addItem(self.gland.gland_russian_name)

    @Qt.pyqtSlot()
    def check_to_add_biggest_gland_side_V(self):
        if hasattr(self, 'downside_block'):
            self.downside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.downside_block.check_possible_to_add_biggest_gland() == False:
                biggest_cable_gland = self.glands_on_sides_dict['В'][0]
                QMessageBox.critical(self, "Ошибка",
                                     f"{biggest_cable_gland.gland_russian_name} не помещается кабельный ввод на сторону В",
                                     QMessageBox.Ok)
                self.sideVListWidget.clear()
                self.glands_on_sides_dict['В'].clear()
                self.downside_block.glands_on_sides_dict['В'].clear()

    @Qt.pyqtSlot()
    def check_to_add_all_area_glands_side_V(self):
        if hasattr(self, 'downside_block'):
            self.downside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.downside_block.check_possible_to_add_all_gland() == False:
                QMessageBox.critical(self, "Ошибка",
                                     f"Невозможно поместить эти кабельные вводы",
                                     QMessageBox.Ok)
                self.sideVListWidget.clear()
                self.glands_on_sides_dict['В'].clear()
                self.downside_block.glands_on_sides_dict['В'].clear()

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_one_row_V(self):
        if hasattr(self, 'downside_block'):
            self.downside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.downside_block.check_possible_to_add_in_one_row() == False:
                QMessageBox.critical(self, "Справка",
                                     f"На сторону В в один ряд НЕ помещаются кабельные вводы",
                                     QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Справка",
                                     f"На сторону В в один ряд ПОМЕЩАЮТСЯ кабельные вводы",
                                     QMessageBox.Ok)

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_two_row_V(self):
        if hasattr(self, 'downside_block'):
            self.downside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if hasattr(self.downside_block,'one_row_check'):
                # if self.downside_block.one_row_check.status_add_in_one_row == False:
                    try:
                         self.downside_block.calculate_coordinates_glands_two_row()
                         if self.downside_block.list_glands != []:
                             QMessageBox.critical(self, "Справка",
                                                  f"Невозможно добавить {[_.gland_russian_name for _ in self.downside_block.list_glands]}",
                                                  QMessageBox.Ok)
                    except:
                        QMessageBox.critical(self, "Справка",
                                             f"Невозможно создать в два ряда",
                                             QMessageBox.Ok)
                        self.sideVListWidget.clear()
                        self.glands_on_sides_dict['В'].clear()
                        self.downside_block.glands_on_sides_dict['В'].clear()


    @Qt.pyqtSlot()
    def add_gland_side_G(self):
        if hasattr(self,'key_gland'):
            if self.siteGSpinBox_2.text() != '0':
                for _ in range(0, int(self.siteGSpinBox_2.text())):
                    self.gland = gland_csv.CableGlandInformation(
                        gland_dict=self.gland_information.gland_main_dict[self.key_gland])
                    self.add_options_to_gland()
                    self.gland.side = 'leftside'
                    self.glands_on_sides_dict['Г'].append(self.gland)
                    self.sideGListWidget.addItem(self.gland.gland_russian_name)

    @Qt.pyqtSlot()
    def check_to_add_biggest_gland_side_G(self):
        if hasattr(self, 'leftside_block'):
            self.leftside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.leftside_block.check_possible_to_add_biggest_gland() == False:
                biggest_cable_gland = self.glands_on_sides_dict['Г'][0]
                QMessageBox.critical(self, "Ошибка",
                                     f"{biggest_cable_gland.gland_russian_name} не помещается кабельный ввод на сторону Г",
                                     QMessageBox.Ok)
                self.sideGListWidget.clear()
                self.glands_on_sides_dict['Г'].clear()
                self.leftside_block.glands_on_sides_dict['Г'].clear()

    @Qt.pyqtSlot()
    def check_to_add_all_area_glands_side_G(self):
        if hasattr(self, 'leftside_block'):
            self.leftside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.leftside_block.check_possible_to_add_all_gland() == False:
                QMessageBox.critical(self, "Ошибка",
                                     f"Невозможно поместить эти кабельные вводы",
                                     QMessageBox.Ok)
                self.sideGListWidget.clear()
                self.glands_on_sides_dict['Г'].clear()
                self.leftside_block.glands_on_sides_dict['Г'].clear()

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_one_row_G(self):
        if hasattr(self, 'leftside_block'):
            self.leftside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.leftside_block.check_possible_to_add_in_one_row() == False:
                QMessageBox.critical(self, "Справка",
                                     f"На сторону Г в один ряд НЕ помещаются кабельные вводы",
                                     QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Справка",
                                     f"На сторону Г в один ряд ПОМЕЩАЮТСЯ кабельные вводы",
                                     QMessageBox.Ok)

    @Qt.pyqtSlot()
    def check_to_possible_to_create_all_glands_in_two_row_G(self):
        if hasattr(self, 'leftside_block'):
            self.leftside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if hasattr(self.leftside_block,'one_row_check'):
                # if self.leftside_block.one_row_check.status_add_in_one_row == False:
                    try:
                         self.leftside_block.calculate_coordinates_glands_two_row()
                         if self.leftside_block.list_glands != []:
                             QMessageBox.critical(self, "Справка",
                                                  f"Невозможно добавить {[_.gland_russian_name for _ in self.leftside_block.list_glands]}",
                                                  QMessageBox.Ok)
                    except:
                        QMessageBox.critical(self, "Справка",
                                             f"Невозможно создать в два ряда",
                                             QMessageBox.Ok)
                        self.sideGListWidget.clear()
                        self.glands_on_sides_dict['Г'].clear()
                        self.leftside_block.glands_on_sides_dict['Г'].clear()

    @Qt.pyqtSlot()
    def add_gland_side_Cover(self):
        if hasattr(self,'key_gland'):
            if self.siteCoverSpinBox.text() != '0':
                for _ in range(0, int(self.siteCoverSpinBox.text())):
                    self.gland = gland_csv.CableGlandInformation(
                        gland_dict=self.gland_information.gland_main_dict[self.key_gland])
                    self.add_options_to_gland()
                    self.gland.side = 'topside'
                    self.glands_on_sides_dict['Крышка'].append(self.gland)
                    self.CoverListWidget.addItem(self.gland.gland_russian_name)


    @Qt.pyqtSlot()
    def check_to_add_biggest_gland_side_Cover(self):
        if hasattr(self, 'topside_block'):
            self.topside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            if self.topside_block.check_possible_to_add_biggest_gland() == False:
                biggest_cable_gland = self.glands_on_sides_dict['Крышка'][0]
                QMessageBox.critical(self, "Ошибка",
                                     f"{biggest_cable_gland.gland_russian_name} не помещается кабельный ввод на сторону Крышка",
                                     QMessageBox.Ok)
                self.CoverListWidget.clear()
                self.glands_on_sides_dict['Крышка'].clear()
                self.upside_block.glands_on_sides_dict['Крышка'].clear()


    @Qt.pyqtSlot()
    def clear_ABVG_spinbox_afted_add_button(self):
        # Установка нулевых значений в spinbox
        self.siteASpinBox_2.setValue(0)
        self.siteBSpinBox_2.setValue(0)
        self.siteVSpinBox_2.setValue(0)
        self.siteGSpinBox_2.setValue(0)
        self.siteCoverSpinBox.setValue(0)
        self.gland_checkdiam_minlineedit.clear()
        self.gland_checkdiam_maxlineedit.clear()
        self.gland_additionalmarkingcomboBox.clear()

    @Qt.pyqtSlot()
    def clear_all_list_widget(self):
        self.sideAListWidget.clear()
        self.sideBListWidget.clear()
        self.sideVListWidget.clear()
        self.sideGListWidget.clear()
        self.CoverListWidget.clear()
        self.glands_on_sides_dict = {"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}

    @Qt.pyqtSlot()
    def click_up_button_A(self):
        rowIndex = self.sideAListWidget.currentRow()
        currentItem = self.sideAListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['А'][rowIndex],self.glands_on_sides_dict['А'][rowIndex - 1] =\
        self.glands_on_sides_dict['А'][rowIndex-1], self.glands_on_sides_dict['А'][rowIndex]
        self.sideAListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideAListWidget.setCurrentRow(rowIndex - 1)

    @Qt.pyqtSlot()
    def click_up_button_B(self):
        rowIndex = self.sideBListWidget.currentRow()
        currentItem = self.sideBListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['Б'][rowIndex],self.glands_on_sides_dict['Б'][rowIndex - 1] =\
        self.glands_on_sides_dict['Б'][rowIndex-1], self.glands_on_sides_dict['Б'][rowIndex]
        self.sideBListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideBListWidget.setCurrentRow(rowIndex - 1)

    @Qt.pyqtSlot()
    def click_up_button_V(self):
        rowIndex = self.sideVListWidget.currentRow()
        currentItem = self.sideVListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['В'][rowIndex],self.glands_on_sides_dict['В'][rowIndex - 1] =\
        self.glands_on_sides_dict['В'][rowIndex-1], self.glands_on_sides_dict['В'][rowIndex]
        self.sideVListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideVListWidget.setCurrentRow(rowIndex - 1)

    @Qt.pyqtSlot()
    def click_up_button_G(self):
        rowIndex = self.sideGListWidget.currentRow()
        currentItem = self.sideGListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['Г'][rowIndex],self.glands_on_sides_dict['Г'][rowIndex - 1] =\
        self.glands_on_sides_dict['Г'][rowIndex-1], self.glands_on_sides_dict['Г'][rowIndex]
        self.sideGListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideGListWidget.setCurrentRow(rowIndex - 1)

    @Qt.pyqtSlot()
    def click_up_button_cover(self):
        rowIndex = self.CoverListWidget.currentRow()
        currentItem = self.CoverListWidget.takeItem(rowIndex)
        self.CoverListWidget.insertItem(rowIndex - 1, currentItem)
        self.CoverListWidget.setCurrentRow(rowIndex - 1)

    @Qt.pyqtSlot()
    def click_down_button_A(self):
        rowIndex = self.sideAListWidget.currentRow()
        currentItem = self.sideAListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['А'][rowIndex],self.glands_on_sides_dict['А'][rowIndex +1] =\
        self.glands_on_sides_dict['А'][rowIndex+1], self.glands_on_sides_dict['А'][rowIndex]
        self.sideAListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideAListWidget.setCurrentRow(rowIndex + 1)

    @Qt.pyqtSlot()
    def click_down_button_B(self):
        rowIndex = self.sideBListWidget.currentRow()
        currentItem = self.sideBListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['Б'][rowIndex],self.glands_on_sides_dict['Б'][rowIndex +1] =\
        self.glands_on_sides_dict['Б'][rowIndex+1], self.glands_on_sides_dict['Б'][rowIndex]
        self.sideBListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideBListWidget.setCurrentRow(rowIndex + 1)

    @Qt.pyqtSlot()
    def click_down_button_V(self):
        rowIndex = self.sideVListWidget.currentRow()
        currentItem = self.sideVListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['В'][rowIndex],self.glands_on_sides_dict['В'][rowIndex +1] =\
        self.glands_on_sides_dict['В'][rowIndex+1], self.glands_on_sides_dict['В'][rowIndex]
        self.sideVListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideVListWidget.setCurrentRow(rowIndex + 1)

    @Qt.pyqtSlot()
    def click_down_button_G(self):
        rowIndex = self.sideGListWidget.currentRow()
        currentItem = self.sideGListWidget.takeItem(rowIndex)
        self.glands_on_sides_dict['Г'][rowIndex],self.glands_on_sides_dict['Г'][rowIndex +1] =\
        self.glands_on_sides_dict['Г'][rowIndex+1], self.glands_on_sides_dict['Г'][rowIndex]
        self.sideGListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideGListWidget.setCurrentRow(rowIndex + 1)

    @Qt.pyqtSlot()
    def click_down_button_cover(self):
        rowIndex = self.CoverListWidget.currentRow()
        currentItem = self.CoverListWidget.takeItem(rowIndex)
        self.CoverListWidget.insertItem(rowIndex + 1, currentItem)
        self.CoverListWidget.setCurrentRow(rowIndex + 1)

    @Qt.pyqtSlot()
    def click_delete_button_A(self):
        if self.sideAListWidget.count() !=0:
            rowIndex = self.sideAListWidget.currentRow()
            self.glands_on_sides_dict['А'].pop(rowIndex)
            currentItem = self.sideAListWidget.takeItem(rowIndex)

    @Qt.pyqtSlot()
    def click_delete_button_B(self):
        if self.sideBListWidget.count() != 0:
            rowIndex = self.sideBListWidget.currentRow()
            self.glands_on_sides_dict['Б'].pop(rowIndex)
            currentItem = self.sideBListWidget.takeItem(rowIndex)

    @Qt.pyqtSlot()
    def click_delete_button_V(self):
        if self.sideVListWidget.count() != 0:
            rowIndex = self.sideVListWidget.currentRow()
            self.glands_on_sides_dict['В'].pop(rowIndex)
            currentItem = self.sideVListWidget.takeItem(rowIndex)

    @Qt.pyqtSlot()
    def click_delete_button_G(self):
        if self.sideGListWidget.count() != 0:
            rowIndex = self.sideGListWidget.currentRow()
            self.glands_on_sides_dict['Г'].pop(rowIndex)
            currentItem = self.sideGListWidget.takeItem(rowIndex)

    @Qt.pyqtSlot()
    def click_delete_button_cover(self):
        if self.CoverListWidget.count() != 0:
            rowIndex = self.CoverListWidget.currentRow()
            self.glands_on_sides_dict['Крышка'].pop(rowIndex)
            currentItem = self.CoverListWidget.takeItem(rowIndex)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = GlandInterface()
    welcome_window.show()
    sys.exit(app.exec_())