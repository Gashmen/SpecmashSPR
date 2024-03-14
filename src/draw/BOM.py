
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
                self.vrpt_name.split('#')
            self.vrpt_name = list(self.vrpt_name)

    def set_fullname(self):
        if hasattr(self,'shell_full_information'):
            self.fullname = str(self.shell_full_information['СПЕЦИФИКАЦИЯ_НАИМЕНОВАНИЕ'])
            if '#' in self.fullname:
                self.fullname.split('#')
            self.fullname = list(self.fullname)

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
            {self.fullname:
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


class BOM_GLAND:

    def set_glands_dict(self,glands_dxf_dict):
        self.glands_dict = glands_dxf_dict

    def shell_name(self):











