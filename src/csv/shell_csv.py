import os

import pandas as pd

class Shell_csv:

    def __init__(self,shell_csv_path):
        self.shell_csv_path = shell_csv_path
        self.shell_main_dict = self.get_main_dict(main_path=self.shell_csv_path)
        self.shell_main_dict_copy = self.shell_main_dict.copy()


    def set_shell_csv_path(self,shell_csv_path):
        '''
        Если надо будет переопределить путь до shell_csv
        Например если к серверу не будет подключения
        '''
        self.shell_csv_path = shell_csv_path

    def get_main_dict(self,main_path:str) ->dict:

        '''
        :param main_path: main_path = os.getcwd() + '\Общая база'
        :return: main_dict
         {0: {'Производитель': 'ВЗОР', 'Серия': 'ВА', 'Типоразмер': 80807, 'Взрывозащита': 'Exe', 'Материал': 'Алюминий', 'Цвет(RAL)': nan,...},
         {1: {'Производитель': 'ВЗОР', 'Серия': 'ВА', 'Типоразмер': 121209, 'Взрывозащита': 'Exe', 'Материал': 'Алюминий', 'Цвет(RAL)': 7042,...},
        '''

        main_dict = pd.read_csv(main_path,delimiter=';').to_dict('index')

        return main_dict

    '''не используется'''
    def get_unique_manufacturer(self,main_dict):
        '''
        :param main_dict: {0: {'Производитель': 'ВЗОР', 'Серия': 'ВА', 'Типоразмер': 80807, 'Взрывозащита': 'Exe', 'Материал': 'Алюминий', 'Цвет(RAL)': nan,...},
                         {1: {'Производитель': 'ВЗОР', 'Серия': 'ВА', 'Типоразмер': 121209, 'Взрывозащита': 'Exe', 'Материал': 'Алюминий', 'Цвет(RAL)': 7042,...},
        :return:
        '''

        self.unique_name_manufacturers = list(set([main_dict[key_shell]['Производитель'] for key_shell in self.shell_main_dict]))
        return self.unique_name_manufacturers

    def set_manufacturer(self,manufacturer=None):
        '''
        Установка параметра производителя, по идее ставится из конфига сразу в pyqt, а оттуда забирается сюда.
        :param manufacturer: Производитель из pyqt(по дефолту ВЗОР)
        :return:
        '''
        self.manufacturer = manufacturer

    def set_explosion_protection(self,explosion_protection):
        '''
        Установка параметра типа взрывозащиты, забирается напрямую из pyqt,
        всего два варианта "Exe" или "Exd"
        :param explosion_protection:
        :return:
        '''
        self.explosion_protection = explosion_protection

    def get_unique_series(self):
        '''Получение списка серий оболочек для данного производителя'''
        if hasattr(self,'unique_series'):
            self.shell_main_dict_copy = self.shell_main_dict.copy()

        self.unique_series = list()

        for key_shell in self.shell_main_dict_copy.copy():

            if self.shell_main_dict_copy[key_shell]['Производитель'] == self.manufacturer and \
                self.shell_main_dict_copy[key_shell]['Взрывозащита'] == self.explosion_protection:
                    self.unique_series.append(self.shell_main_dict_copy[key_shell]['Серия'])
            else:
                del self.shell_main_dict_copy[key_shell]
        self.shell_main_dict_after_getting_series = self.shell_main_dict_copy.copy()
        self.unique_series = sorted(list(set(self.unique_series)))

    def set_series(self,shell_series):
        '''Устанавливаем значение shell series'''
        self.shell_series = shell_series

    def get_unique_sizes(self):
        '''Получение уникальной серии оболочек для этого производителя'''
        if hasattr(self,'unique_sizes'):
            self.shell_main_dict_copy = self.shell_main_dict.copy()


        self.unique_sizes = list()
        for key_shell in self.shell_main_dict_copy.copy():
            if self.shell_main_dict_copy[key_shell]['Производитель'] == self.manufacturer and\
                self.shell_main_dict_copy[key_shell]['Взрывозащита'] == self.explosion_protection and \
                self.shell_main_dict_copy[key_shell]['Серия'] == self.shell_series    :
                if len(str(self.shell_main_dict_copy[key_shell]['Типоразмер'])) == 5:
                    self.unique_sizes.append('0' + str(self.shell_main_dict_copy[key_shell]['Типоразмер']))
                else:
                    self.unique_sizes.append(str(self.shell_main_dict_copy[key_shell]['Типоразмер']))
            else:
                del self.shell_main_dict_copy[key_shell]
        self.unique_sizes = sorted(list(set(self.unique_sizes)))

    def set_size(self,shell_size):
        '''Установка значения shell_size из pyqt5 при выборе размера'''
        self.shell_size = shell_size

    def set_shell_dict(self,):
        '''К этому моменту останется четкий выбор оболочки'''
        if hasattr(self,'shell_dict'):
            delattr(self,'shell_dict')

        for key_shell in self.shell_main_dict:
            if self.shell_main_dict[key_shell]['Производитель'] == self.manufacturer and\
                self.shell_main_dict[key_shell]['Взрывозащита'] == self.explosion_protection and \
                self.shell_main_dict[key_shell]['Серия'] == self.shell_series:
                    if len(str(self.shell_main_dict[key_shell]['Типоразмер'])) == 5:
                        if '0' + str(self.shell_main_dict[key_shell]['Типоразмер']) == self.shell_size:
                            self.shell_dict = self.shell_main_dict[key_shell]
                    else:
                        if str(self.shell_main_dict[key_shell]['Типоразмер']) == self.shell_size:
                            self.shell_dict = self.shell_main_dict[key_shell]

    def define_marking_explosion_protections(self):
        '''Поиск маркировки взрывозащиты'''
        self.marking_dict = {'gas':[],'dust':[],'ore':[]}
        for count_marking, value_marking in enumerate(self.shell_dict['Маркировка взрывозащиты'].split('--')):
            if ';' in str(value_marking):
                for _ in value_marking.split(';'):
                    if _ != '':
                        if count_marking == 0:
                            self.marking_dict['gas'].append(_)
                        elif count_marking == 1:
                            self.marking_dict['dust'].append(_)
                        elif count_marking == 2:
                            self.marking_dict['ore'].append(_)
            else:
                if count_marking == 0:
                    self.marking_dict['gas'].append(str(value_marking))
                elif count_marking == 1:
                    self.marking_dict['dust'].append(str(value_marking))
                elif count_marking == 2:
                    self.marking_dict['ore'].append(str(value_marking))

    def set_marking_explosion_protection(self,marking_explosion_protection):
        self.marking_explosion_protection = marking_explosion_protection

    def set_minus_temperature(self,minus_temperature):
        self.minus_temperature = minus_temperature

    def set_plus_temperature(self,plus_temperature):
        self.plus_temperature = plus_temperature


if __name__ == '__main__':
    main_dict = get_main_dict(main_path)#Его нужно оставить в памяти, при смене каких либо позиций, чтобы не подключаться заново к smb
    dict_for_modification = main_dict.copy()
    for key_shell in main_dict:
        if main_dict[key_shell]['Производитель'] == 'ВЗОР':
            print(key_shell)

