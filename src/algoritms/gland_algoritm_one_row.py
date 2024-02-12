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

    def check_possible_to_add_biggest_input(self):
        '''
        Проверка на то, влезут ли все самый большой кабельный ввод вообще
        :return: True or False
        '''
        self.min_size = min(self.x_end_rectangle-self.x_start_rectangle, self.y_end_rectangle - self.y_start_rectangle)
        if hasattr(self,'list_diam'):
            if max(self.list_diam) <= self.min_size:
                return True
            else:
                return False


class OneRowChecker(GlandAlgoritmChecker):
    '''Проверка установки в одну линию'''
    def __init__(self,list_glands_on_side,clearens,
                 x_start_rectanglee, x_end_rectangle,
                 y_start_rectangle, y_end_rectangle):

        self.status_add_to_possible_biggest_input = False
        self.status_add_in_one_row = False

        self.install_one_row_checker(list_glands_on_side=list_glands_on_side,
                                     clearens=clearens,
                                     x_start_rectangle=x_start_rectanglee,
                                     x_end_rectangle=x_end_rectangle,
                                     y_start_rectangle=y_start_rectangle,
                                     y_end_rectangle=y_end_rectangle)
        self.set_glands_diametrs()
        if self.check_possible_to_add_biggest_input():
            self.status_add_to_possible_biggest_input = True

            if self.check_possible_to_add_all_inputs_in_one_row():
                self.status_add_in_one_row = True
                self.calculate_x_one_row()
                self.calculate_y_one_row()
                self.calculate_new_x_start_rectangle()
                self.delete_gland_one_row()
            else:
                self.status_add_in_one_row = False
        else:
            self.status_add_to_possible_biggest_input = False

        self.set_status_add_to_possible_biggest_inputs()

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
        self.list_glands[0].set_status_add_to_possible_biggest_input(status=self.status_add_to_possible_biggest_input)

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


# class TwoRowChecker(GlandAlgoritmChecker):
#     '''Проверка установки в одну линию'''
#
#     def __init__(self, list_glands_on_side, clearens,
#                  x_start_rectanglee, x_end_rectangle,
#                  y_start_rectangle, y_end_rectangle):
#
#         self.status_add_in_two_row = False
#
#         self.install_two_row_checker(list_glands_on_side=list_glands_on_side,
#                                      clearens=clearens,
#                                      x_start_rectangle=x_start_rectanglee,
#                                      x_end_rectangle=x_end_rectangle,
#                                      y_start_rectangle=y_start_rectangle,
#                                      y_end_rectangle=y_end_rectangle)
#         self.set_glands_diametrs()
#         if self.check_possible_to_add_biggest_input():
#             if self.check_possible_to_add_all_inputs_in_one_row():
#                 self.status_add_in_one_row = True
#                 self.calculate_x_one_row()
#                 self.calculate_y_one_row()
#                 self.calculate_new_x_start_rectangle()
#                 self.delete_gland_one_row()
#             else:
#                 self.status_add_in_one_row = False
#         else:
#             self.status_add_to_possible_biggest_input = False
#
#
#     def install_two_row_checker(self, list_glands_on_side, clearens,
#                                 x_start_rectangle, x_end_rectangle,
#                                 y_start_rectangle, y_end_rectangle):
#         self.set_list_glands(list_glands_on_side=list_glands_on_side)
#         self.set_x_start_rectangle(x_start_rectangle=x_start_rectangle)
#         self.set_x_end_rectangle(x_end_rectangle=x_end_rectangle)
#         self.set_y_start_rectangle(y_start_rectangle=y_start_rectangle)
#         self.set_y_end_rectangle(y_end_rectangle=y_end_rectangle)
#
#         self.set_clearens(clearens=clearens)
#
#     '''ИХ ОБРАБОТКА'''
#
#     def check_possible_to_create_level(self):
#         '''
#         Проверка, есть ли вообще окружности, которые могут быть друг под другом
#         :param dict_with_inputs_information:{0: ['ВЗ-Н25', 37.3], 1: ['ВЗ-Н25', 37.3], 2: ['ВЗ-Н25', 37.3], 3: ['ВЗ-Н25', 37.3], 4: ['ВЗ-Н25', 37.3], 5: ['ВЗ-Н25', 37.3]}
#         :param width: 62.2
#         :return:
#         '''
#         self.status_add_in_two_row = False
#         for gland_diam_i in self.list_diam:
#             diam_width = list()
#             for gland_diam_j in self.list_diam:
#
#
#
#
#
#     def calculate_y_one_row(self):
#         '''
#         Получение координаты y для установки в одну линию
#         :return: y_coordinate
#         '''
#         self.gland_y_coordinate = self.y_start_rectangle + (self.y_end_rectangle + self.y_start_rectangle) / 2
#         self.list_glands[0].set_y_coordinate(y_coordinate=self.gland_y_coordinate)
#
#     def calculate_x_one_row(self):
#         '''
#         Получение координаты x для установки в одну линию
#         :return: x_coordinate
#         '''
#         if len(self.list_glands) != 1:
#             self.gland_x_coordinate = self.x_start_rectangle + self.list_diam[0] / 2 + self.free_space / (
#                         len(self.list_glands) + 1)
#         else:
#             self.gland_x_coordinate = self.x_start_rectangle + (self.x_end_rectangle - self.x_start_rectangle) / 2
#
#         self.list_glands[0].set_x_coordinate(x_coordinate=self.gland_x_coordinate)
#
#     def calculate_new_x_start_rectangle(self):
#         '''
#         Получение свободного пространства, чтобы равномерно раздвинуть
#         :return:
#         '''
#         if len(self.list_glands) != 1:
#             self.new_x_start_rectangle = self.x_start_rectangle + self.list_diam[
#                 0] + self.clearens + self.free_space / (len(self.list_glands) + 1)
#         else:
#             self.new_x_start_rectangle = self.x_end_rectangle
#
#     def delete_gland_one_row(self):
#         '''Удаление ввода из списка вводов
#         т.к. по одному вводу идет цикл
#         '''
#         self.list_glands.pop(0)





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









