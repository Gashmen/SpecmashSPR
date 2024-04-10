
class BOM_SHELL:

    def __init__(self):
        self.vrpt_name = str()
        self.fullname = str()
        self.property = str()
        self.production_cost = str()
        self.work_cost = str()

    def get_shell_information(self,shell_dict:dict[str:str]):
        '''
        Получение значения со словаря
        :param shell_dict: {'Производитель': 'ВЗОР', 'Серия': 'ВП', 'Типоразмер': 161610, 'Взрывозащита': 'Exe', 'Материал': 'Пластик', 'Цвет(RAL)': 9005, 'Температура минимальная': -60, 'Температура максимальная': 130, 'IP': '66;67', 'Крепление': nan, '8': nan, '9': nan, '10': nan, 'Ширина': 160.0, 'Длина': 160.0, 'Глубина': 100.0, 'Масса': '0.73', 'Толщина стенки': '6', 'Зона Сверловки AB Ш': nan, 'Зона Сверловки БГ Ш': nan, 'Внутренние размеры AB': 120, 'Внутренние размеры БГ': 98, 'Межосевое расстояние для DIN': nan, 'Кол-во отверстий': nan, 'Расстояния болтов вдоль АВ': nan, 'Расстояния болтов вдоль БГ': nan, 'Количество болтов': nan, 'Внутренняя высота коробки': 75.0, 'Маркировка взрывозащиты': '1Ex e IIC;0Ex ia IIC;1Ex ib IIB;1Ex e[ia Ga] IIC;1Ex e mb IIC;1Ex e db IIC;1Ex e db mb IIC;1Ex e db [ia Ga] IIC;1Ex e db [ib] IIC;1Ex e mb ia IIC;1Ex e db mb ia IIC;--Ex tb IIIC;Ex ta IIIC;', 'Наличие': True}
        :return:
        '''

        self.shell_full_information:dict = shell_dict

    def set_vrpt_name(self):
        if hasattr(self,'shell_full_information'):
            self.vrpt_name = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_ОБОЗНАЧЕНИЕ'])
            if '#' in self.vrpt_name:
                self.vrpt_name = self.vrpt_name.split('#')
            else:
                self.vrpt_name = [self.vrpt_name]

    def set_fullname(self):
        if hasattr(self,'shell_full_information'):
            self.fullname = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_НАИМЕНОВАНИЕ'])
            if '#' in self.fullname:
                self.fullname = self.fullname.split('#')
            else:
                self.fullname = [self.fullname]

    def set_property(self):
        if hasattr(self,'shell_full_information'):
            self.property = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_СВОЙСТВО'])

    def set_production_cost(self):
        if hasattr(self,'shell_full_information'):
            self.production_cost = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_СЕБЕСТОИМОСТЬ'])
            if ',' in str(self.production_cost):
                self.production_cost = str(self.production_cost).replace(',','.')

    def set_work_cost(self):
        if hasattr(self,'shell_full_information'):
            self.work_cost = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_РАБОТА'])
            if ',' in str(self.work_cost):
                self.work_cost = str(self.work_cost).replace(',','.')

    def calculate_sum_cost(self):
        if hasattr(self,'work_cost') and hasattr(self,'production_cost'):
            if self.production_cost != '' and self.work_cost !='':
                self.shell_sum_cost = float(self.production_cost) + float(self.work_cost)
                self.shell_sum_cost = str(self.shell_sum_cost)
            else:
                self.shell_sum_cost = ''

    def give_bom_dict(self):
        self.bom_dict = \
            {tuple(self.fullname):
                {
                'Формат':"А4",
                'Зона':"",
                'Поз.':"",
                'Обозначение':self.vrpt_name,
                'Наименование':self.fullname,
                'Кол.':'1',
                'Примечание':'ВЗОР',
                'Свойство':'Сборочные единицы',
                'Цена': self.shell_sum_cost
                }
            }

    def add_din_bom(self,din_length):
        if hasattr(self,'bom_dict'):
            self.bom_dict[tuple([f'ВРПТ.745551.005-{din_length}'])] =\
                {
                    'Формат': "",
                    'Зона': "",
                    'Поз.': "",
                    'Обозначение': [f'ВРПТ.745551.005-{din_length}'],
                    'Наименование': [f'DIN-рейка NS35х7,5, L={din_length} мм'],
                    'Кол.': '',
                    'Примечание': 'ВЗОР',
                    'Свойство': 'Детали',
                    'Цена': f'{int(150*din_length/1000)}'
                }


class BOM_GLAND:

    def __init__(self):
        self.vrpt_name = str()
        self.fullname = str()
        self.property = str()
        self.production_cost = str()
        self.work_cost = str()

    def get_gland_information(self,gland):
        '''
        Получение значения со словаря
        :param shell_dict: {'Производитель': 'ВЗОР', 'Серия': 'ВП', 'Типоразмер': 161610, 'Взрывозащита': 'Exe', 'Материал': 'Пластик', 'Цвет(RAL)': 9005, 'Температура минимальная': -60, 'Температура максимальная': 130, 'IP': '66;67', 'Крепление': nan, '8': nan, '9': nan, '10': nan, 'Ширина': 160.0, 'Длина': 160.0, 'Глубина': 100.0, 'Масса': '0.73', 'Толщина стенки': '6', 'Зона Сверловки AB Ш': nan, 'Зона Сверловки БГ Ш': nan, 'Внутренние размеры AB': 120, 'Внутренние размеры БГ': 98, 'Межосевое расстояние для DIN': nan, 'Кол-во отверстий': nan, 'Расстояния болтов вдоль АВ': nan, 'Расстояния болтов вдоль БГ': nan, 'Количество болтов': nan, 'Внутренняя высота коробки': 75.0, 'Маркировка взрывозащиты': '1Ex e IIC;0Ex ia IIC;1Ex ib IIB;1Ex e[ia Ga] IIC;1Ex e mb IIC;1Ex e db IIC;1Ex e db mb IIC;1Ex e db [ia Ga] IIC;1Ex e db [ib] IIC;1Ex e mb ia IIC;1Ex e db mb ia IIC;--Ex tb IIIC;Ex ta IIIC;', 'Наличие': True}
        :return:
        '''
        self.gland = gland
        self.gland_full_information = gland.gland_dict


    def set_vrpt_name(self):
        if hasattr(self,'gland_full_information'):
            self.vrpt_name =''
            if str(self.gland_full_information['Чертеж основной']) != ' ':
                self.vrpt_name += str(self.gland_full_information['Чертеж основной'])
            if str(self.gland_full_information['Исполнение']) != ' ':
                self.vrpt_name += '-' + str(self.gland_full_information['Исполнение'])
            if '#' in self.vrpt_name:
                self.vrpt_name = self.vrpt_name.split('#')
            else:
                self.vrpt_name = [self.vrpt_name]

    def set_fullname(self):
        if hasattr(self,'gland_full_information'):
            self.fullname = str(self.gland_full_information['СПЕЦИФИКАЦИЯ_НАИМЕНОВАНИЕ'])
            if '#' in self.fullname:
                self.fullname = self.fullname.split('#')
            else:
                self.fullname = [self.fullname]

    def set_property(self):
        if hasattr(self,'gland_full_information'):
            self.property = 'Сборочные единицы'

    def set_production_cost(self):
        if hasattr(self,'gland_full_information'):
            self.production_cost = str(self.gland_full_information['Стоимость материальная'])
            if ',' in self.production_cost:
                self.production_cost.replace(',','.')

    def set_work_cost(self):
        if hasattr(self,'gland_full_information'):
            self.work_cost = str(self.gland_full_information['Стоимость работ'])
            if ',' in self.work_cost:
                self.work_cost.replace(',','.')

    def calculate_sum_cost(self):
        if hasattr(self,'work_cost') and hasattr(self,'production_cost'):
            if self.production_cost != '' and self.work_cost != '' and self.production_cost != 'nan' and self.work_cost != 'nan':
                self.shell_sum_cost = float(self.production_cost) + float(self.work_cost)
                self.shell_sum_cost = str(self.shell_sum_cost)
            else:
                self.shell_sum_cost = ''

    def give_bom_dict(self):
        self.bom_dict = \
            {tuple(self.fullname):
                {
                'Формат':"А4",
                'Зона':"",
                'Поз.':"",
                'Обозначение':self.vrpt_name,
                'Наименование':self.fullname,
                'Кол.':'',
                'Примечание':'ВЗОР',
                'Свойство':'Сборочные единицы',
                'Цена':self.shell_sum_cost
                }
            }


    def add_options_bom(self):
        if hasattr(self,'bom_dict'):
            self.bom_dict[tuple([f'Уплотнительное кольцо Ду {self.gland.cable_type_size}, полимер'])] =\
                {
                    'Формат': "",
                    'Зона': "",
                    'Поз.': "",
                    'Обозначение': [f'УК{self.gland.cable_type_size}'],
                    'Наименование': [f'Уплотнительное кольцо Ду {self.gland.cable_type_size}, полимер'],
                    'Кол.': '',
                    'Примечание': 'ВЗОР',
                    'Свойство': 'Детали',
                    'Цена': ''
                }

            if self.gland.kz == True:
                self.bom_dict[tuple([f'Кольцо заземления Ду {self.gland.cable_type_size}-6,','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': [f'КЗ{self.gland.cable_type_size}'],
                        'Наименование': [f'Кольцо заземления Ду {self.gland.cable_type_size}-6,','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР',
                        'Свойство': 'Детали',
                        'Цена': ''
                    }

            if self.gland.gsh == True:
                self.bom_dict[tuple([f'Гроверная шайба {self.gland.cable_type_size},','нержавеющая сталь AISI 304'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': [f'ГШ{self.gland.cable_type_size}'],
                        'Наименование': [f'Гроверная шайба {self.gland.cable_type_size},','нержавеющая сталь AISI 304'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР',
                        'Свойство': 'Детали',
                        'Цена': ''
                    }

            if self.gland.kg == True:
                self.bom_dict[tuple([f'Контргайка М{self.gland.cable_type_size}х1.5,','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': [f'КГ{self.gland.cable_type_size}'],
                        'Наименование': [f'Контргайка М{self.gland.cable_type_size}х1.5,','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР',
                        'Свойство': 'Детали',
                        'Цена': ''
                    }

            if self.gland.vz_vz == True:
                self.bom_dict[tuple([f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': [f'ВЗ-ВЗ{self.gland.cable_type_size}'],
                        'Наименование': [f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР',
                        'Свойство': 'Детали',
                        'Цена': ''
                    }

            if self.gland.vz_vze == True:
                self.bom_dict[tuple([f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': [f'ВЗ-ВЗе{self.gland.cable_type_size}'],
                        'Наименование': [f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР',
                        'Свойство': 'Детали',
                        'Цена': ''
                    }
            if self.gland.ch == True:
                self.bom_dict[tuple([f'Чехол защитный М{self.gland.cable_type_size}'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': [f'Ч{self.gland.cable_type_size}'],
                        'Наименование': [f'Чехол защитный М{self.gland.cable_type_size}'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР',
                        'Свойство': 'Детали',
                        'Цена': ''
                    }

class BOM_GENERAL:
    tag_in_BOM_dxf = {'Формат': 'A', 'Зона': 'B', 'Поз.': 'C', 'Обозначение': 'D', 'Наименование': 'E', 'Кол.': 'F',
                      'Примечание': 'G', 'Цена': 'H'}
    def __init__(self):
        self.list_elements = []
        self.bom_dict = dict()
        self.list_with_all_names = list()

    def add_bom_list_elements(self,BOM:dict):
        self.list_elements.append(BOM)

    def create_new_bom_dict(self):
        '''Создает новый словарь c учетом того, что элементы повторяются тут'''
        self.bom_dict = dict()
        for dict_elements in self.list_elements:
            for element in dict_elements:
                if element not in self.bom_dict:
                    self.bom_dict[element] = dict_elements[element].copy()
                    self.bom_dict[element]['Кол.'] = '1'
                else:
                    self.bom_dict[element]['Кол.'] = str(1+int(self.bom_dict[element]['Кол.']))



    def create_dict_main_properties(self):
        '''
        Свойства нужно вынести наружу и сделать словарь
        :param list_properties:
    [{'Обозначение': 'ВРПТ.301172.024-11', 'Наименование': 'Оболочка ВП.161610', 'Свойство': 'Сборочные единицы', 'Формат': 'А4', 'Кол.': None, 'Примечание': None},
     {'Обозначение': None, 'Наименование': 'Винт А2.М6-6gx10.019#ГОСТ 17473-80', 'Свойство': 'Стандартные изделия', 'Формат': 'А4', 'Кол.': None, 'Примечание': None},
     {'Обозначение': None, 'Наименование': 'Шайба 6 019 ГОСТ 6402-70', 'Свойство': 'Стандартные изделия', 'Формат': 'А4', 'Кол.': None, 'Примечание': None},
     {'Обозначение': None, 'Наименование': 'Шайба A.6.019 ГОСТ 11371-78', 'Свойство': 'Стандартные изделия', 'Формат': 'А4', 'Кол.': None, 'Примечание': None},
     {'Обозначение': 'ВРПТ.745551.005-140', 'Наименование': 'DIN-рейка NS35х7,5, L=140 мм', 'Свойство': 'Детали', 'Формат': 'А4', 'Кол.': None, 'Примечание': None},
     {'Обозначение': 'ВРПТ.305311.001-025', 'Наименование': 'Кабельный ввод ВЗ-Н25#для не бронированного#кабеля, диаметром 12-18мм', 'Свойство': 'Сборочные единицы', 'Формат': 'А4', 'Кол.': None, 'Примечание': None}]

        :return: "Стандартные изделия":{}
        '''
        list_properties = list(self.bom_dict.values())
        self.dict_for_creating_BOM_with = dict()
        for equip_dict in list_properties:
            property = equip_dict['Свойство']
            if property not in self.dict_for_creating_BOM_with:
                equip_dict.pop('Свойство')
                self.dict_for_creating_BOM_with[property] = [equip_dict]
            else:
                equip_dict.pop('Свойство')
                self.dict_for_creating_BOM_with[property].append(equip_dict)


    def dict_all_attrib_in_BOM(self):
        '''

        :param list_for_creating_BOM_with:
        {'Сборочные единицы': [{'Обозначение': 'ВРПТ.301172.024-021', 'Наименование': 'Оболочка ВП.262512', 'Формат': 'А4', 'Кол.': 1, 'Примечание': None, 'Цена': 7154.1}, {'Обозначение': 'ВРПТ.305311.001-025', 'Наименование': 'Кабельный ввод ВЗ-Н25#для не бронированного#кабеля, диаметром 12-18мм', 'Формат': 'А4', 'Кол.': 6, 'Примечание': None, 'Цена': 884.21}, {'Обозначение': 'ВРПТ.305311.001-016', 'Наименование': 'Кабельный ввод ВЗ-Н16#для не бронированного#кабеля, диаметром 3-8мм', 'Формат': 'А4', 'Кол.': 3, 'Примечание': None, 'Цена': 615.75}, {'Обозначение': 'ВРПТ.305311.001-012', 'Наименование': 'Кабельный ввод ВЗ-Н12#для не бронированного#кабеля, диаметром 2-6мм', 'Формат': 'А4', 'Кол.': 2, 'Примечание': None, 'Цена': 607.79}, {'Обозначение': 'ВРПТ.305311.001-032', 'Наименование': 'Кабельный ввод ВЗ-Н32#для не бронированного#кабеля, диаметром 18-25мм', 'Формат': 'А4', 'Кол.': 2, 'Примечание': None, 'Цена': 1188.38}, {'Обозначение': 'ВРПТ.685541.003', 'Наименование': 'Устройство заземления', 'Формат': None, 'Кол.': 1, 'Примечание': None, 'Цена': None}],
        'Стандартные изделия': [{'Обозначение': None, 'Наименование': 'Винт А2.М6-6gx10.019#ГОСТ 17473-80', 'Формат': 'А4', 'Кол.': 2, 'Примечание': None, 'Цена': None}, {'Обозначение': None, 'Наименование': 'Шайба 6 019 ГОСТ 6402-70', 'Формат': 'А4', 'Кол.': 2, 'Примечание': None, 'Цена': None}, {'Обозначение': None, 'Наименование': 'Шайба A.6.019 ГОСТ 11371-78', 'Формат': 'А4', 'Кол.': 2, 'Примечание': None, 'Цена': None}],
        'Детали': [{'Обозначение': 'ВРПТ.745551.005-240', 'Наименование': 'DIN-рейка NS35х7,5, L=240 мм', 'Формат': 'А4', 'Кол.': 1, 'Примечание': None, 'Цена': None}]}
        :return:
        '''

        self.return_dict_attribs = dict()

        tag_in_BOM_dxf = {'Формат': 'A', 'Зона': 'B', 'Поз.': 'C', 'Обозначение': 'D', 'Наименование': 'E', 'Кол.': 'F',
                          'Примечание': 'G', 'Цена': 'H'}

        start_row_int = 1
        startstart_row_int = 1

        for name_property in self.dict_for_creating_BOM_with:
            start_row_int += 1
            startstart_row_int += 1
            self.return_dict_attribs[f'E{start_row_int}'] = name_property
            start_row_int += 2
            startstart_row_int += 2

            equipment_list = self.dict_for_creating_BOM_with[name_property]
            for equip_dict in equipment_list:
                max_row = max((len(equip_dict['Обозначение']), len(equip_dict['Наименование']))) + startstart_row_int
                for column_name in equip_dict:
                    '''СДЕЛАТЬ ['A4','',''] и тд'''
                    if not isinstance(equip_dict[column_name], list):
                        equip_dict[column_name] = [equip_dict[column_name]]
                        for _ in range(1, max((len(equip_dict['Обозначение']), len(equip_dict['Наименование'])))):
                            equip_dict[column_name].append('')
                    # if 'Цена' != column_name:
                    for name in equip_dict[column_name]:

                        if column_name in tag_in_BOM_dxf:
                            tag_attrib = tag_in_BOM_dxf[column_name] + str(start_row_int)
                            self.return_dict_attribs[tag_attrib] = name
                            start_row_int += 1
                    start_row_int = startstart_row_int
                start_row_int = max_row
                startstart_row_int = max_row


    def check_next_page(self,BOM_insert_name: str, row_number: int):
        '''
        Проверка на создание следующей страницы
        :param BOM_insert_name: либо BOM_FIRST либо BOM_SECOND
        :param row_number: 1-29 или 1-32
        :return: True or False
        '''

        if BOM_insert_name == 'BOM_FIRST':
            if row_number > 29:
                return False
            else:
                return True
        elif BOM_insert_name == 'BOM_SECOND':
            if row_number > 32:
                return False
            else:
                return True

    def modify_dict_for_BOM(self):
        '''
        Нужно получить номер листа ключом, значение аттрибуты и их значения,
        :param dict_all_attribs_for_bom:{'E2': 'Сборочные единицы',
        'D4': 'ВРПТ.301172.024-021',
        'E4': 'Оболочка ВП.262512', 'A4': 'А4', 'F4': '1', 'G4': '', 'D5': 'ВРПТ.305311.001-025', 'D6': '', 'D7': '',
        'E5': 'Кабельный ввод ВЗ-Н25', 'E6': 'для не бронированного', 'E7': 'кабеля, диаметром 12-18мм', 'A5': 'А4',
        'A6': '', 'A7': '', 'F5': '6', 'F6': '', 'F7': '', 'G5': '', 'G6': '', 'G7': '', 'D8': 'ВРПТ.305311.001-016', 'D9': '', 'D10': '', 'E8': 'Кабельный ввод ВЗ-Н16', 'E9': 'для не бронированного', 'E10': 'кабеля, диаметром 3-8мм', 'A8': 'А4', 'A9': '', 'A10': '', 'F8': '3', 'F9': '', 'F10': '', 'G8': '', 'G9': '', 'G10': '', 'D11': 'ВРПТ.305311.001-012', 'D12': '', 'D13': '', 'E11': 'Кабельный ввод ВЗ-Н12', 'E12': 'для не бронированного', 'E13': 'кабеля, диаметром 2-6мм', 'A11': 'А4', 'A12': '', 'A13': '', 'F11': '2', 'F12': '', 'F13': '', 'G11': '', 'G12': '', 'G13': '', 'D14': 'ВРПТ.305311.001-032', 'D15': '', 'D16': '', 'E14': 'Кабельный ввод ВЗ-Н32', 'E15': 'для не бронированного', 'E16': 'кабеля, диаметром 18-25мм', 'A14': 'А4', 'A15': '', 'A16': '', 'F14': '2', 'F15': '', 'F16': '', 'G14': '', 'G15': '', 'G16': '', 'E18': 'Стандартные изделия', 'D20': '', 'D21': '', 'E20': 'Винт А2.М6-6gx10.019', 'E21': 'ГОСТ 17473-80', 'A20': 'А4', 'A21': '', 'F20': '2', 'F21': '', 'G20': '', 'G21': '', 'D22': '', 'E22': 'Шайба 6 019 ГОСТ 6402-70', 'A22': 'А4', 'F22': '2', 'G22': '', 'D23': '', 'E23': 'Шайба A.6.019 ГОСТ 11371-78', 'A23': 'А4', 'F23': '2', 'G23': '', 'E25': 'Детали', 'D27': 'ВРПТ.745551.005-240', 'E27': 'DIN-рейка NS35х7,5, L=240 мм', 'A27': 'А4', 'F27': '1', 'G27': '', 'E29': 'Прочие изделия', 'D31': 'TU16-2-GY', 'E31': 'Клемма проходная винтовая Iн=76А', 'A31': '', 'F31': '3', 'G31': ''}
        :return:
        '''

        self.BOM_result_dict = dict()

        for attrib_name in self.return_dict_attribs:
            if (int(attrib_name[1:]) - 29) <= 0:
                if 1 not in self.BOM_result_dict:
                    self.BOM_result_dict[1] = dict()
                self.BOM_result_dict[1][attrib_name] = self.return_dict_attribs[attrib_name]
            else:
                page_number = ((int(attrib_name[1:]) - 29) // 32) + 2
                if page_number not in self.BOM_result_dict:
                    self.BOM_result_dict[page_number] = dict()

                self.BOM_result_dict[page_number][attrib_name[0] + str(int(attrib_name[1:]) - 29 - (32 * (page_number - 2)))] = \
                self.return_dict_attribs[attrib_name]

    def create_BOM_first(self,doc_bom):
        '''Создает первый лист спецификации'''

        block_border = doc_bom.blocks['BOM_FIRST']
        values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
        doc_bom.modelspace().delete_all_entities()
        if doc_bom.blocks.get('BOM_FIRST'):
            border_insert = doc_bom.modelspace().add_blockref(name='BOM_FIRST',
                                                              insert=(0, 0))
            border_insert.add_auto_attribs(values)

            return border_insert

    def create_BOM_SECOND(self,doc_bom):
        '''Создает первый лист спецификации'''

        block_border = doc_bom.blocks['BOM_SECOND']
        values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
        doc_bom.modelspace().delete_all_entities()
        if doc_bom.blocks.get('BOM_SECOND'):
            border_insert = doc_bom.modelspace().add_blockref(name='BOM_SECOND',
                                                              insert=(0, 0))
            border_insert.add_auto_attribs(values)

            return border_insert

