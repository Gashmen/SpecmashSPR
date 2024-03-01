import transliterate

from ezdxf.layouts.layout import Modelspace
from ezdxf.document import Drawing

from src.draw.base import DxfBase
from src.csv.shell_csv import Shell_csv
from src.algoritms import gland_algoritm_one_row
from src.csv.gland_csv import CableGlandInformation
from src.Widgets_Custom import UI_BaseError

class ShellBaseDxf:
    '''
    Базовый класс оболочки DXF, информацию с класса используют все виды оболочки (topside,leftside...)
    shell_dict:
    {'Производитель': 'ВЗОР', 'Серия': 'ВП', 'Типоразмер': 161610, 'Взрывозащита': 'Exe', 'Материал': 'Пластик',
    'Цвет(RAL)': 9005, 'Температура минимальная': -60, 'Температура максимальная': 130, 'IP': '66;67', 'Крепление': nan,
    '8': nan, '9': nan, '10': nan, 'Ширина': 160.0, 'Длина': 160.0, 'Глубина': 100.0, 'Масса': '0.73', 'Толщина стенки': '6',
    'Зона Сверловки AB Ш': nan, 'Зона Сверловки БГ Ш': nan, 'Внутренние размеры AB': 120, 'Внутренние размеры БГ': 98,
    'Межосевое расстояние для DIN': nan, 'Кол-во отверстий': nan, 'Расстояния болтов вдоль АВ': nan, 'Расстояния болтов вдоль БГ': nan,
    'Количество болтов': nan, 'Внутренняя высота коробки': 75.0,
    'Маркировка взрывозащиты': '1Ex e IIC;0Ex ia IIC;1Ex ib IIB;1Ex e[ia Ga] IIC;1Ex e mb IIC;1Ex e db IIC;1Ex e db mb IIC;1Ex e db [ia Ga] IIC;1Ex e db [ib] IIC;1Ex e mb ia IIC;1Ex e db mb ia IIC;--Ex tb IIIC;Ex ta IIIC;', 'Наличие': True}
    '''
    def __init__(self,shell_dict:dict):
        if isinstance(shell_dict,dict):
            self.shell_dict = shell_dict

    def set_russian_name_shell(self):
        '''Получение русского имени оболочки'''
        if hasattr(self,'shell_dict'):
            self.shell_russian_name = self.shell_dict['Серия'] + '.' + str(self.shell_dict['Типоразмер'])

    def set_translit_name(self):
        '''Получение транслита имени'''
        if hasattr(self,'shell_russian_name'):
            self.shell_translit_name = transliterate.translit(self.shell_russian_name, language_code='ru', reversed=True)

    def check_possible_to_draw(self, dxf_base: DxfBase):
        '''Проверка на наличие в базе dxf оболочки'''
        if isinstance(dxf_base,DxfBase):
            return dxf_base.check_shell(shell_translite_name=self.shell_translit_name)

    def get_shell_block_names(self):

        if hasattr(self,'shell_translit_name'):
            shell_blocks_end = ('topside','upside','downside',
                                 'leftside','rightside','withoutcapside',
                                 'cutside','installation_dimensions')
            self.shell_blocks_names = [self.shell_translit_name + '_' + end for end in shell_blocks_end]


    def set_shell_csv_finished(self,shell_finished_csv:Shell_csv):
        '''Передача всей информации с Qt и csv заполненой информацией оболочки на dxf'''
        if isinstance(shell_finished_csv,Shell_csv):
            self.shell_finished_csv = shell_finished_csv

class ShellSideBlock(DxfBase):

    def set_doc_base(self,doc_base: Drawing):
        '''
        Установка doc
        :param doc: doc_base общая dxf база
        :return:
        '''
        self.doc_base = doc_base

    def set_shell_side_name(self,translit_name,side_dxf_name):
        '''
        Установить имя блока в dxf
        :param translit_name:VP.161610
        :param side: topside or downside or upside...
        :return:VP.161610_topside
        '''
        self.side_dxf_name = side_dxf_name
        self.shell_side_name = translit_name + '_' + side_dxf_name

    def set_block_from_dxf_base(self):
        '''Получение блока shell name_topside'''
        self.get_block(block_name=self.shell_side_name)

    def set_side_russian_name(self,side_russian_name):
        self.side_russian_name = side_russian_name

    def set_dict_glands_all_sizes(self,glands_on_sides_dict):
        self.glands_on_sides_dict = glands_on_sides_dict

    def set_status_painting_side(self):
        '''Передать список glands, чтобы поставить статус, что рисуется, а что не рисуется'''
        if len(self.glands_on_sides_dict[self.side_russian_name]) <0:
            self.status_painting_side = False
        else:
            self.status_painting_side = True

    def search_polyline(self):
        '''Установка полилинии'''
        self.polyline = PolylineSurfaceOnSideDxf()
        self.polyline.set_main_coordinates(block=self.block)
        if hasattr(self,'side_dxf_name'):# задаются координаты Полилинии
            self.polyline.side = self.side_dxf_name  # Имя стороны по последней части имени в блоке

    def check_possible_to_add_all_gland(self):
        '''Проверка на всех кабельных вводов на сторону'''
        if hasattr(self, 'side_russian_name'):
            self.list_glands = self.glands_on_sides_dict[self.side_russian_name]
            if len(self.list_glands) >0:

                x_start_rectangle = self.polyline.x0
                x_end_rectangle = self.polyline.x1
                y_start_rectangle = self.polyline.y0
                y_end_rectangle = self.polyline.y1

                area_rectangle_polyline = (x_end_rectangle-x_start_rectangle) * (y_end_rectangle-y_start_rectangle)
                area_rectangle_glands = sum([(3.14 * gland.diametr * gland.diametr /4 ) for gland in self.list_glands])

                if area_rectangle_polyline >= area_rectangle_glands:
                    return True
                else:
                    return False
            else:
                return False


    def check_possible_to_add_biggest_gland(self):
        '''Проверка на помещение самого большого кабельного ввода на сторону'''
        if hasattr(self,'side_russian_name'):
            self.list_glands = self.glands_on_sides_dict[self.side_russian_name]
            if len(self.list_glands) >0:
                x_start_rectangle = self.polyline.x0
                x_end_rectangle = self.polyline.x1
                y_start_rectangle = self.polyline.y0
                y_end_rectangle = self.polyline.y1

                self.biggest_check = gland_algoritm_one_row.BigGlandChecker(list_glands_on_side=self.list_glands,
                                                                       x_start_rectangle=x_start_rectangle,
                                                                       y_start_rectangle=y_start_rectangle,
                                                                       x_end_rectangle=x_end_rectangle,
                                                                       y_end_rectangle=y_end_rectangle,
                                                                       )
                return self.biggest_check.status_add_to_possible_biggest_input


    def check_possible_to_add_in_one_row(self):
        '''Проверка на помещение самого большого кабельного ввода на сторону'''
        if hasattr(self,'side_russian_name'):
            self.list_glands = self.glands_on_sides_dict[self.side_russian_name]
            if len(self.list_glands) > 0:

                x_start_rectangle = self.polyline.x0
                x_end_rectangle = self.polyline.x1
                y_start_rectangle = self.polyline.y0
                y_end_rectangle = self.polyline.y1

                self.one_row_check = gland_algoritm_one_row.OneRowGlandChecker(list_glands_on_side=self.list_glands,
                                                                               x_start_rectangle=x_start_rectangle,
                                                                               y_start_rectangle=y_start_rectangle,
                                                                               x_end_rectangle=x_end_rectangle,
                                                                               y_end_rectangle=y_end_rectangle,
                                                                               )
                return self.one_row_check.status_add_in_one_row

    def calculate_coordinates_glands_two_row(self):
        if hasattr(self,'side_russian_name'):
            self.list_glands = self.glands_on_sides_dict[self.side_russian_name].copy()
            if len(self.list_glands) > 0:

                x_start_rectangle = self.polyline.x0
                x_end_rectangle = self.polyline.x1
                y_start_rectangle = self.polyline.y0
                y_end_rectangle = self.polyline.y1

                self.two_row_calculate = gland_algoritm_one_row.TwoRowGlandChecker(list_glands_on_side=self.list_glands,
                                                                                   x_start_rectangle=x_start_rectangle,
                                                                                   y_start_rectangle=y_start_rectangle,
                                                                                   x_end_rectangle=x_end_rectangle,
                                                                                   y_end_rectangle=y_end_rectangle,
                                                                                   )
                self.list_glands = self.two_row_calculate.list_glands

    def calculate_coordinate_glands_one_row(self):
        '''Рассчет координат '''
        if hasattr(self,'side_russian_name'):
            self.list_glands = self.glands_on_sides_dict[self.side_russian_name]
            list_glands_for_delete = self.list_glands.copy()

            x_start_rectangle = self.polyline.x0
            x_end_rectangle = self.polyline.x1
            y_start_rectangle = self.polyline.y0
            y_end_rectangle = self.polyline.y1



            ###################
            # ДЛЯ ВТОРОГО УРОВНЯ
            ###################
            level_dict = dict()

            while len(list_glands_for_delete)>0:
                first_check = gland_algoritm_one_row.OneRowChecker(list_glands_on_side=list_glands_for_delete,
                                                                   x_start_rectanglee=x_start_rectangle,
                                                                   y_start_rectangle=y_start_rectangle,
                                                                   x_end_rectangle=x_end_rectangle,
                                                                   y_end_rectangle=y_end_rectangle,
                                                                   clearens=5)

                if first_check.status_add_in_one_row == False:
                    break

                if hasattr(first_check, 'new_x_start_rectangle'):
                    x_start_rectangle = first_check.new_x_start_rectangle


    def draw_glands_in_block(self):
        if hasattr(self,'list_glands'):
            if len(self.list_glands) > 0:
                for cable_gland_information in self.list_glands:
                    self.block.add_blockref(name=cable_gland_information.gland_dxf_name + '_exe',
                                            insert=(cable_gland_information.x_coordinate,
                                                    cable_gland_information.y_coordinate))

    def add_gland_in_block(self):
        '''Вставка кабельных вводов в блок'''


        if hasattr(self,'two_row_calculate'):
            if hasattr(self.two_row_calculate,'level_dict'):
                if len(list(self.two_row_calculate.level_dict.keys()))>0:
                    '''self.two_row_calculate.level_dict:
                       {0: {'x_insert_coordinate': 10.95, 'list_cable_glands': [<src.csv.gland_csv.CableGlandInformation object at 0x0000024BEC0BBBE0>, <src.csv.gland_csv.CableGlandInformation object at 0x0000024BEC0BBA30>], 'level_main_diametr': 21.9}, 
                       1: {'x_insert_coordinate': 37.849999999999994, 'list_cable_glands': [<src.csv.gland_csv.CableGlandInformation object at 0x0000024BEC0BB490>], 'level_main_diametr': 21.9}, 
                       2: {'x_insert_coordinate': 64.75, 'list_cable_glands': [<src.csv.gland_csv.CableGlandInformation object at 0x0000024BEC0BB850>], 'level_main_diametr': 21.9}, 
                       3: {'x_insert_coordinate': 91.64999999999999, 'list_cable_glands': [<src.csv.gland_csv.CableGlandInformation object at 0x0000024BEC0BB880>], 'level_main_diametr': 21.9}
                       }'''
                    for level_gland in self.two_row_calculate.level_dict:
                        level_information = self.two_row_calculate.level_dict[level_gland]
                        for cable_gland in level_information['list_cable_glands']:
                            self.block.add_blockref(cable_gland.gland_dxf_name + '_exe',
                                                    insert=(cable_gland.x_coordinate,cable_gland.y_coordinate))


    # def calculate_max_length_gland(self):
    #     if hasattr(self,'glands_on_sides_dict'):
    #         if self.glands_on_sides_dict[self.side_russian_name] != []:
    #             if hasattr(self,'two_row_calculate'):


    def delete_inserts(self):
        for insert in self.doc_base.blocks[self.shell_side_name].query('INSERT'):
            self.doc_base.blocks[self.shell_side_name].delete_entity(insert)

class ShellTopSideBlock(ShellSideBlock):

    def __init__(self,translit_name,doc_base:Drawing,glands_on_sides_dict):
        '''
        Построение топсайда у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''

        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='topside')
        self.set_side_russian_name(side_russian_name='Крышка')
        self.set_dict_glands_all_sizes(glands_on_sides_dict=glands_on_sides_dict)
        self.set_block_from_dxf_base()
        self.set_status_painting_side()
        self.search_polyline()


    def draw_topside_insert(self):
        '''
        Создает shell_topside в координатах 0,0
        НУЖНО БУДЕТ УЧЕСТЬ МАСШТАБ И КАК ДВИГАЕТСЯ ОТНОСИТЕЛЬНО РАМКИ
        :param doc: пустой лист со вставленными импортами блоками
        :param shell_name: VP.161610
        :return: topside_insert вставленный на моделспейс
        '''
        self.topside_insert = self.doc_base.modelspace().add_blockref(name=self.shell_topside_name,
                                                                      insert=(0,0))

    def draw_topside_exe_glands(self):
        self.delete_inserts()
        if self.glands_on_sides_dict[self.side_russian_name] != list():
            for gland in self.glands_on_sides_dict[self.side_russian_name]:
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_exe',
                    insert=(gland.x_coordinate,
                            gland.y_coordinate))

    def draw_leftside_glands(self, leftside_extreme_lines, added_gland_dxf_name='_leftside'):
        if self.glands_on_sides_dict['Г'] != list():
            for gland in sorted(self.glands_on_sides_dict['Г'], key=lambda x: x.y_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + added_gland_dxf_name,
                    insert=(self.extreme_lines['x_min'],
                            leftside_extreme_lines['x_max'] - gland.x_coordinate + self.extreme_lines['y_min']
                            ))
                gland_insert.dxf.rotation = 270

    def draw_rightside_glands(self, rightside_extreme_lines, added_gland_dxf_name='_rightside'):
        if self.glands_on_sides_dict['Б'] != list():
            for gland in sorted(self.glands_on_sides_dict['Б'], key=lambda x: x.y_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + added_gland_dxf_name,
                    insert=(self.extreme_lines['x_max'],
                            gland.x_coordinate - rightside_extreme_lines['x_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 90

    def draw_upside_glands(self, upside_extreme_lines, added_gland_dxf_name='_upside'):
        if self.glands_on_sides_dict['А'] != list():
            for gland in sorted(self.glands_on_sides_dict['А'], key=lambda x: x.y_coordinate, reverse=False):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + added_gland_dxf_name,
                    insert=(upside_extreme_lines['x_max'] - gland.x_coordinate + self.extreme_lines['x_min'],
                            self.extreme_lines['y_max']))
                gland_insert.dxf.rotation = 180

    def draw_downside_glands(self, downside_extreme_lines,added_gland_dxf_name='_downside'):
        if self.glands_on_sides_dict['В'] != list():
            for gland in sorted(self.glands_on_sides_dict['В'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + added_gland_dxf_name,
                    insert=(gland.x_coordinate - downside_extreme_lines['x_min'] + self.extreme_lines['x_min'],
                            self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 0

class ShellDownSideBlock(ShellSideBlock):

    def __init__(self,translit_name,doc_base:Drawing,glands_on_sides_dict):
        '''
        Построение downside у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='downside')
        self.set_side_russian_name(side_russian_name='В')
        self.set_dict_glands_all_sizes(glands_on_sides_dict=glands_on_sides_dict)
        self.set_block_from_dxf_base()
        self.set_status_painting_side()
        self.search_polyline()
    def draw_downside_exe_glands(self):
        self.delete_inserts()
        if self.glands_on_sides_dict[self.side_russian_name] != list():
            for gland in self.glands_on_sides_dict[self.side_russian_name]:
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_exe',
                    insert=(gland.x_coordinate,
                            gland.y_coordinate))

    def draw_leftside_glands(self, leftside_extreme_lines):
        if self.glands_on_sides_dict['Г'] != list():
            for gland in sorted(self.glands_on_sides_dict['Г'], key=lambda x: x.x_coordinate, reverse=False):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_leftside',
                    insert=(self.extreme_lines['x_min'],
                            gland.y_coordinate - leftside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 270

    def draw_rightside_glands(self, rightside_extreme_lines):
        if self.glands_on_sides_dict['Б'] != list():
            for gland in sorted(self.glands_on_sides_dict['Б'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_rightside',
                    insert=(self.extreme_lines['x_max'],
                            gland.y_coordinate - rightside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 90

    def draw_topside_glands(self, topside_extreme_lines):
        if self.glands_on_sides_dict['Крышка'] != list():
            for gland in sorted(self.glands_on_sides_dict['Крышка'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_topside',
                    insert=(gland.y_coordinate - topside_extreme_lines['y_min'] - self.extreme_lines['x_min'],
                            self.extreme_lines['y_max']))
                gland_insert.dxf.rotation = 180

class ShellUpSideBlock(ShellSideBlock):
    def __init__(self,translit_name,doc_base:Drawing,glands_on_sides_dict):
        '''
        Построение downside у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='upside')
        self.set_side_russian_name(side_russian_name='А')
        # self.set_dict_glands_all_sizes(glands_on_sides_dict=glands_on_sides_dict)
        self.set_block_from_dxf_base()
        # self.set_status_painting_side()
        self.search_polyline()

    def draw_upside_exe_glands(self):
        self.delete_inserts()
        if self.glands_on_sides_dict[self.side_russian_name] != list():
            for gland in self.glands_on_sides_dict[self.side_russian_name]:
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_exe',
                    insert=(gland.x_coordinate,
                            gland.y_coordinate))


    def draw_leftside_glands(self, leftside_extreme_lines):
        if self.glands_on_sides_dict['Г'] != list():
            for gland in sorted(self.glands_on_sides_dict['Г'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_leftside',
                    insert=(self.extreme_lines['x_max'],
                            gland.y_coordinate - leftside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 90

    def draw_rightside_glands(self, rightside_extreme_lines):
        if self.glands_on_sides_dict['Б'] != list():
            for gland in sorted(self.glands_on_sides_dict['Б'], key=lambda x: x.x_coordinate, reverse=False):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_rightside',
                    insert=(self.extreme_lines['x_min'],
                            gland.y_coordinate - rightside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 270

    def draw_topside_glands(self, topside_extreme_lines):
        if self.glands_on_sides_dict['Крышка'] != list():
            for gland in sorted(self.glands_on_sides_dict['Крышка'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_topside',
                    insert=(gland.y_coordinate - topside_extreme_lines['y_min'] - self.extreme_lines['x_min'],
                            self.extreme_lines['y_max']))
                gland_insert.dxf.rotation = 180


class ShellLeftSideBlock(ShellSideBlock):
    def __init__(self,translit_name,doc_base:Drawing,glands_on_sides_dict):
        '''
        Построение downside у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='leftside')
        self.set_side_russian_name(side_russian_name='Г')
        self.set_dict_glands_all_sizes(glands_on_sides_dict=glands_on_sides_dict)
        self.set_block_from_dxf_base()
        self.search_polyline()

    def draw_leftside_exe_glands(self):
        self.delete_inserts()
        if self.glands_on_sides_dict[self.side_russian_name] != list():
            for gland in self.glands_on_sides_dict[self.side_russian_name]:
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_exe',
                    insert=(gland.x_coordinate,
                            gland.y_coordinate))

    def draw_upside_glands(self, upside_extreme_lines):
        if self.glands_on_sides_dict['А'] != list():
            for gland in sorted(self.glands_on_sides_dict['А'], key=lambda x: x.x_coordinate, reverse=False):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_upside',
                    insert=(self.extreme_lines['x_min'],
                            gland.y_coordinate - upside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 270

    def draw_downside_glands(self, downside_extreme_lines):
        if self.glands_on_sides_dict['В'] != list():
            for gland in sorted(self.glands_on_sides_dict['В'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_downside',
                    insert=(self.extreme_lines['x_max'],
                            gland.y_coordinate - downside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 90

    def draw_topside_glands(self, topside_extreme_lines):
        if self.glands_on_sides_dict['Крышка'] != list():
            for gland in sorted(self.glands_on_sides_dict['Крышка'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_topside',
                    insert=(gland.y_coordinate - topside_extreme_lines['y_min'] - self.extreme_lines['x_min'],
                            self.extreme_lines['y_max']))
                gland_insert.dxf.rotation = 180


class ShellRightSideBlock(ShellSideBlock):
    def __init__(self,translit_name,doc_base:Drawing,glands_on_sides_dict):
        '''
        Построение downside у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='rightside')
        self.set_side_russian_name(side_russian_name='Б')
        self.set_dict_glands_all_sizes(glands_on_sides_dict=glands_on_sides_dict)
        self.set_block_from_dxf_base()
        self.search_polyline()

    def draw_rightside_exe_glands(self):
        self.delete_inserts()
        for gland in self.glands_on_sides_dict[self.side_russian_name]:
            gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                                                                    name=gland.gland_dxf_name + '_exe',
                                                                    insert=(gland.x_coordinate,
                                                                            gland.y_coordinate))
    def draw_upside_glands(self,upside_extreme_lines):
        for gland in sorted(self.glands_on_sides_dict['А'], key=lambda x:x.x_coordinate, reverse=True):
            gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                               name=gland.gland_dxf_name + '_upside',
                               insert=(self.extreme_lines['x_max'], gland.y_coordinate - upside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
            gland_insert.dxf.rotation = 90

    def draw_downside_glands(self,downside_extreme_lines):
        for gland in sorted(self.glands_on_sides_dict['В'], key=lambda x:x.x_coordinate, reverse=False):
            gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                               name=gland.gland_dxf_name + '_downside',
                               insert=(self.extreme_lines['x_min'], gland.y_coordinate - downside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
            gland_insert.dxf.rotation = 270

    def draw_topside_glands(self,topside_extreme_lines):
        for gland in sorted(self.glands_on_sides_dict['Крышка'], key=lambda x:x.x_coordinate, reverse=True):
            gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                               name=gland.gland_dxf_name + '_topside',
                               insert=(gland.y_coordinate - topside_extreme_lines['y_min'] - self.extreme_lines['x_min'],
                                       self.extreme_lines['y_max']))
            gland_insert.dxf.rotation = 180

class ShellCutSideBlock(ShellSideBlock):

    def __init__(self, translit_name, doc_base: Drawing):
        '''
        Построение cutside у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='cutside')
        self.set_block_from_dxf_base()

    def draw_upside_glands(self, upside_extreme_lines):
        self.delete_inserts()
        if self.glands_on_sides_dict['А'] != list():
            for gland in sorted(self.glands_on_sides_dict['А'], key=lambda x: x.x_coordinate, reverse=False):
                if gland.x_coordinate <= (upside_extreme_lines['x_max'] + upside_extreme_lines['x_min'])/2:
                    gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                        name=gland.gland_dxf_name + '_upside',
                        insert=(self.extreme_lines['x_min'],
                                gland.y_coordinate - upside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                    gland_insert.dxf.rotation = 270

    def draw_downside_glands(self, downside_extreme_lines):
        if self.glands_on_sides_dict['В'] != list():
            for gland in sorted(self.glands_on_sides_dict['В'], key=lambda x: x.x_coordinate, reverse=True):
                if gland.x_coordinate >= (downside_extreme_lines['x_max'] + downside_extreme_lines['x_min']) / 2:
                    gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                        name=gland.gland_dxf_name + '_downside',
                        insert=(self.extreme_lines['x_max'],
                                gland.y_coordinate - downside_extreme_lines['y_min'] + self.extreme_lines['y_min']))
                    gland_insert.dxf.rotation = 90

    def draw_topside_glands(self, topside_extreme_lines):
        if self.glands_on_sides_dict['Крышка'] != list():
                for gland in sorted(self.glands_on_sides_dict['Крышка'], key=lambda x: x.x_coordinate, reverse=True):
                    if gland.x_coordinate >= (topside_extreme_lines['x_max'] + topside_extreme_lines['x_min']) / 2:
                        gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                            name=gland.gland_dxf_name + '_topside',
                            insert=(gland.y_coordinate - topside_extreme_lines['y_min'] - self.extreme_lines['x_min'],
                                    self.extreme_lines['y_max']))
                        gland_insert.dxf.rotation = 180

class ShellWithoutcapsideBlock(ShellSideBlock):

    def __init__(self, translit_name, doc_base: Drawing):
        '''
        Построение installation_dimension у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='withoutcapside')
        self.set_block_from_dxf_base()

    def draw_leftside_glands(self, leftside_extreme_lines):
        self.delete_inserts()
        if self.glands_on_sides_dict['Г'] != list():
            for gland in sorted(self.glands_on_sides_dict['Г'], key=lambda x: x.y_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_withoutcapside',
                    insert=(self.extreme_lines['x_min'],
                            leftside_extreme_lines['x_max'] - gland.x_coordinate + self.extreme_lines['y_min']
                            ))
                gland_insert.dxf.rotation = 270

    def draw_rightside_glands(self, rightside_extreme_lines):
        if self.glands_on_sides_dict['Б'] != list():
            for gland in sorted(self.glands_on_sides_dict['Б'], key=lambda x: x.y_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_withoutcapside',
                    insert=(self.extreme_lines['x_max'],
                            gland.x_coordinate - rightside_extreme_lines['x_min'] + self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 90

    def draw_upside_glands(self, upside_extreme_lines):
        if self.glands_on_sides_dict['А'] != list():
            for gland in sorted(self.glands_on_sides_dict['А'], key=lambda x: x.y_coordinate, reverse=False):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_withoutcapside',
                    insert=(upside_extreme_lines['x_max'] - gland.x_coordinate + self.extreme_lines['x_min'],
                            self.extreme_lines['y_max']))
                gland_insert.dxf.rotation = 180

    def draw_downside_glands(self, downside_extreme_lines):
        if self.glands_on_sides_dict['В'] != list():
            for gland in sorted(self.glands_on_sides_dict['В'], key=lambda x: x.x_coordinate, reverse=True):
                gland_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
                    name=gland.gland_dxf_name + '_withoutcapside',
                    insert=(gland.x_coordinate - downside_extreme_lines['x_min'] + self.extreme_lines['x_min'],
                            self.extreme_lines['y_min']))
                gland_insert.dxf.rotation = 0

    def draw_din(self):
        din_base = DxfBase()
        din_base.doc_base = self.doc_base
        din_base.get_block(block_name='DIN_' + self.shell_side_name.split('_')[0])
        din_base.define_extreme_lines()
        self.din_length = din_base.extreme_lines['x_max'] - din_base.extreme_lines['x_min']

        self.din_insert = self.doc_base.blocks[self.shell_side_name].add_blockref(
            name = 'DIN_' + self.shell_side_name.split('_')[0],
            insert=(0,0))
        self.din_insert.dxf.rotation = 0


class ShellInstallationBlock(ShellSideBlock):
    def __init__(self, translit_name, doc_base: Drawing):
        '''
        Построение installation_dimension у оболочки
        :param translit_name: VP.161610
        :param doc:Drawing
        :param glands_on_sides_dict:{"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        '''
        self.set_doc_base(doc_base=doc_base)
        self.set_shell_side_name(translit_name=translit_name,
                                 side_dxf_name='installation_dimensions')
        self.set_block_from_dxf_base()




class PolylineSurfaceOnSideDxf:

    def __init__(self):
        self._side = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self,value):
        self._side = value

    def set_main_coordinates(self,block):
        '''
        Передача каждой координате данных
        :param surface_coordinates: {'xy0': [0.0, 8.0], 'xy1': [120.0, 71.8]}
        '''

        self.get_lwpolyline_coordinate(block=block)
        self.define_rectangle_size_for_inputs()
        if isinstance(self.surface_coordinates,dict):
            if self.surface_coordinates.__getitem__('xy0') and self.surface_coordinates.__getitem__('xy1'):
                self.x0 = self.surface_coordinates['xy0'][0]
                self.y0 = self.surface_coordinates['xy0'][1]
                self.x1 = self.surface_coordinates['xy1'][0]
                self.y1 = self.surface_coordinates['xy1'][1]


    def get_lwpolyline_coordinate(self,block):
        self.polyline_xy_coordinate_side = {'x': [], 'y': []}
        lwpolyline = block.query('LWPOLYLINE')[0]
        if lwpolyline is not None:
            lwpolyline.dxf.color = 255#чтобы все были белыми, если при добавлении в базу что-то случится
            for xy_coordinate in lwpolyline.get_points():
                self.polyline_xy_coordinate_side['x'].append(round(xy_coordinate[0], 1))
                self.polyline_xy_coordinate_side['y'].append(round(xy_coordinate[1], 1))
            self.polyline_xy_coordinate_side['x'] = tuple(sorted(set(self.polyline_xy_coordinate_side['x'])))
            self.polyline_xy_coordinate_side['y'] = tuple(sorted(set(self.polyline_xy_coordinate_side['y'])))
        else:
            raise BaseException('Нет полилинии в блоке')

    def define_rectangle_size_for_inputs(self):
        if hasattr(self,'polyline_xy_coordinate_side'):
            self.surface_coordinates = {}
            if len(self.polyline_xy_coordinate_side['y']) == 2:  # главное по высоте проверить
                self.surface_coordinates['xy0'] = [self.polyline_xy_coordinate_side['x'][0], self.polyline_xy_coordinate_side['y'][0]]
                self.surface_coordinates['xy1'] = [self.polyline_xy_coordinate_side['x'][1], self.polyline_xy_coordinate_side['y'][1]]
            else:
                self.surface_coordinates['xy0'] = [self.polyline_xy_coordinate_side['x'][0], self.polyline_xy_coordinate_side['y'][-2]]
                self.surface_coordinates['xy1'] = [self.polyline_xy_coordinate_side['x'][-1], self.polyline_xy_coordinate_side['y'][-1]]
        else:
            print('Непонятная ошибка draw.shell_side.dxf_shell.define_rectangle_size_for_inputs')


