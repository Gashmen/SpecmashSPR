
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
            if ',' in self.production_cost:
                self.production_cost.replace(',','.')

    def set_work_cost(self):
        if hasattr(self,'shell_full_information'):
            self.work_cost = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_РАБОТА'])
            if ',' in self.work_cost:
                self.work_cost.replace(',','.')

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
                'Примечание':'ВЗОР'
                }
            }
        print(self.bom_dict)


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
            self.vrpt_name = str(self.gland_full_information['Чертеж основной']) + '-' + str(self.gland_full_information['Исполнение'])
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
                'Примечание':'ВЗОР'
                }
            }
        print(self.bom_dict)

    def add_options_bom(self):
        if hasattr(self,'bom_dict'):
            self.bom_dict[tuple([f'Уплотнительное кольцо Ду {self.gland.cable_type_size}, полимер'])] =\
                {
                    'Формат': "",
                    'Зона': "",
                    'Поз.': "",
                    'Обозначение': f'УК{self.gland.cable_type_size}',
                    'Наименование': [f'Уплотнительное кольцо Ду {self.gland.cable_type_size}, полимер'],
                    'Кол.': '',
                    'Примечание': 'ВЗОР'
                }

            if self.gland.kz == True:
                self.bom_dict[tuple([f'Кольцо заземления Ду {self.gland.cable_type_size}-6,','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': f'КЗ{self.gland.cable_type_size}',
                        'Наименование': [f'Кольцо заземления Ду {self.gland.cable_type_size}-6,','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР'
                    }

            if self.gland.gsh == True:
                self.bom_dict[tuple([f'Гроверная шайба {self.gland.cable_type_size},','нержавеющая сталь AISI 304'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': f'ГШ{self.gland.cable_type_size}',
                        'Наименование': [f'Гроверная шайба {self.gland.cable_type_size},','нержавеющая сталь AISI 304'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР'
                    }

            if self.gland.kg == True:
                self.bom_dict[tuple([f'Контргайка М{self.gland.cable_type_size}х1.5,','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': f'КГ{self.gland.cable_type_size}',
                        'Наименование': [f'Контргайка М{self.gland.cable_type_size}х1.5,','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР'
                    }

            if self.gland.vz_vz == True:
                self.bom_dict[tuple([f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': f'ВЗ-ВЗ{self.gland.cable_type_size}',
                        'Наименование': [f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР'
                    }

            if self.gland.vz_vze == True:
                self.bom_dict[tuple([f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': f'ВЗ-ВЗе{self.gland.cable_type_size}',
                        'Наименование': [f'Взрывозащищенная защитная пробка',f'для кабельных вводов М{self.gland.cable_type_size},','никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР'
                    }
            if self.gland.ch == True:
                self.bom_dict[tuple([f'Чехол защитный М{self.gland.cable_type_size}'])] = \
                    {
                        'Формат': "",
                        'Зона': "",
                        'Поз.': "",
                        'Обозначение': f'ВЗ-ВЗе{self.gland.cable_type_size}',
                        'Наименование': [f'Взрывозащищенная защитная пробка',
                                         f'для кабельных вводов М{self.gland.cable_type_size},',
                                         'никелированная латунь'],
                        'Кол.': '',
                        'Примечание': 'ВЗОР'
                    }

class BOM_GENERAL:
    tag_in_BOM_dxf = {'Формат': 'A', 'Зона': 'B', 'Поз.': 'C', 'Обозначение': 'D', 'Наименование': 'E', 'Кол.': 'F',
                      'Примечание': 'G', 'Цена': 'H'}
    def __init__(self):
        self.list_elements = []
        self.bom_dict = dict()

    def add_bom_list_elements(self,BOM:dict):
        self.list_elements.append(BOM)
        # for dict_elements in self.list_elements:
        #     for element in dict_elements:
        #         if element not in



