import os

import pandas as pd
import re
import transliterate

def get_main_dict(main_path: str) -> dict:
    '''
    :param main_path: main_path = os.getcwd() + '\Общая база'
    :return: {'ВЗОР':{'Exe оболочки':{Серия:{0:'ВА',1:'ВА'...}}
    '''

    main_dict = pd.read_csv(main_path, delimiter=';').to_dict('index')

    return main_dict

def set_only_gland_type(gland_main_dict: dict):
    '''оставляет только "Тип":"Кабельнный ввод", всякие гайки, шайбы, ноги удаляются'''
    return_dict = dict()
    for key_number in gland_main_dict.copy():
        if gland_main_dict[key_number]['Тип'] == 'Кабельный ввод':
            return_dict[key_number] = gland_main_dict[key_number].copy()
    return return_dict


def set_correct_number(number:str):
    '''Удаление запятой или еще чего из числа'''
    return_number = number
    if ',' in str(return_number):
        return_number = str(return_number).replace(',','.')
    try:
        return int(float(return_number))
    except:
        return 0

class GlandMainDictQt:
    def __init__(self,gland_csv_path):
        self.gland_csv_path = gland_csv_path


    def set_main_dict(self,main_path: str) -> dict:
        '''
        :param main_path: main_path = os.getcwd() + '\Общая база'
        :return: {'ВЗОР':{'Exe оболочки':{Серия:{0:'ВА',1:'ВА'...}}
        '''

        self.gland_main_dict = pd.read_csv(main_path, delimiter=';').to_dict('index')
        self.gland_main_dict_copy = self.gland_main_dict.copy()

    def set_only_gland_type(self):
        '''оставляет только "Тип":"Кабельнный ввод", всякие гайки, шайбы, ноги удаляются
        personal_gland: '''
        for key_number in self.gland_main_dict.copy():
            if self.gland_main_dict[key_number]['Тип'] != 'Кабельный ввод':
                del self.gland_main_dict[key_number]

    def get_all_glands(self):
        '''Получение всех имен которые есть в csv в столбце полные наименования'''
        self.check_gland_names = list()
        self.gland_all_names = dict()
        if hasattr(self,'gland_main_dict'):
            for key_gland in self.gland_main_dict:

                if self.gland_main_dict[key_gland]['Тип'] == 'Кабельный ввод':
                    if self.gland_main_dict[key_gland]['Полное наименование'] !='' and \
                        self.gland_main_dict[key_gland]['Полное наименование'] != 'ФОРМУЛА!!!!' and\
                        str(self.gland_main_dict[key_gland]['Полное наименование']) != 'nan':
                            if str(self.gland_main_dict[key_gland]['Полное наименование']) not in self.check_gland_names:
                                self.check_gland_names.append(str(self.gland_main_dict[key_gland]['Полное наименование']))
                                self.gland_all_names[str(self.gland_main_dict[key_gland]['Полное наименование'])] = key_gland

    def get_unique_designation(self):
        '''Получение уникальных опций назначения'''
        self.gland_unique_designation = ['Заглушка','Кабельный ввод']

    def set_gland_designation(self,gland_designation):
        '''Установка назначения кабельного ввода'''
        self.gland_designation = gland_designation

    def get_unique_material(self):
        '''Получение уникальных материалов для кабельнного ввода'''
        self.gland_unique_material = ['Никелированная латунь','Латунь','Нержавеющая сталь','Оцинкованная сталь','Пластик']

    def set_gland_material(self,gland_material):
        '''Установка материала кабельного ввода'''
        self.gland_material = gland_material

    def get_unique_thread(self):
        '''Получение уникальных типов резьбы для кабельнного ввода'''
        self.gland_unique_thread = ['М','G','NPT']

    def set_gland_thread(self,gland_thread):
        '''Установка типа резьбы кабельного ввода'''
        self.gland_thread = gland_thread

    def get_unique_cable_type(self):
        '''Получение уникальных значений типа кабеля'''
        self.gland_unique_cable_type = ['Небронированный', 'Бронированный', 'Плоский']

    def set_cable_type(self,gland_cable_type):
        '''Установка типа кабеля(Бронь, небронь, плоский)'''
        self.gland_cable_type = gland_cable_type

    def set_dict_for_calculate_gland_diam(self):
        '''Нужно отсеять кабельные вводы по параметрам: Материал, Тип Кабеля, Тип Резьбы'''
        if hasattr(self,'dict_for_calculate_gland_diam'):
            self.gland_main_dict_copy = self.gland_main_dict.copy()

        for key_number in self.gland_main_dict_copy.copy():
            if str(self.gland_main_dict_copy[key_number]['Тип']) == self.gland_designation and\
                str(self.gland_main_dict_copy[key_number]['Материал']) == self.gland_material and \
                str(self.gland_main_dict_copy[key_number]['Тип кабеля']) == self.gland_cable_type and\
                str(self.gland_main_dict_copy[key_number]['Тип резьбы']) == self.gland_thread and\
                str(self.gland_main_dict_copy[key_number]['Актуальность']) == 'Да':
                continue
            else:
                del self.gland_main_dict_copy[key_number]
        self.dict_for_calculate_gland_diam = self.gland_main_dict_copy.copy()

    def set_gland_min_diam(self,cable_min_diam):
        '''Минимальный диаметр обжимаего кабеля'''
        if isinstance(cable_min_diam,str):
            cable_min_diam = set_correct_number(cable_min_diam)

        if hasattr(self,'cable_max_diam'):
            if cable_min_diam > self.cable_max_diam:
                cable_min_diam = self.cable_max_diam
        if cable_min_diam < 0:
            cable_min_diam = 0

        self.cable_min_diam = int(cable_min_diam)

    def set_gland_max_diam(self,cable_max_diam):
        '''Максимальный диаметр обжимаего кабеля'''
        if isinstance(cable_max_diam,str):
            cable_max_diam = set_correct_number(cable_max_diam)

        if cable_max_diam < 0:
            if hasattr(self,'cable_min_diam'):
                cable_max_diam = self.cable_min_diam
            else:
                cable_max_diam = self.cable_min_diam

        self.cable_max_diam = int(cable_max_diam)

    def give_possible_glands_for_calculate(self,min_diam_from_qt,max_diam_from_qt):
        '''Получение ключей glands, которые удовлетворяют требования мин и макс диамов'''
        result_dict = dict()

        self.set_gland_min_diam(cable_min_diam=min_diam_from_qt)
        self.set_gland_max_diam(cable_max_diam=max_diam_from_qt)

        gland_diam_range_qt = list(range(self.cable_min_diam,self.cable_max_diam+1))
        #Здесь получили все кабельные вводы, с которыми есть пересечение
        if self.gland_cable_type == 'Небронированный' or self.gland_cable_type == 'Бронированный':
            for key_gland in self.dict_for_calculate_gland_diam:
                gland_min_diam_csv = self.dict_for_calculate_gland_diam[key_gland]['Мин диаметр внешнего обжатия кабеля']
                gland_max_diam_csv = self.dict_for_calculate_gland_diam[key_gland]['Макс диаметр внешнего обжатия кабеля']
                range_diam_csv = list(range(set_correct_number(gland_min_diam_csv),set_correct_number(gland_max_diam_csv)+1))
                if list(set(gland_diam_range_qt) & set(range_diam_csv)) != []:
                    result_dict[key_gland] = list(set(gland_diam_range_qt) & set(range_diam_csv))
            max_сoincidence_range = len(max(result_dict.values()))

        #Здесь оставили только те, в которых максимальное количество совпадений по промежутку
        for key_gland in result_dict.copy():
            if len(result_dict[key_gland]) == max_сoincidence_range:
                continue
            else:
                del result_dict[key_gland]
        #ЗДЕСЬ ЕСЛИ ПОПАДАЮТСЯ УСЛОВНО ПЕРЕСЕЧЕНИЯ, НАПРИМЕР ЗНАЮТ ЧЕТКО ЗНАЧЕНИЯ ДИАМЕТРА ОДНОГО КАБЕЛЯ
        #НАПРИМЕР 5 мм, ТОГДА ПОДХОДЯТ И 12 и 16 ТИПОРАЗМЕР. ВЫБРАТЬ НАДО 12
        self.gland_typsize = min([int(self.gland_main_dict[key_gland]['Типоразмер резьбы штуцера']) for _ in result_dict])

        #ЗДЕСЬ КАЖДЫЙ РАЗ ФОРМИРУЕМ СЛОВАРЬ, В КОТОРОМ ОСТАВАЛИСЬ БЫ ТОЛЬКО ВВОДА, В КОТОРЫХ ТИПОРАЗМЕР ОПРЕДЕЛЕН
        self.dict_for_choose_modification_cable = dict()

        for key_gland in result_dict:
            if int(self.gland_main_dict[key_gland]['Типоразмер резьбы штуцера']) == self.gland_typsize:
                self.dict_for_choose_modification_cable[key_gland] = self.gland_main_dict[key_gland]

    def set_gland_without_modification_tube_mr(self):
        '''Выбор кабельнного ввода без модификаций'''
        if hasattr(self,'dict_for_choose_modification_cable'):
            self.key_gland = list()
            for key_gland in self.dict_for_choose_modification_cable:
                if str(self.dict_for_choose_modification_cable[key_gland]['Металлорукав']).lower() == 'нет' and \
                        str(self.dict_for_choose_modification_cable[key_gland]['Трубный']).lower() == 'нет':
                    self.key_gland.append(key_gland)
            if len(self.key_gland) == 0:
                raise BaseException('в src.csv.gland_csv.set_gland не найден key_gland')
            elif len(self.key_gland) == 1:
                self.key_gland = self.key_gland[0]
            else:
                # Оставить только ту, где нет модификации
                self.key_gland = [i for i in self.key_gland if
                                  self.dict_for_choose_modification_cable[i]['Модификация'].lower() == 'нет'][0]





    def give_modification_for_calculated_diam(self):
        def add_special_modification():
            result_list = list()
            for key_gland in self.dict_for_choose_modification_cable:
                modification = re.split(r'[-;!.,=+]', self.dict_for_choose_modification_cable[key_gland]['Серия'])
                # if len(modification) >2:
                modification = '-'.join(modification[2:])
                if modification != '':
                    result_list.append(modification)
            return result_list
        #НУЖНО ПОЛУЧИТЬ ОТ СЛОВАРЯ self.dict_for_choose_modification_cable ТОЛЬКО ЗНАЧЕНИЯ МОДИФИКАЦИЙ, Т.Е. ПО СЕРИИ ПРОЙТИСЬ
        #ВЗ-Н-Т Нужно получить Т, и размер. и модификацию (расширенный или нет).
        #ВЗ-Б-Т-МР получить [Т,МР]

        self.list_with_modifications_name = sorted(list(set(add_special_modification())))


    def set_gland_additional_marking(self, gland_additional_marking=None):
        # self.gland_series = gland_series
        self.gland_additional_marking = gland_additional_marking

    def get_uniqie_tube_mr_modification(self):
        '''
        Добавление параметром либо металлорукава либо трубопровода: МР25, МР32... или 1/4, 3/8 и тд
        :return: self.unique_tube_mr_modification
        '''
        unique_tube_mr_modification = list()

        for key_gland in self.dict_for_choose_modification_cable:
            if hasattr(self,'gland_additional_marking'):
                if self.gland_additional_marking == 'МР':

                    if self.dict_for_choose_modification_cable[key_gland]['Металлорукав'].lower() != 'нет':
                        unique_tube_mr_modification.append(self.dict_for_choose_modification_cable[key_gland]['Металлорукав'])
                elif self.gland_additional_marking == 'Т':
                    self.thread_name_in = str()
                    self.thread_value_in = str()
                    self.thread_name_out = str()
                    self.thread_value_out = str()
                    if self.dict_for_choose_modification_cable[key_gland]['Внутренняя трубная резьба, тип'] == 'G':
                        self.thread_name_in = 'G'+'(В)'
                        self.thread_value_in = f'{self.dict_for_choose_modification_cable[key_gland]["Внутренняя трубная резьба, размер"]}'
                    if self.dict_for_choose_modification_cable[key_gland]['Внешняя трубная резьба, тип'] == 'G':
                        self.thread_name_out = 'G'+'(Н)'
                        self.thread_value_out = f'{self.dict_for_choose_modification_cable[key_gland]["Внешняя трубная резьба, размер"]}'

                    unique_tube_mr_modification.append(self.thread_value_out + self.thread_name_out +
                                                       self.thread_value_in + self.thread_name_in)
                elif self.gland_additional_marking == 'Т-МР':
                    self.thread_name_in = str()
                    self.thread_value_in = str()
                    self.thread_name_out = str()
                    self.thread_value_out = str()
                    if self.dict_for_choose_modification_cable[key_gland]['Внутренняя трубная резьба, тип'] == 'G':
                        self.thread_name_in = 'G'+'(В)'
                        self.thread_value_in = f'{self.dict_for_choose_modification_cable[key_gland]["Внутренняя трубная резьба, размер"]}'
                    if self.dict_for_choose_modification_cable[key_gland]['Внешняя трубная резьба, тип'] == 'G':
                        self.thread_name_out = 'G'+'(Н)'
                        self.thread_value_out = f'{self.dict_for_choose_modification_cable[key_gland]["Внешняя трубная резьба, размер"]}'

                    tube_part = (self.thread_value_out + self.thread_name_out +
                                 self.thread_value_in + self.thread_name_in)
                    mr_part = self.dict_for_choose_modification_cable[key_gland]['Металлорукав']
                    unique_tube_mr_modification.append(tube_part + '/' + mr_part)

        self.unique_tube_mr_modification = list()

        self.unique_tube_mr_modification = sorted(list(set(unique_tube_mr_modification[:])))

    def set_gland_tube_mr_modification(self,gland_tube_mr_modification=None):
        self.gland_tube_mr_modification = gland_tube_mr_modification

    def set_gland(self):
        #Закинем все ключи, а далее если будет модификация, то удалим его с модификацией, а если останется там один, то все ок
        self.key_gland = list()
        for key_gland in self.dict_for_choose_modification_cable:
            if self.dict_for_choose_modification_cable[key_gland]['Типоразмер резьбы штуцера'] == str(self.gland_typsize):
                if not hasattr(self,'gland_additional_marking'):
                    self.key_gland.append(key_gland)
                else:
                    if hasattr(self,'gland_tube_mr_modification'):
                        if self.gland_additional_marking == 'МР':
                            if self.dict_for_choose_modification_cable[key_gland]['Металлорукав'] == self.gland_tube_mr_modification:
                                self.key_gland.append(key_gland)
                        if self.gland_additional_marking == 'Т':
                            if self.gland_tube_mr_modification.split('G')[1] == '(В)':
                                if self.dict_for_choose_modification_cable[key_gland]['Внутренняя трубная резьба, размер'] == self.gland_tube_mr_modification.split('G')[0]:
                                    self.key_gland.append(key_gland)
                            elif self.gland_tube_mr_modification.split('G')[1] == '(Н)':
                                if self.dict_for_choose_modification_cable[key_gland]['Внешняя трубная резьба, размер'] == self.gland_tube_mr_modification.split('G')[1]:
                                    self.key_gland.append(key_gland)
                        if self.gland_additional_marking == 'Т-МР':
                            if self.thread_name_in != str():
                                if self.dict_for_choose_modification_cable[key_gland]['Внутренняя трубная резьба, размер'] == self.thread_value_in and\
                                    self.dict_for_choose_modification_cable[key_gland]['Металлорукав'] == self.gland_tube_mr_modification.split('/')[1]:
                                    self.key_gland.append(key_gland)
                            elif self.thread_name_out != str():
                                if self.dict_for_choose_modification_cable[key_gland]['Внешняя трубная резьба, размер'] == self.thread_value_out and\
                                    self.dict_for_choose_modification_cable[key_gland]['Металлорукав'] ==self.gland_tube_mr_modification.split('/')[1]:
                                    self.key_gland.append(key_gland)
        if len(self.key_gland) == 0:
            raise BaseException('в src.csv.gland_csv.set_gland не найден key_gland')
        elif len(self.key_gland) == 1:
            self.key_gland = self.key_gland[0]
        else:
            #Оставить только ту, где нет модификации
            self.key_gland = [i for i in self.key_gland if self.dict_for_choose_modification_cable[i]['Модификация'].lower() == 'нет'][0]

        # #теперь оставляем только один, такой, чтобы у него был наименьший диаметр из оставшихся и не было дополнительных диапазонов
        # #т.е. если есть М25 и М25Р и она оба одинаковый диапазон, надо оставить М25
        # min_gland = None
        # modification = None
        # key_gland_main = None
        # for key_gland in result_dict:
        #     if min_gland == None:
        #         min_gland = int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера'])
        #         modification = str(self.glands_correct_diametr[key_gland]['Модификация'])
        #         key_gland_main = key_gland
        #     else:
        #         if min_gland > int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера']):
        #             min_gland = int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера'])
        #             modification = str(self.glands_correct_diametr[key_gland]['Модификация'])
        #             key_gland_main = key_gland
        #         elif min_gland == int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера']):
        #             if modification == 'Нет':
        #                 continue
        #             else:
        #                 modification = str(self.glands_correct_diametr[key_gland]['Модификация'])
        #                 key_gland_main = key_gland



class CableGlandInformation:

    def __init__(self,gland_dict):
        self.set_gland_dict(gland_dict=gland_dict)
        self.set_properties()
        self.create_name()
        self.create_dxf_name()

        '''Для алгоритмов добавления кабельных вводов'''
        self.set_status_add_in_one_row(status=False)
        self.set_status_add_to_possible_biggest_input(status=False)

    def set_gland_dict(self, gland_dict):
        self.gland_dict = gland_dict

    def create_name(self):

        self.gland_russian_name = ''
        if str(self.gland_dict['Полное наименование']) != 'nan' and  str(self.gland_dict['Полное наименование']) !='' and  str(self.gland_dict['Полное наименование']) !='ФОРМУЛА!!!!':
            self.gland_russian_name +=str(self.gland_dict['Полное наименование'])



        else:
            if hasattr(self,'material_gland'):
                self.gland_russian_name += self.material_gland + '-' + self.cable_type + self.cable_type_size #Добавляем материал + тип кабеля

                if self.tube_type != None:
                    if hasattr(self,'internal_tube_size'):
                        self.gland_russian_name += '-' + 'Т' + self.internal_tube_size + self.internal_tube_status + '(В)'
                    elif hasattr(self,'external_tube_status'):
                        self.gland_russian_name += '-' + 'Т' + self.external_tube_size + self.external_tube_status + '(Н)'

                if self.metalhose != None:
                    self.gland_russian_name += '-' + self.metalhose

        if self.gland_russian_name.lower() in ['устройство заземления']:
            self.gland_russian_name = 'ground'

    def create_dxf_name(self):
        if hasattr(self,'gland_russian_name'):
            self.gland_dxf_name = transliterate.translit(self.gland_russian_name, language_code='ru', reversed=True)
            if '/' in self.gland_dxf_name:
                self.gland_dxf_name = self.gland_dxf_name.replace('/','')

    def set_properties(self):
        self.set_material()
        self.set_cable_type()
        self.set_cable_type_size()
        self.set_metalhose()
        self.set_tube()
        self.set_diametr()
        self.set_options()

    def set_material(self):
        material = str(self.gland_dict['Материал'])
        if material != None:
            if material.lower() == 'Никелированная латунь'.lower():
                self.material_gland = 'ВЗ'
            elif material.lower() == 'Латунь'.lower():
                self.material_gland = 'ЛВЗ'
            elif material.lower() == 'Нержавеющая сталь'.lower():
                self.material_gland = 'НВЗ'
            elif material.lower() == 'Оцинкованная сталь'.lower():
                self.material_gland = 'ОВЗ'
            elif material.lower() == 'Пластик'.lower():
                self.material_gland = 'ПВЗ'

    def set_cable_type(self):
        cable_type = str(self.gland_dict['Тип кабеля'])
        if cable_type != None:
            if cable_type.lower() == 'небронированный':
                self.cable_type = 'Н'
            elif cable_type.lower() == 'бронированный':
                self.cable_type = 'Б'

    def set_cable_type_size(self):
        cable_type_size = str(self.gland_dict['Типоразмер резьбы штуцера'])
        if cable_type_size != None:
            self.cable_type_size = cable_type_size

    def set_metalhose(self):
        metalhose = str(self.gland_dict['Металлорукав'])
        if metalhose != None:
            if metalhose.lower() == 'нет':
                self.metalhose = None
            else:
                self.metalhose = metalhose

    def set_tube(self):
        tube_status = str(self.gland_dict['Трубный'])
        internal_tube_status = str(self.gland_dict['Внутренняя трубная резьба, тип'])
        external_tube_status = str(self.gland_dict['Внешняя трубная резьба, тип'])
        if tube_status.lower() == 'нет' or \
           (tube_status.lower() == 'да' and
            internal_tube_status.lower() == 'нет' and
            external_tube_status.lower() == 'нет' ):
                self.tube_type = None
        else:
                self.tube_type = ''
                if internal_tube_status.lower() != 'нет':
                    self.internal_tube_status = internal_tube_status
                    self.internal_tube_size = str(self.gland_dict['Внутренняя трубная резьба, размер'])
                if external_tube_status.lower() != 'нет':
                    self.external_tube_status = external_tube_status
                    self.external_tube_size = str(self.gland_dict['Внешняя трубная резьба, размер'])
    def set_diametr(self):
        diametr = str(self.gland_dict['Описаный диаметр кабельного ввода'])
        '''Удаление запятой или еще чего из числа'''
        if ',' in str(diametr):
            diametr = str(diametr).replace(',', '.')
        try:
            self.diametr = float(diametr)
        except:
            self.diametr = 0

    def set_options(self):
        self.vz_vz = False
        self.vz_vze = False
        self.ch = False
        self.gsh = False
        self.kg = False
        self.kz = False

    def set_x_coordinate(self,x_coordinate):
        self.x_coordinate = x_coordinate

    def set_y_coordinate(self,y_coordinate):
        self.y_coordinate = y_coordinate

    def set_z_coordinate(self,z_coordinate):
        self.z_coordinate = z_coordinate

    def set_status_add_to_possible_biggest_input(self,status:bool):
        self.status_add_to_possible_biggest_input = status

    def set_status_add_in_one_row(self,status:bool):
        self.status_add_in_one_row = status

    def set_property_onerow_algoritm(self):
        self.property_onerow_algoritm = True
        self.property_tworow_algoritm = False
        self.property_snake_algoritm = False

    def set_property_tworow_algoritm(self):
        self.property_tworow_algoritm = True
        self.property_onerow_algoritm = False
        self.property_snake_algoritm = False

    def set_property_snake_algoritm(self):
        self.property_snake_algoritm = True
        self.property_onerow_algoritm = False
        self.property_tworow_algoritm = False

    def set_BOM_gland(self,BOM_gland):
        self.BOM_gland = BOM_gland





if __name__ == '__main__':
    print(set_correct_number(number = '-13,5'))
    # gland_main_dict = get_main_dict(main_path=gland_csv_path)
    # set_only_gland_type(gland_main_dict=gland_main_dict)
    # print(gland_main_dict)
    # dict_all_names = dict()
    # for key_number in gland_main_dict:
    #     gland_dict = gland_main_dict[key_number]
    #     cable_gland = CableGlandInformation(gland_dict)
    #     dict_all_names[key_number] = cable_gland.gland_russian_name
    #     # print(cable_gland.gland_russian_name)
    #
    # wb = openpyxl.Workbook()
    # sheet1 = wb.active
    # for row_number, value in dict_all_names.items():
    #     print(row_number)
    #     print(value)
    #     sheet1.cell(row=int(row_number),column=1,value=value)
    # wb.save('test.xlsx')
    #     # sheet1[cell] = value
    #
    # print(len(dict_all_names))