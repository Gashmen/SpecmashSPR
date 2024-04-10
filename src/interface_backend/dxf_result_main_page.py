import ezdxf
import os
import sys
from pypdf import PdfMerger
from ezdxf.addons import Importer
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox
import time
from src.interface_backend import dxf_terminal_ui  #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ
from src.draw import nameplate
from src.draw import price
from src.draw import border as border_create
from src.border import change_border
from src.draw.preview import cad_viewer

class MainPageDxfQtCommunication(dxf_terminal_ui.DxfTerminalQtCommunication):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        time_pusk = time.time()
        super().__init__()


        self.sizeCombobox_shellpage.currentTextChanged.connect(self.actions_shell)

        self.border_window_setup()
        self.border_window.lineEdit_10.editingFinished.connect(self.change_scale)

        self.serialCombobox_shellpage.currentTextChanged.connect(self.border_window_title)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.border_window_title)

        self.borderButton.clicked.connect(self.border_window_show)

        self.sizeCombobox_shellpage.currentTextChanged.connect(self.preview_button_enabled)
        self.previewButton_leftMenu.clicked.connect(self.preview_mode)


        self.Autohelper.clicked.connect(self.create_border)

        self.Autohelper.clicked.connect(self.create_nameplate)
        self.Autohelper.clicked.connect(self.create_dimension)
        # self.Autohelper.clicked.connect(self.redraw_withoutcapside)
        self.Autohelper.clicked.connect(self.redraw_dinreyka)
        # self.Autohelper.clicked.connect(self.redraw_nameplate)
        self.Autohelper.clicked.connect(self.create_importer)
        self.Autohelper.clicked.connect(self.logger_update_info)


        self.Autohelper.clicked.connect(self.save_doc)
        self.Autohelper.clicked.connect(self.save_pdf)

        self.Autohelper.clicked.connect(self.create_BOM)
        self.Autohelper.clicked.connect(self.merge_result_pdf)

        # self.Autohelper.clicked.connect(self.delete_block_before_save)



        print('Запуск программы: ',time.time()-time_pusk)

    @Qt.pyqtSlot()
    def actions_shell(self):
        # self.create_doc_copy()
        self.set_shell_base_dxf()#Установка класса ShellBaseDxf в переменную shell_base_dxf
        self.check_possible_to_add_shell()

        self.set_zero_max_glands_length()

        self.set_shell_blocks()
        self.calculate_scale_shell()
        self.setup_gland_sideA()
        self.setup_gland_sideB()
        self.setup_gland_sideV()
        self.setup_gland_sideG()
        self.setup_gland_sideCover()
        self.check_possible_to_add_terminals()
        if hasattr(self,'glands_on_sides_dxf_dict'):
            if self.glands_on_sides_dxf_dict != {"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}:

                self.setup_glands()
        self.draw_shells_inserts()

    def create_border(self):
        '''Создает рамку относительно '''
        block_border = self.base_dxf.doc_base.blocks['Border_A3']
        values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
        self.border_insert = self.base_dxf.doc_base.modelspace().add_blockref(name='Border_A3',
                                                                              insert=(0,0))
        self.border_insert.add_auto_attribs(values)

        for attrib in self.border_insert.attribs:
            if self.designer_name !='':
                border_create.write_rudes(attrib_rudes=attrib, rudes=self.designer_name)
                border_create.write_rudesdata(attrib_rudesdata=attrib, rudesdata=self.border_window.date_today)

            if self.border_window.lineEdit_2.text() !='':
                border_create.write_rucheck(attrib,self.border_window.lineEdit_2.text())
                border_create.write_rucheckdata(attrib, self.border_window.date_today)

            if self.border_window.lineEdit_3.text() !='':
                border_create.write_runcont(attrib,self.border_window.lineEdit_3.text())
                border_create.write_runcontdata(attrib, self.border_window.date_today)

            if self.border_window.lineEdit_4.text() != '':
                border_create.wrire_rupem(attrib,self.border_window.lineEdit_4.text())
                border_create.wrire_rupemdata(attrib, self.border_window.date_today)

            border_create.write_RUTITLE_attrib(attrib_rutitle=attrib, rutitle_text=self.border_window.lineEdit_5.text())
            border_create.write_project_title_1(attrib,self.border_window.lineEdit_6.text())
            border_create.write_project_title_2(attrib, self.border_window.lineEdit_7.text())
            border_create.write_project_title_3(attrib, self.border_window.lineEdit_8.text())
            border_create.write_company_attrib(attrib,self.border_window.lineEdit_9.text())

            border_create.write_scale(attrib_SCALE=attrib,SCALE=self.scale_class.scale)
            border_create.write_page_number(attrib_RUSHEET=attrib,sheet_number=1)
            border_create.write_page_numbers(attrib_RUSHTS=attrib,sheet_count='')


    def create_importer(self):
        self.base_dxf.doc_for_save = ezdxf.new()
        self.importer = Importer(self.base_dxf.doc_base, self.base_dxf.doc_for_save)
        self.importer.import_modelspace()
        self.importer.import_block('BOM_FIRST')
        self.importer.import_block('BOM_SECOND')
        self.importer.finalize()
        din_block = self.base_dxf.doc_base.blocks[self.withoutcapside_block.din_insert.dxf.name]
        din_block.set_redraw_order(
            (solid.dxf.handle, "%X" % (1000 - solid.dxf.color))
            for solid in din_block.entity_space if solid.dxftype() == 'HATCH')


    def create_dimension(self):
        '''Создаем размер'''
        y_upper = self.topside_insert.dxf.insert[1] + self.topside_block.extreme_lines['y_max']/self.scale_class.scale
        x_upper = self.topside_insert.dxf.insert[0] + self.topside_block.extreme_lines['x_min']/self.scale_class.scale
        if hasattr(self,'glands_on_sides_dxf_dict'):
            if len(self.glands_on_sides_dxf_dict['А']) >0:
                y_upper += self.scale_class.len4_y/self.scale_class.scale
                biggest_leftest_gland = sorted([i for i in self.glands_on_sides_dxf_dict['А'] if self.scale_class.len4_y == i.gland_length_dxf],key=lambda x:x.gland_csv.x_coordinate,reverse=True)[0]
                x_upper += (self.upside_block.extreme_lines['x_max'] - biggest_leftest_gland.gland_csv.x_coordinate)/self.scale_class.scale

        y_bottom = self.topside_insert.dxf.insert[1] + self.topside_block.extreme_lines['y_min']/self.scale_class.scale
        x_bottom = self.topside_insert.dxf.insert[0] + self.topside_block.extreme_lines['x_min']/self.scale_class.scale
        if hasattr(self, 'glands_on_sides_dxf_dict'):
            if len(self.glands_on_sides_dxf_dict['В']) >0:
                y_bottom -= self.scale_class.len2_y/self.scale_class.scale
                biggest_leftest_gland = sorted([i for i in self.glands_on_sides_dxf_dict['В'] if self.scale_class.len2_y == i.gland_length_dxf],key=lambda x:x.gland_csv.x_coordinate,reverse=False)[0]
                x_bottom += (-self.upside_block.extreme_lines['x_min'] + biggest_leftest_gland.gland_csv.x_coordinate)/self.scale_class.scale

        y_leftest = self.topside_insert.dxf.insert[1] + self.topside_block.extreme_lines['y_min'] / self.scale_class.scale
        x_leftest = self.topside_insert.dxf.insert[0] + self.topside_block.extreme_lines['x_min'] / self.scale_class.scale
        if hasattr(self, 'glands_on_sides_dxf_dict'):
            if len(self.glands_on_sides_dxf_dict['Г']) > 0:
                x_leftest -= self.scale_class.len2_x/self.scale_class.scale
                biggest_leftest_gland = \
                sorted([i for i in self.glands_on_sides_dxf_dict['Г'] if self.scale_class.len2_x == i.gland_length_dxf],
                       key=lambda x: x.gland_csv.x_coordinate, reverse=True)[0]
                y_leftest += (self.leftside_block.extreme_lines['x_max'] - biggest_leftest_gland.gland_csv.x_coordinate) / self.scale_class.scale

        y_rightest = self.topside_insert.dxf.insert[1] + self.topside_block.extreme_lines['y_min'] / self.scale_class.scale
        x_rightest = self.topside_insert.dxf.insert[0] + self.topside_block.extreme_lines['x_max'] / self.scale_class.scale

        if hasattr(self, 'glands_on_sides_dxf_dict'):
            if len(self.glands_on_sides_dxf_dict['Б']) > 0:
                x_rightest += self.scale_class.len4_x / self.scale_class.scale
                biggest_leftest_gland = \
                    sorted([i for i in self.glands_on_sides_dxf_dict['Б'] if self.scale_class.len4_x == i.gland_length_dxf],
                           key=lambda x: x.gland_csv.x_coordinate, reverse=False)[0]
                y_rightest += (-self.rightside_block.extreme_lines['x_min'] + biggest_leftest_gland.gland_csv.x_coordinate) / self.scale_class.scale

        x_for_leftside_dim = self.rightside_insert.dxf.insert[0] - self.rightside_block.extreme_lines['y_max']/self.scale_class.scale
        y_for_leftside_dim = self.rightside_insert.dxf.insert[1] + self.rightside_block.extreme_lines['x_min']/self.scale_class.scale
        if hasattr(self, 'glands_on_sides_dxf_dict'):
            if len(self.glands_on_sides_dxf_dict['Крышка']) > 0:
                x_for_leftside_dim -= self.scale_class.len0_x / self.scale_class.scale
                biggest_leftest_gland = \
                    sorted([i for i in self.glands_on_sides_dxf_dict['Крышка'] if self.scale_class.len0_x == i.gland_length_dxf],
                           key=lambda x: x.gland_csv.y_coordinate, reverse=True)[0]
                y_for_leftside_dim += ((-self.topside_block.extreme_lines['y_min'] + biggest_leftest_gland.gland_csv.y_coordinate)/ self.scale_class.scale)

        dim_style_old = ezdxf.setup_dimstyles(doc = self.base_dxf.doc_base)

        dim_base = self.base_dxf.doc_base.modelspace().add_linear_dim(
            angle=90,
            p1=tuple([x_bottom,y_bottom]),
            p2=tuple([x_upper,y_upper]),
            dimstyle='EZDXF',
            base=((self.rightside_insert.dxf.insert[0] - self.rightside_block.extreme_lines['y_min']/self.scale_class.scale + x_leftest)/2,
                  self.topside_insert.dxf.insert[1]),
            text = f'{round((y_upper - y_bottom)  * self.scale_class.scale, 1)}'

        )

        dim_horizontal_base = self.base_dxf.doc_base.modelspace().add_linear_dim(
                    angle =0,
                    p1=tuple([x_leftest,y_leftest]),
                    p2=tuple([x_rightest,y_rightest]),
                    dimstyle='EZDXF',
                    text=f'{round((x_rightest - x_leftest) * self.scale_class.scale, 1)}',
                    base=(self.topside_insert.dxf.insert[0],
                          (self.upside_insert.dxf.insert[1] -
                             self.rightside_block.extreme_lines['y_min'] / self.scale_class.scale + y_bottom) / 2)
                    )

        self.base_dxf.doc_base.styles.entries['kdimtextstyle'].dxf.width = 1
        self.base_dxf.doc_base.styles.entries['kdimtextstyle'].dxf.oblique = 0
        self.base_dxf.doc_base.styles.entries['kdimtextstyle'].dxf.height = 3.5
        dim_horizontal_base.dimstyle.dxf.dimtxsty = 'kdimtextstyle'
        dim_horizontal_base.dimstyle.dxf.dimtxt = 2.2
        dim_horizontal_base.dimstyle.dxf.dimexe = 1
        dim_horizontal_base.dimstyle.dxf.dimgap = 1
        dim_horizontal_base.dimstyle.dxf.dimblk = ''
        dim_horizontal_base.dimstyle.dxf.dimasz = 4
        dim_horizontal_base.dimension.dxf.color = 256

        dim_height_rightside_base = self.base_dxf.doc_base.modelspace().add_linear_dim(
                    p1=(x_for_leftside_dim,
                        y_for_leftside_dim),
                    p2=(self.rightside_insert.dxf.insert[0] - self.rightside_block.extreme_lines['y_min']/self.scale_class.scale,
                        self.rightside_insert.dxf.insert[1] + self.rightside_block.extreme_lines['x_max']/self.scale_class.scale),
                    dimstyle='EZDXF',
                    base=(self.rightside_insert.dxf.insert[0] +
                               (self.rightside_block.extreme_lines['y_min']/self.scale_class.scale +
                                self.rightside_block.extreme_lines['y_max']/self.scale_class.scale)/2,
                          (y_upper + self.downside_insert.dxf.insert[1] + self.downside_block.extreme_lines['y_min'])/2 ),
                    text=f'{round((self.rightside_insert.dxf.insert[0] - self.rightside_block.extreme_lines["y_min"]/self.scale_class.scale - x_for_leftside_dim)  * self.scale_class.scale, 1)}'
                )

        dim_height_rightside_base.dimension.dxf.color = 256

        dim_base.render()
        dim_horizontal_base.render()
        dim_height_rightside_base.render()

    def delete_block_before_save(self):
        time1 = time.time()
        for block_name in list(self.base_dxf.doc_dict_blocks.keys()):
            if block_name not in ['BOM_FIRST','BOM_SECOND','Border_A3',
                                  'cut_name_bottom','cut_name_main','cut_name_top'] and\
                    '*' not in block_name:
                try:
                    self.base_dxf.doc_base.blocks.delete_block(name=block_name)
                except:
                    continue
        time1 = time.time() - time1
        print(time1)

    def create_nameplate(self):

        if self.glands_on_sides_dict['Крышка'] ==[]:
            self.nameplate_insert = nameplate.create_nameplate_doc(doc_base=self.base_dxf.doc_base,
                                                                   scale=self.scale_class.scale,
                                                                   topside_insert=self.topside_insert)
            for attrib_in_nameplate in self.nameplate_insert.attribs:
                if self.task_number != '':
                    nameplate.write_attrib_box_full_name(attrib=attrib_in_nameplate,
                                                         full_name=f'К{self.serialCombobox_shellpage.currentText()}.{self.sizeCombobox_shellpage.currentText()}',
                                                         add_numbers=f'.{self.task_number}.{self.position_number}')
                else:
                    nameplate.write_attrib_box_full_name(attrib=attrib_in_nameplate,
                                                         full_name=f'К{self.serialCombobox_shellpage.currentText()}.{self.sizeCombobox_shellpage.currentText()}')

                nameplate.write_explosion_tag(attrib=attrib_in_nameplate,
                                              gasdustore=self.gasdustoreComboBox_shellpage.currentText(),
                                              temperature_class=self.temperature_class_comboBox_shellpage.currentText())
                nameplate.write_minus_temperature(attrib=attrib_in_nameplate,
                                                  minus_temperature=self.mintempLineEdit_shellpage_3.text())
                nameplate.write_plus_temperature(attrib=attrib_in_nameplate,
                                                 plus_temperature=self.maxtempLineedit_shellpage_3.text())
                nameplate.write_voltage_current_frequency(attrib=attrib_in_nameplate)
                nameplate.write_batch_number(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_1(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_2(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_3(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_4(attrib=attrib_in_nameplate)

    def redraw_withoutcapside(self):
        # Create a dictionary of entity_handle and sort_handle pairs using a dictionary comprehension
        handles = {}
        sort_handle = 1  # Start with a lower sort handle for other inserts
        for solid in self.base_dxf.doc_base.modelspace():
            if solid.dxftype() == 'INSERT':
                if 'withoutcapside' in solid.dxf.name:
                    handles[
                        solid.dxf.handle] = 0  # Set sort handle 'A' for inserts with 'withoutcapside' in their names
                else:
                    handles[solid.dxf.handle] = str(sort_handle)  # Set a unique sort handle for other inserts
                    sort_handle += 1  # Increment the sort handle for other inserts

        self.base_dxf.doc_base.modelspace().set_redraw_order(handles)

    def redraw_dinreyka(self):
        # Create a dictionary of entity_handle and sort_handle pairs using a dictionary comprehension
        handles = {}
        sort_handle = 1  # Start with a lower sort handle for other inserts
        for solid in self.base_dxf.doc_base.blocks[self.withoutcapside_block.din_insert.dxf.name].query():
            if solid.dxftype() != 'HATCH':
                handles[solid.dxf.handle] = 0  # Set sort handle 'A' for inserts with 'withoutcapside' in their names
            else:
                handles[solid.dxf.handle] = str(sort_handle)  # Set a unique sort handle for other inserts
                sort_handle += 1  # Increment the sort handle for other inserts

        self.base_dxf.doc_base.blocks[self.withoutcapside_block.din_insert.dxf.name].set_redraw_order(handles)

    def redraw_nameplate(self):

        handles = {}
        sort_handle = 1  # Start with a lower sort handle for other inserts
        for solid in self.base_dxf.doc_base.blocks['nameplate']:
            if solid.dxftype() == 'ATTDEF':
                handles[solid.dxf.handle] = 0
            if solid.dxftype() != 'HATCH':
                handles[solid.dxf.handle] = 0  # Set sort handle 'A' for inserts with 'withoutcapside' in their names
            else:
                handles[solid.dxf.handle] = str(len(list(self.base_dxf.doc_for_save.blocks['nameplate'].query())))  # Set a unique sort handle for other inserts
                sort_handle += 1  # Increment the sort handle for other inserts

        self.base_dxf.doc_base.blocks['nameplate'].set_redraw_order(handles)

    def logger_update_info(self):

        if hasattr(self,'logger'):
            self.logger.logger.info(f'Время заполнения информации: {time.time() - self.logger_time}')
            if hasattr(self,'shell_dict'):
                self.logger.logger.info(f'Оболочка: {self.shell_dict["СПЕЦИФИКАЦИЯ_НАИМЕНОВАНИЕ"]}')
            if self.sideAListWidget.count() != 0:
                self.logger.logger.info(f'Сторона А: {[self.sideAListWidget.item(i).text() for i in range(self.sideAListWidget.count())]}')
            if self.sideBListWidget.count() != 0:
                self.logger.logger.info(f'Сторона Б: {[self.sideBListWidget.item(i).text() for i in range(self.sideBListWidget.count())]}')
            if self.sideVListWidget.count() != 0:
                self.logger.logger.info(f'Сторона В: {[self.sideVListWidget.item(i).text() for i in range(self.sideVListWidget.count())]}')
            if self.sideGListWidget.count() != 0:
                self.logger.logger.info(f'Сторона Г: {[self.sideGListWidget.item(i).text() for i in range(self.sideGListWidget.count())]}')
            if self.CoverListWidget.count() != 0:
                self.logger.logger.info(f'На Крышке: {[self.CoverListWidget.item(i).text() for i in range(self.CoverListWidget.count())]}')

            if self.add_button_terminal_listwidget.count() != 0:
                self.logger.logger.info(f'Клеммы: {[self.add_button_terminal_listwidget.item(i).text() for i in range(self.add_button_terminal_listwidget.count())]}')



            # with open(self.logger.logger_path, 'r') as fr,open(f'{os.getlogin()}_{time.time()}.txt','w') as fw:
            #     for line in fr:
            #         fw.write(line)


            self.smb_specmash.save_log(logger_path=self.logger.logger_path)

    def create_BOM(self):
        if hasattr(self,'BOM_general'):
            self.BOM_general.list_elements.clear()
            #Добавление оболочки и всего причастного в BOM
            # self.shell_information.BOM_shell.give_bom_dict()
            self.shell_information.BOM_shell.add_din_bom(self.withoutcapside_block.din_length)
            self.BOM_general.add_bom_list_elements(BOM=self.shell_information.BOM_shell.bom_dict)

            #Добавление кабельных вводов и всего причастного в BOM
            for gland_on_side in list(self.glands_on_sides_dxf_dict.values()):
                for gland in gland_on_side:
                    self.BOM_general.add_bom_list_elements(BOM=gland.gland_csv.BOM_gland.bom_dict)
            #Добавление клемм и всего причастного в BOM
            for terminal in self.list_terminal_dxf:
                self.BOM_general.add_bom_list_elements(BOM=terminal.bom_dict)
            self.BOM_general.create_new_bom_dict()
            self.BOM_general.create_dict_main_properties()
            self.BOM_general.dict_all_attrib_in_BOM()
            self.BOM_general.modify_dict_for_BOM()

            for bom_page in self.BOM_general.BOM_result_dict:
                BOM = None
                if bom_page == 1:
                    BOM = self.BOM_general.create_BOM_first(doc_bom=self.base_dxf.doc_for_save)
                else:
                    BOM = self.BOM_general.create_BOM_SECOND(doc_bom=self.base_dxf.doc_for_save)
                dict_attribs = {attrib.dxf.tag: attrib for attrib in BOM.attribs}
                dict_attribs['SHEET_FIRST'].dxf.text = str(bom_page)
                dict_attribs['RUTITLE'].dxf.text = self.border_window.lineEdit_5.text()
                if bom_page == 1:
                    dict_attribs['SHEET_COUNT'].dxf.text = str(max(list(self.BOM_general.BOM_result_dict.keys())))
                    if self.designer_name != '':
                        dict_attribs['RUDES'].dxf.text = self.designer_name
                        dict_attribs['RUDESDATA'].dxf.text = self.border_window.date_today
                    if self.border_window.lineEdit_2.text() !='':
                        dict_attribs['RUCHECK'].dxf.text = self.border_window.lineEdit_2.text()
                        dict_attribs['RUCHECKDATA'].dxf.text = self.border_window.date_today
                    if self.border_window.lineEdit_3.text() !='':
                        dict_attribs['RUNCONT'].dxf.text = self.border_window.lineEdit_3.text()
                        dict_attribs['RUNCONTDATA'].dxf.text = self.border_window.date_today
                    if self.border_window.lineEdit_4.text() !='':
                        dict_attribs['RUPEM'].dxf.text = self.border_window.lineEdit_4.text()
                        dict_attribs['RUPEMDATA'].dxf.text = self.border_window.date_today

                    dict_attribs['PROJECT_TITLE_1'].dxf.text = self.border_window.lineEdit_6.text()
                    dict_attribs['PROJECT_TITLE_2'].dxf.text = self.border_window.lineEdit_7.text()
                    dict_attribs['PROJECT_TITLE_3'].dxf.text = self.border_window.lineEdit_8.text()




                for attribs in self.BOM_general.BOM_result_dict[bom_page]:
                    if attribs in list(dict_attribs.keys()):
                        dict_attribs[attribs].dxf.text = self.BOM_general.BOM_result_dict[bom_page][attribs]

                # self.base_dxf.doc_for_save = ezdxf.new()
                # self.importer = Importer(self.base_dxf.doc_base, self.base_dxf.doc_for_save)
                # self.importer.import_modelspace()
                # self.importer.finalize()

                if self.border_window.lineEdit_5.text() !='':
                    self.base_dxf.doc_for_save.saveas(f'Спецификация_' + self.border_window.lineEdit_5.text() + '.dxf')
                else:
                    self.base_dxf.doc_for_save.saveas(f'Спецификация' + self.designer_name + str(time.time()) + '.dxf')
                self.save_pdf_BOM(page_number=bom_page)
                self.smb_specmash.get_base_pricexlsx_path()
                price_terminal_dict = price.read_price(path_price=self.smb_specmash.price_xlsx_path)
                self.price_xlsx_wb = price.result_xlsx(dict_columnrowname_value=self.BOM_general.return_dict_attribs,
                                                       price_terminal_dict=price_terminal_dict)
                self.price_xlsx_wb.save(f'Спецификация_' + self.border_window.lineEdit_5.text() + '.xlsx')

    def merge_result_pdf(self):

        merger = PdfMerger()

        for pdf in self.pdf_files:
            merger.append(pdf)

        merger.write(self.border_window.lineEdit_5.text() + ".pdf")
        merger.close()

        for i in self.pdf_files:
            os.remove(i)
        self.pdf_files.clear()

    def border_window_setup(self):
        self.border_window = change_border.BorderInterface()


    def border_window_title(self):
        self.title_name = ''
        if self.serialCombobox_shellpage.currentText() != '':
            self.title_name += f'К{self.serialCombobox_shellpage.currentText()}.'
        if self.sizeCombobox_shellpage.currentText() != '':
            self.title_name += f'{self.sizeCombobox_shellpage.currentText()}.'
        if self.task_number != '':
            self.title_name += f'{self.task_number}.'
        else:
            self.title_name += f'ХХХХ.'
        if self.position_number != '':
            self.title_name += f'{self.position_number} '
        else:
            self.title_name += f'ХX '
        self.title_name += 'ВО'

        self.border_window.set_title(title=self.title_name)


    def border_window_show(self):
        '''открытие окна настройки рамки'''
        self.border_window.set_designer(designer=self.designer_name)
        if hasattr(self,'scale_class'):
            if hasattr(self.scale_class,'scale_border'):
                self.border_window.set_scale(scale= str(self.scale_class.scale_border))
        self.border_window.show()

    def change_scale(self):
        if hasattr(self.scale_class,'scale'):
            if self.border_window.lineEdit_10.text() != '':
                if self.scale_class.scale != self.border_window.lineEdit_10.text():

                    if '.' in self.border_window.lineEdit_10.text():
                        self.scale_class.scale = float(self.border_window.lineEdit_10.text())
                    else:
                        self.scale_class.scale = int(self.border_window.lineEdit_10.text())

                    self.scale_class.calculate_len_x_top(scale_gost=self.scale_class.scale)
                    self.scale_class.calculate_len_y_left(scale_gost=self.scale_class.scale)
                    self.scale_class.calculate_free_space()

                    self.draw_glands_in_sides()
                    self.draw_shells_inserts()

    def preview_button_enabled(self):
        if hasattr(self,'base_dxf'):
            if hasattr(self.base_dxf,'doc_base'):
                self.previewButton_leftMenu.setEnabled(True)
    def preview_mode(self):
        cad_viewer.preview_mode(doc=self.base_dxf.doc_base)






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = MainPageDxfQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())