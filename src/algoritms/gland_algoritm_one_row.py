from src.csv import gland_csv

class GlandAlgoritmChecker:

    '''УСТАНОВОЧНЫЕ ДАННЫЕ'''
    def set_x_start_rectangle(self,x_start_rectangle):
        self.x_start_rectangle = x_start_rectangle

    def set_x_end_rectangle(self,x_end_rectangle):
        self.x_end_rectangle = x_end_rectangle

    def set_y_start_rectangle(self,y_start_rectangle):
        self.y_start_rectangle = y_start_rectangle

    def set_y_end_rectangle(self,y_end_rectangle):
        self.y_end_rectangle = y_end_rectangle

    def set_list_glands(self,list_glands_on_side:list[gland_csv.CableGlandInformation]):
        self.list_glands = list_glands_on_side

    def set_clearens(self,clearens):
        self.clearens = clearens

    def set_glands_diametrs(self):
        self.list_diam = [float(gland.diametr) for gland in self.list_glands]


class BigGlandChecker(GlandAlgoritmChecker):
    '''Проверка на возможность в целом установки в самый большой кабельный ввод'''

    def __init__(self,list_glands_on_side,
                 x_start_rectangle,x_end_rectangle,
                 y_start_rectangle,y_end_rectangle):
        self.big_gland_check_setup(list_glands_on_side=list_glands_on_side,
                                   x_start_rectangle=x_start_rectangle,
                                   x_end_rectangle=x_end_rectangle,
                                   y_start_rectangle=y_start_rectangle,
                                   y_end_rectangle=y_end_rectangle)
        self.check_possible_to_add_biggest_input()


    def big_gland_check_setup(self,list_glands_on_side,
                              x_start_rectangle, x_end_rectangle,
                              y_start_rectangle, y_end_rectangle
                              ):
        self.set_list_glands(list_glands_on_side=list_glands_on_side)
        self.set_glands_diametrs()
        self.set_x_start_rectangle(x_start_rectangle=x_start_rectangle)
        self.set_x_end_rectangle(x_end_rectangle=x_end_rectangle)
        self.set_y_start_rectangle(y_start_rectangle=y_start_rectangle)
        self.set_y_end_rectangle(y_end_rectangle=y_end_rectangle)

    def check_possible_to_add_biggest_input(self):
        '''
        Проверка на то, влезут ли все самый большой кабельный ввод вообще
        :return: True or False
        '''
        self.min_size = min(self.x_end_rectangle - self.x_start_rectangle,
                            self.y_end_rectangle - self.y_start_rectangle)
        if hasattr(self, 'list_diam'):
            if len(self.list_diam) >0:
                # if self.list_diam
                if max(self.list_diam) <= self.min_size:
                    self.status_add_to_possible_biggest_input = True
                else:
                    self.status_add_to_possible_biggest_input = False

class OneRowGlandChecker(GlandAlgoritmChecker):
    '''Проверка на возможность в целом установки в самый большой кабельный ввод'''

    def __init__(self,list_glands_on_side,
                 x_start_rectangle,x_end_rectangle,
                 y_start_rectangle,y_end_rectangle,
                 clearens=5):
        self.one_row_gland_check_setup(list_glands_on_side=list_glands_on_side,
                                       x_start_rectangle=x_start_rectangle,
                                       x_end_rectangle=x_end_rectangle,
                                       y_start_rectangle=y_start_rectangle,
                                       y_end_rectangle=y_end_rectangle,
                                       clearens=clearens)
        self.check_possible_to_add_all_inputs_in_one_row()


    def one_row_gland_check_setup(self,list_glands_on_side,
                                  x_start_rectangle, x_end_rectangle,
                                  y_start_rectangle, y_end_rectangle,
                                  clearens):
        '''НЕОБХОДИМО ПЕРЕДАВАТЬ СЮДА ЛИСТ С ОСТАВШИМИСЯ КАБЕЛЬНЫМИ ВВОДАМИ ПОСЛЕ ПРОХОЖДЕНИЯ ПРОВЕРКИ НА ДВА РЯДА
        Т.Е. ПЕРВАЯ ИТЕРАЦИЯ БУДЕТ ЭТОТ АЛГОРИТМ ПРОВЕРКИ, ЕСЛИ НЕТ, ТО ИДЕТ НА ДВА РЯДА, ДВА РЯДА ДОЛЖЕН ДАВАТЬ СРАЗУ КООРДИНАТЫ ВВОДАМ
        '''
        self.set_list_glands(list_glands_on_side=list_glands_on_side)
        self.set_glands_diametrs()
        self.set_x_start_rectangle(x_start_rectangle=x_start_rectangle)
        self.set_x_end_rectangle(x_end_rectangle=x_end_rectangle)
        self.set_y_start_rectangle(y_start_rectangle=y_start_rectangle)
        self.set_y_end_rectangle(y_end_rectangle=y_end_rectangle)
        self.set_clearens(clearens=clearens)

    def check_possible_to_add_all_inputs_in_one_row(self):
        '''
        Если все ввода помещаются, и расстояние между ними = 5 мм, то значит их можно вставить
        :param free_space: max(x,y)
        :param length_clearens: вот этот клириэнс между вводами, по дефолту = 5
        :return: True or False
        '''
        self.max_size = max(self.x_end_rectangle-self.x_start_rectangle, self.y_end_rectangle - self.y_start_rectangle)
        self.len_cable_glands = sum(self.list_diam) + self.clearens * (len(self.list_diam)-1)
        self.free_space = self.max_size - self.len_cable_glands
        if self.max_size >= sum(self.list_diam) + self.clearens * (len(self.list_diam)-1):
            self.status_add_in_one_row = True
        else:
            self.status_add_in_one_row = False

class TwoRowGlandChecker(GlandAlgoritmChecker):
    '''Проверка, есть ли вообще окружности, которые могут быть друг под другом'''
    def __init__(self,list_glands_on_side,
                 x_start_rectangle,x_end_rectangle,
                 y_start_rectangle,y_end_rectangle):
        self.two_row_gland_check_setup(list_glands_on_side=list_glands_on_side,
                                       x_start_rectangle=x_start_rectangle,
                                       x_end_rectangle=x_end_rectangle,
                                       y_start_rectangle=y_start_rectangle,
                                       y_end_rectangle=y_end_rectangle)

        self.min_size = min(self.x_end_rectangle - self.x_start_rectangle,
                            self.y_end_rectangle - self.y_start_rectangle)


        self.width_for_cut = self.min_size

        '''Описание и заполнение уровней'''
        self.level_dict = dict()
        self.current_gland_index = 0

        while len(self.list_glands) > 0:

            if self.x_start_rectangle + min(self.list_diam) <= self.x_end_rectangle:
                # Всегда проверка одного ряда, каждое обновление
                if self.check_possible_to_add_all_inputs_in_one_row() and (self.width_for_cut == self.min_size):
                        self.create_level()
                        # self.calculate_x_one_row()
                        self.calculate_y_one_row()
                        self.list_glands[0].set_property_onerow_algoritm()
                        self.x_start_rectangle = self.calculate_new_x_start_rectangle()

                        self.list_glands.pop(0)
                        self.list_diam.pop(0)

                else:
                    if self.check_possible_to_create_level():
                        #Сначала сортируем список кабельнных вводов по убыванию диаметра
                        self.set_sorted_glands()
                        if self.width_for_cut == self.min_size:
                            self.create_level()
                            self.width_for_cut -= self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'][-1].diametr
                            self.x_start_rectangle = self.calculate_new_x_start_rectangle()
                            self.list_glands[0].set_property_tworow_algoritm()
                            self.list_glands.pop(0)
                            self.list_diam.pop(0)

                            while self.width_for_cut >= 0:
                                if self.search_inputs_can_insert_in_level() == True:
                                    self.add_in_current_level()
                                    self.width_for_cut -= self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'][-1].diametr
                                    self.list_glands[self.current_gland_index].set_property_tworow_algoritm()
                                    self.list_glands.pop(self.current_gland_index)
                                    self.list_diam.pop(self.current_gland_index)
                                else:
                                    break
                            step = self.width_for_cut / (len(self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'])+1)
                            clearens = 5
                            y_start = self.y_start_rectangle
                            if step >= clearens:#Проверка делается для того, что если шаг больше чем клириэнс, то просто отодвинуть ввода на шаг
                                for gland_two_row in self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands']:
                                    gland_y_coordinate = y_start + gland_two_row.diametr/2 + step
                                    y_start = gland_y_coordinate + gland_two_row.diametr/2
                                    gland_two_row.set_y_coordinate(y_coordinate=gland_y_coordinate)
                            else:
                                y_start = self.y_start_rectangle + \
                                          (self.width_for_cut -
                                          clearens * (len(self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'])-1))/2 #2x = free_space - clearens * (len(gland)-1) Нужно найти икс и прибавить к y_start
                                for gland_two_row in self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands']:
                                    gland_y_coordinate = y_start + gland_two_row.diametr/2 + clearens
                                    y_start = gland_y_coordinate + gland_two_row.diametr/2
                            self.width_for_cut = self.min_size
                    else:
                        if self.level_dict == dict():
                            self.create_level()
                            # self.calculate_x_one_row()
                            y_coordinate = self.y_start_rectangle + self.list_glands[0].diametr/2
                            self.list_glands[0].set_y_coordinate(y_coordinate=y_coordinate)
                            self.x_start_rectangle = self.list_glands[0].diametr + 5
                            self.list_glands[0].set_property_snake_algoritm()
                            self.list_glands.pop(0)
                            self.list_diam.pop(0)
                        else:
                            self.create_snake_level()
                            self.x_start_rectangle = self.level_dict[max(list(self.level_dict.keys()))]['x_insert_coordinate'] + \
                                                     self.level_dict[max(list(self.level_dict.keys()))]['level_main_diametr']/2 + \
                                                     5

                            self.list_glands[0].set_property_snake_algoritm()
                            self.list_glands.pop(0)
                            self.list_diam.pop(0)

            else:
                self.status_possible_to_create_input_all_inputs_after_algoritms = False
                break

        self.final_calculate()
        print(self.level_dict)

    def check_possible_to_add_all_inputs_in_one_row(self,clearens=5):
        '''
        Если все ввода помещаются, и расстояние между ними = 5 мм, то значит их можно вставить
        :param free_space: max(x,y)
        :param length_clearens: вот этот клириэнс между вводами, по дефолту = 5
        :return: True or False
        '''
        self.len_cable_glands = sum(self.list_diam) + clearens * (len(self.list_diam) - 1) #т.к. self.max будет меняться и может y стать максом
        if self.x_end_rectangle - self.x_start_rectangle >= self.len_cable_glands:
            return True
        else:
            return False

    def set_sorted_glands(self):
        self.list_glands = sorted(self.list_glands,key=lambda gland:gland.diametr,reverse=True)
        self.list_diam = [float(gland.diametr) for gland in self.list_glands]
    def two_row_gland_check_setup(self,list_glands_on_side,
                                  x_start_rectangle, x_end_rectangle,
                                  y_start_rectangle, y_end_rectangle
                                  ):
        '''НЕОБХОДИМО ПЕРЕДАВАТЬ СЮДА ЛИСТ С ОСТАВШИМИСЯ КАБЕЛЬНЫМИ ВВОДАМИ ПОСЛЕ ПРОХОЖДЕНИЯ ПРОВЕРКИ НА ДВА РЯДА
        Т.Е. ПЕРВАЯ ИТЕРАЦИЯ БУДЕТ ЭТОТ АЛГОРИТМ ПРОВЕРКИ, ЕСЛИ НЕТ, ТО ИДЕТ НА ДВА РЯДА, ДВА РЯДА ДОЛЖЕН ДАВАТЬ СРАЗУ КООРДИНАТЫ ВВОДАМ
        '''
        self.set_list_glands(list_glands_on_side=list_glands_on_side)
        self.set_glands_diametrs()
        # self.set_sorted_glands()
        self.set_x_start_rectangle(x_start_rectangle=x_start_rectangle)
        self.set_x_end_rectangle(x_end_rectangle=x_end_rectangle)
        self.set_y_start_rectangle(y_start_rectangle=y_start_rectangle)
        self.set_y_end_rectangle(y_end_rectangle=y_end_rectangle)

    def check_possible_to_create_level(self):
        '''
        Если все ввода помещаются, и расстояние между ними = 5 мм, то значит их можно вставить
        :param free_space: max(x,y)
        :param length_clearens: вот этот клириэнс между вводами, по дефолту = 5
        :return: True or False
        '''
        possible_create_levels = False
        if len(self.list_diam) > 1:
            for gland_diam_i in self.list_diam[1:]:
                if self.min_size >= self.list_diam[0] + gland_diam_i + 5:
                    possible_create_levels = True
                    return possible_create_levels
            return possible_create_levels

    def create_level(self):
        '''
        Создание нового уровня в словаре уровня
        :param level_dict: {номер уровня: {'x_insert': x_coordinate, список кабельных вводов:[ gland], диаметр: gland.diametr} ,
                            номер уровня +1:... }
        :return:level_dict с новой инфой {x_coordinate:[['ВЗ-Н25' : 42.6],...]}
        '''

        if self.level_dict == dict():
            number_gland_level = 0
        else:
            number_gland_level = max(list(self.level_dict.keys())) + 1

        dict_for_level_dict = dict()

        x_insert_coordinate = self.x_start_rectangle + float(self.list_glands[0].diametr) / 2
        dict_for_level_dict['x_insert_coordinate'] = x_insert_coordinate

        list_cable_glands = [self.list_glands[0]]
        dict_for_level_dict['list_cable_glands'] = list_cable_glands

        level_main_diametr = self.list_glands[0].diametr
        dict_for_level_dict['level_main_diametr'] = level_main_diametr

        self.level_dict[number_gland_level] = dict_for_level_dict

    def create_snake_level(self):
        '''
        Создание нового уровня в словаре уровня при попадании в snake
        :param level_dict: {номер уровня: {'x_insert': x_coordinate, список кабельных вводов:[ gland], диаметр: gland.diametr} ,
                            номер уровня +1:... }
        :return:level_dict с новой инфой {x_coordinate:[['ВЗ-Н25' : 42.6],...]}
        '''

        number_gland_level = int()
        if hasattr(self,'level_dict'):
            number_gland_level = max(list(self.level_dict.keys())) + 1

        dict_for_level_dict = dict()

        x_previous = self.level_dict[max(list(self.level_dict.keys()))]['x_insert_coordinate']
        if hasattr(self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'][0],'y_coordinate'):
            y_previous = self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'][0].y_coordinate
        diam_previous = self.level_dict[max(list(self.level_dict.keys()))]['level_main_diametr']

        x_start_rectangle = x_previous + diam_previous/2
        x_insert_coordinate = x_previous + \
                              ((diam_previous/2+5+self.list_glands[0].diametr/2)**2 -
                              (self.y_end_rectangle - self.list_glands[0].diametr/2 - self.y_start_rectangle - diam_previous/2)**2) \
                              ** (1/2)#ПРОВЕРИТЬ, diam один +5, потому что достаточно, если что прибавить ко второму диаметру тоже +5

        dict_for_level_dict['x_insert_coordinate'] = x_insert_coordinate

        list_cable_glands = [self.list_glands[0]]
        dict_for_level_dict['list_cable_glands'] = list_cable_glands

        level_main_diametr = self.list_glands[0].diametr
        dict_for_level_dict['level_main_diametr'] = level_main_diametr

        self.gland_x_coordinate = x_insert_coordinate
        self.gland_y_coordinate = self.y_end_rectangle * (1/2*(1 - (-1)**number_gland_level)) + ((level_main_diametr/2)*(-1)**number_gland_level)

        self.level_dict[number_gland_level] = dict_for_level_dict

    def add_in_current_level(self):
        number_current_gland_level = max(list(self.level_dict.keys()))
        self.level_dict[number_current_gland_level]['list_cable_glands'].append(self.list_glands[self.current_gland_index])

    def search_inputs_can_insert_in_level(self):
        '''
        Поиск ввода который поместится снизу
        :param free_width: свободное пространство
        :param dict_inputs: {0:['ВЗ-Н40',40], 1:['ВЗ-Н32',30], 2:['ВЗ-Н25',20]}
        :param number_input_in_second_level: 2
        :return:
        '''
        search_gland_success = False
        if self.list_glands is not None:
            if len(self.list_glands) > 0:
                for gland in self.list_glands:
                    if self.width_for_cut - 5 >= gland.diametr:
                        self.current_gland_index = self.list_glands.index(gland)
                        search_gland_success = True
                        return search_gland_success
        return search_gland_success



    def calculate_x_one_row(self):
        '''
        Получение координаты x для установки в одну линию
        :return: x_coordinate
        '''
        self.gland_x_coordinate = self.x_start_rectangle + self.list_diam[0] / 2
        self.list_glands[0].set_x_coordinate(x_coordinate=self.gland_x_coordinate)

    def calculate_y_one_row(self):
        '''
        Получение координаты y для установки в одну линию
        :return: y_coordinate
        '''
        self.gland_y_coordinate = self.y_start_rectangle + (self.y_end_rectangle - self.y_start_rectangle)/2
        self.list_glands[0].set_y_coordinate(y_coordinate=self.gland_y_coordinate)

    def calculate_new_x_start_rectangle(self,clearens=5):
        '''
        Получение свободного пространства, чтобы равномерно раздвинуть
        :return:
        '''
        if len(self.list_glands) != 1:
            self.new_x_start_rectangle = self.x_start_rectangle + \
                                         self.level_dict[max(list(self.level_dict.keys()))]['level_main_diametr'] + \
                                         clearens
        else:
            self.new_x_start_rectangle = self.x_end_rectangle
        return self.new_x_start_rectangle


    def delete_gland_one_row(self):
        '''Удаление ввода из списка вводов
        т.к. по одному вводу идет цикл
        '''
        self.list_glands.pop(0)

    def final_calculate(self):
        '''Финальный расчет после получения координат'''
        if hasattr(self,'level_dict'):
            if len(list(self.level_dict.keys())) > 0:

                self.max_size = max(self.x_end_rectangle,self.y_end_rectangle)

                free_space = self.x_end_rectangle - \
                             (self.level_dict[max(list(self.level_dict.keys()))]['x_insert_coordinate'] +
                              self.level_dict[max(list(self.level_dict.keys()))]['list_cable_glands'][0].diametr/2)

                for current_level in self.level_dict:
                    level_current_dict = self.level_dict[current_level]
                    level_current_dict['x_insert_coordinate'] += free_space / (len(list(self.level_dict.keys()))+1)
                    if len(level_current_dict['list_cable_glands']) > 0:
                        for cable_gland in level_current_dict['list_cable_glands']:
                            cable_gland.set_x_coordinate(x_coordinate=level_current_dict['x_insert_coordinate'])




class OneRowChecker(GlandAlgoritmChecker):
    '''Проверка установки в одну линию'''
    def __init__(self,list_glands_on_side,
                 x_start_rectanglee,
                 x_end_rectangle,
                 y_start_rectangle,
                 y_end_rectangle,
                 clearens):

        self.status_add_in_one_row = False

        self.install_one_row_checker(list_glands_on_side=list_glands_on_side,
                                     clearens=clearens,
                                     x_start_rectangle=x_start_rectanglee,
                                     x_end_rectangle=x_end_rectangle,
                                     y_start_rectangle=y_start_rectangle,
                                     y_end_rectangle=y_end_rectangle)
        self.set_glands_diametrs()
        self.gland_current_iteration = self.list_glands[0]
        if self.check_possible_to_add_biggest_input():
            self.status_add_to_possible_biggest_input = True

            if self.check_possible_to_add_all_inputs_in_one_row():
                self.status_add_in_one_row = True
                self.calculate_x_one_row()
                self.calculate_y_one_row()
                self.calculate_new_x_start_rectangle()
            else:
                self.status_add_in_one_row = False
        else:
            self.status_add_to_possible_biggest_input = False

        self.set_status_add_to_possible_biggest_inputs()
        self.set_status_add_in_one_row()
        self.delete_gland_one_row()

    def install_one_row_checker(self,list_glands_on_side,clearens,
                                x_start_rectangle,x_end_rectangle,
                                y_start_rectangle,y_end_rectangle):
        self.set_list_glands(list_glands_on_side=list_glands_on_side)
        self.set_x_start_rectangle(x_start_rectangle=x_start_rectangle)
        self.set_x_end_rectangle(x_end_rectangle=x_end_rectangle)
        self.set_y_start_rectangle(y_start_rectangle=y_start_rectangle)
        self.set_y_end_rectangle(y_end_rectangle=y_end_rectangle)
        self.set_clearens(clearens=clearens)

    '''ИХ ОБРАБОТКА'''

    def set_status_add_to_possible_biggest_inputs(self):
        self.gland_current_iteration.set_status_add_to_possible_biggest_input(status=self.status_add_to_possible_biggest_input)

    def set_status_add_in_one_row(self):
        self.gland_current_iteration.set_status_add_in_one_row(status=self.status_add_in_one_row)

    def check_possible_to_add_all_inputs_in_one_row(self):
        '''
        Если все ввода помещаются, и расстояние между ними = 5 мм, то значит их можно вставить
        :param free_space: max(x,y)
        :param length_clearens: вот этот клириэнс между вводами, по дефолту = 5
        :return: True or False
        '''
        self.max_size = max(self.x_end_rectangle-self.x_start_rectangle, self.y_end_rectangle - self.y_start_rectangle)
        self.len_cable_glands = sum(self.list_diam) + self.clearens * (len(self.list_diam)-1)
        self.free_space = self.max_size - self.len_cable_glands
        if self.max_size >= sum(self.list_diam) + self.clearens * (len(self.list_diam)-1):
            return True
        else:
            return False

    def calculate_y_one_row(self):
        '''
        Получение координаты y для установки в одну линию
        :return: y_coordinate
        '''
        self.gland_y_coordinate = self.y_start_rectangle + (self.y_end_rectangle + self.y_start_rectangle)/2
        self.list_glands[0].set_y_coordinate(y_coordinate=self.gland_y_coordinate)

    def calculate_x_one_row(self):
        '''
        Получение координаты x для установки в одну линию
        :return: x_coordinate
        '''
        if len(self.list_glands) != 1:
            self.gland_x_coordinate = self.x_start_rectangle + self.list_diam[0]/2 + self.free_space/(len(self.list_glands)+1)
        else:
            self.gland_x_coordinate = self.x_start_rectangle + (self.x_end_rectangle - self.x_start_rectangle)/2

        self.list_glands[0].set_x_coordinate(x_coordinate=self.gland_x_coordinate)

    def calculate_new_x_start_rectangle(self):
        '''
        Получение свободного пространства, чтобы равномерно раздвинуть
        :return:
        '''
        if len(self.list_glands) != 1:
            self.new_x_start_rectangle = self.x_start_rectangle + self.list_diam[0] + self.clearens + self.free_space/(len(self.list_glands)+1)
        else:
            self.new_x_start_rectangle = self.x_end_rectangle

    def delete_gland_one_row(self):
        '''Удаление ввода из списка вводов
        т.к. по одному вводу идет цикл
        '''
        self.list_glands.pop(0)



if __name__ == '__main__':
    list_glands = []

    vzn_dict = {'Тип': 'Кабельный ввод', 'Серия': 'ВЗ-Н', 'Типоразмер резьбы штуцера': '16', 'Типоразмер ': 'nan', 'Тип резьбы': 'М', 'Шаг резьбы': '1.5', 'Поле допуска': '6g', 'Резьба вводного штуцера': 'ФОРМУЛА!!!!', 'Модификация': 'Нет', 'Материал': 'Никелированная латунь', 'Тип кабеля': 'Небронированный', 'Металлорукав': 'Нет', 'Марка металлорукава': 'Нет', 'Трубный': 'Нет', 'Внутренняя трубная резьба, тип': 'Нет', 'Внутренняя трубная резьба, размер': 'Нет', 'Внешняя трубная резьба, тип': 'Нет', 'Внешняя трубная резьба, размер': 'Нет', 'Полное наименование': 'ВЗ-Н16', 'Мин диаметр внешнего обжатия кабеля': '3', 'Макс диаметр внешнего обжатия кабеля': '8', 'Мин диаметр обжатия внутренней оболочки': 'Нет', 'Макс диаметр обжатия внутренней оболочки': 'Нет', 'Типоразмер плоского кабеля': 'Нет', 'Тип внутренней резьбы переходника': 'Нет', 'Резьба внутренняя резьба переходника': 'Нет', 'Размер под ключ': '24', 'Описаный диаметр кабельного ввода': '29.6', 'Наружный диаметр заглушки, пробки, кольца, шайбы': 'Нет', 'Внутренний диаметр заглушки, пробки, кольца, шайбы': 'Нет', 'Толщина заглушки или материала': 'Нет', 'Внутренний диаметр чехла защитного': 'nan', 'Наружний диаметр чехла защитного': 'nan', 'Внутренний диаметр прохода кольца заземления': 'nan', 'Диаметр отверстия под провод заземления': 'nan', 'Внутренний диаметр прохода рифленой шайбы': 'nan', 'Охранная зона Ex e': '36', 'Охранная зона Ex d': 'nan', 'Длина, мм': '47', 'Масса, г': 84.0, 'Температура эксплуатации мин': -60.0, 'Температура эксплуатации макс': 230.0, 'IP': '66;67;68', 'Климатическое исполнение': 'УХЛ1', 'Маркировки взрывозащиты Ex d': '1Ex d IIC Gb', 'Маркировки взрывозащиты Ex e': '1Ex e IIC Gb', 'Маркировки взрывозащиты Ex i': '0Ex ia IIC Ga', 'Маркировки взрывозащиты Ex  n': '2Ex nR IIC Gc', 'Маркировки взрывозащиты Ex  tb': 'Ex ta IIIC Da', 'Маркировка взрывозащиты 5': 'nan', 'Маркировка взрывозащиты 6': 'nan', 'Маркировка взрывозащиты 7': 'nan', 'Маркировка взрывозащиты 8': 'nan', 'Маркировки взрывозащиты Ex  РВ, РО,РП,РН': 'nan', 'Актуальность': 'Да', 'Сертификат ТР ТС 012': 'ЕАЭС RU C-RU.МЮ62.В.01285/19', 'Срок действия , до ': '23.10.2024', 'Ссылка': 'nan', 'Сертификат РМ РС': 'nan', 'Срок действия , до .1': 'nan', 'Ссылка.1': 'nan', 'Сертификат Интергазсерт': 'nan', 'Срок действия , до .2': 'nan', 'Ссылка.2': 'nan', 'Сертификат сейсмика': 'nan', 'Срок действия , до .3': 'nan', 'Ссылка.3': 'nan', 'Сертификат': 'nan', 'Срок действия , до .4': 'nan', 'Ссылка.4': 'nan', 'Сертификат.1': 'nan', 'Срок действия , до .5': 'nan', 'Ссылка.5': 'nan', 'Сертификат.2': 'nan', 'Срок действия , до .6': 'nan', 'Ссылка.6': 'nan', 'Сертификат.3': 'nan', 'Срок действия , до .7': 'nan', 'Ссылка.7': 'nan', 'Сертификат.4': 'nan', 'Срок действия , до .8': 'nan', 'Ссылка.8': 'nan', 'Сертификат.5': 'nan', 'Срок действия , до .9': 'nan', 'Ссылка.9': 'nan', 'Сертификат.6': 'nan', 'Срок действия , до .10': 'nan', 'Ссылка.10': 'nan', 'Изображение чертеж (путь)': 'nan', 'Изображение рендер (путь)': 'nan', 'Чертеж основной': 'ВРПТ.305311.001', 'Исполнение': 16.0, 'Актуальность.1': 'Да', 'Стоимость': 'nan', 'Описание': 'nan', 'Отличительные особенности': 'Эластомерные уплотнительные кольца с широким температурным диапазоном эксплуатации;Повышенная стойкость к агрессивным средам;Удобный монтаж с помощью стандартных ключей;Широкий диапазон обжатий; Широкий номенклатурный рядтипоразмеров', 'Аналог 1': 'nan', 'Аналог 2': 'nan', 'Аналог 3': 'nan'}
    for i in range(0,3):
        gland = gland_csv.CableGlandInformation(gland_dict=vzn_dict)
        list_glands.append(gland)
    list_glands_for_delete = list_glands.copy()


    x_start_rectangle = 0
    y_start_rectangle = 8
    x_end_rectangle = 98.9
    y_end_rectangle = 64.1

    while len(list_glands_for_delete) > 0:

        first_check = OneRowChecker(list_glands_on_side=list_glands_for_delete,
                                    x_start_rectanglee=x_start_rectangle,
                                    y_start_rectangle=y_start_rectangle,
                                    x_end_rectangle=x_end_rectangle,
                                    y_end_rectangle=y_end_rectangle,
                                    clearens=5)
        if hasattr(first_check,'new_x_start_rectangle'):
            x_start_rectangle = first_check.new_x_start_rectangle


    print(list_glands)









