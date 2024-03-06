import ezdxf
import os
import sys
from ezdxf.addons import Importer
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox
import time
from src.interface_backend import dxf_terminal_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ
from src.draw import nameplate

class MainPageDxfQtCommunication(dxf_terminal_ui.DxfTerminalQtCommunication):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        time_pusk = time.time()
        super().__init__()

        self.sizeCombobox_shellpage.currentTextChanged.connect(self.actions_shell)

        self.Autohelper.clicked.connect(self.create_border)

        self.Autohelper.clicked.connect(self.create_nameplate)
        self.Autohelper.clicked.connect(self.create_importer)
        self.Autohelper.clicked.connect(self.create_dimension)
        self.Autohelper.clicked.connect(self.redraw_withoutcapside)
        # self.Autohelper.clicked.connect(self.delete_block_before_save)
        self.Autohelper.clicked.connect(self.save_doc)
        self.Autohelper.clicked.connect(self.save_pdf)
        print(time.time()-time_pusk)
    def create_border(self):
        '''Создает рамку относительно '''
        block_border = self.base_dxf.doc_base.blocks['Border_A3']
        values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
        self.border_insert = self.base_dxf.doc_base.modelspace().add_blockref(name='Border_A3',
                                                                              insert=(0,0))
        self.border_insert.add_auto_attribs(values)

    def create_importer(self):
        # тест, потом удалить
        time2 = time.time()
        self.base_dxf.doc_for_save = ezdxf.new()
        self.importer = Importer(self.base_dxf.doc_base, self.base_dxf.doc_for_save)
        self.importer.import_modelspace()
        self.importer.finalize()
        din_block = self.base_dxf.doc_base.blocks[self.withoutcapside_block.din_insert.dxf.name]
        din_block.set_redraw_order(
            (solid.dxf.handle, "%X" % (1000 - solid.dxf.color))
            for solid in din_block.entity_space if solid.dxftype() == 'HATCH')
        # self.base_dxf.doc_for_save.saveas('check.dxf')
        print(time.time() - time2)
        # pass

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

        dim_style_new = ezdxf.setup_dimstyles(doc = self.base_dxf.doc_for_save)

        dim = self.base_dxf.doc_for_save.modelspace().add_linear_dim(
            angle=90,
            p1=tuple([x_bottom,y_bottom]),
            p2=tuple([x_upper,y_upper]),
            dimstyle='EZDXF',
            base=((self.rightside_insert.dxf.insert[0] - self.rightside_block.extreme_lines['y_min']/self.scale_class.scale + x_leftest)/2,
                  self.topside_insert.dxf.insert[1]),
            text = f'{round((y_upper - y_bottom)  * self.scale_class.scale, 1)}'

        )

        dim_horizontal = self.base_dxf.doc_for_save.modelspace().add_linear_dim(
                    angle =0,
                    p1=tuple([x_leftest,y_leftest]),
                    p2=tuple([x_rightest,y_rightest]),
                    dimstyle='EZDXF',
                    text=f'{round((x_rightest - x_leftest) * self.scale_class.scale, 1)}',
                    base=(self.topside_insert.dxf.insert[0],
                          (self.upside_insert.dxf.insert[1] -
                             self.rightside_block.extreme_lines['y_min'] / self.scale_class.scale + y_bottom) / 2)
                    )
        self.base_dxf.doc_for_save.styles.entries['kdimtextstyle'].dxf.width = 1
        self.base_dxf.doc_for_save.styles.entries['kdimtextstyle'].dxf.oblique = 0
        self.base_dxf.doc_for_save.styles.entries['kdimtextstyle'].dxf.height = 3.5
        dim_horizontal.dimstyle.dxf.dimtxsty = 'kdimtextstyle'
        dim_horizontal.dimstyle.dxf.dimtxt = 2.2
        dim_horizontal.dimstyle.dxf.dimexe = 1
        dim_horizontal.dimstyle.dxf.dimgap = 1
        dim_horizontal.dimstyle.dxf.dimblk = ''
        dim_horizontal.dimstyle.dxf.dimasz = 4

        # dim_horizontal.render()

        dim_height_rightside = self.base_dxf.doc_for_save.modelspace().add_linear_dim(
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
        # Assuming self.base_dxf.doc_base.modelspace() returns the modelspace object

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
                                                  minus_temperature=self.mintempLineEdit_shellpage.text())
                nameplate.write_plus_temperature(attrib=attrib_in_nameplate,
                                                 plus_temperature=self.maxtempLineedit_shellpage.text())
                nameplate.write_voltage_current_frequency(attrib=attrib_in_nameplate)
                nameplate.write_batch_number(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_1(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_2(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_3(attrib=attrib_in_nameplate)
                nameplate.write_just_attrib_4(attrib=attrib_in_nameplate)

        block_nameplate = self.base_dxf.doc_base.blocks['nameplate']
        values = {attdef.dxf.tag: '' for attdef in block_nameplate.query('ATTDEF')}
        self.nameplate_insert_withoutcapside = self.base_dxf.doc_base.modelspace().add_blockref(
            name='nameplate',
            insert=(self.withoutcapside_insert.dxf.insert[0],
                    (self.withoutcapside_insert.dxf.insert[1] +
                        (self.withoutcapside_block.extreme_lines['y_max']-8)/(2*self.scale_class.scale))))
        self.nameplate_insert_withoutcapside.dxf.xscale = 1 / self.scale_class.scale
        self.nameplate_insert_withoutcapside.dxf.yscale = 1 / self.scale_class.scale
        self.nameplate_insert_withoutcapside.dxf.zscale = 1 / self.scale_class.scale
        self.nameplate_insert_withoutcapside.add_auto_attribs(values)
        for attrib_in_nameplate in self.nameplate_insert_withoutcapside.attribs:
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
                                              minus_temperature=self.mintempLineEdit_shellpage.text())
            nameplate.write_plus_temperature(attrib=attrib_in_nameplate,
                                             plus_temperature=self.maxtempLineedit_shellpage.text())
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
        for solid in self.base_dxf.doc_for_save.modelspace():
            if solid.dxftype() == 'INSERT':
                if 'withoutcapside' in solid.dxf.name:
                    handles[
                        solid.dxf.handle] = 0  # Set sort handle 'A' for inserts with 'withoutcapside' in their names
                else:
                    handles[solid.dxf.handle] = str(sort_handle)  # Set a unique sort handle for other inserts
                    sort_handle += 1  # Increment the sort handle for other inserts


        self.base_dxf.doc_for_save.modelspace().set_redraw_order(handles)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = MainPageDxfQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())