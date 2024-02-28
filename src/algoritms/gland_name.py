import pandas as pd
import openpyxl


gland_csv_path = 'Кабельные вводы ВЗОР (рев.6).csv'

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
            if self.gland_main_dict_copy[key_number]['Тип'] == self.gland_designation and\
                self.gland_main_dict_copy[key_number]['Материал'] == self.gland_material and \
                self.gland_main_dict_copy[key_number]['Тип кабеля'] == self.gland_cable_type and\
                self.gland_main_dict_copy[key_number]['Тип резьбы'] == self.gland_thread:
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

        gland_diam_range_qt = list(set(self.cable_min_diam,self.cable_max_diam))
        #Здесь получили все кабельные вводы, с которыми есть пересечение
        if self.gland_cable_type == 'Небронированный' or self.gland_cable_type == 'Бронированный':
            for key_gland in self.dict_for_calculate_gland_diam:
                gland_min_diam_csv = self.dict_for_calculate_gland_diam[key_gland]['Мин диаметр внешнего обжатия кабеля']
                gland_max_diam_csv = self.dict_for_calculate_gland_diam[key_gland]['Макс диаметр внешнего обжатия кабеля']
                range_diam_csv = list(map(set_correct_number,[gland_min_diam_csv,gland_max_diam_csv]))
                if list(set(gland_diam_range_qt) & set(range_diam_csv)) != []:
                    result_dict[key_gland] = list(set(gland_diam_range_qt) & set(range_diam_csv))
            max_сoincidence_range = len(max(result_dict.values()))

        #Здесь оставили только те, в которых максимальное количество совпадений по промежутку
        for key_gland in result_dict.copy():
            if len(result_dict[key_gland]) == max_сoincidence_range:
                continue
            else:
                del result_dict[key_gland]

        #теперь оставляем только один, такой, чтобы у него был наименьший диаметр из оставшихся и не было дополнительных диапазонов
        #т.е. если есть М25 и М25Р и она оба одинаковый диапазон, надо оставить М25
        min_gland = None
        modification = None
        key_gland_main = None
        for key_gland in result_dict:
            if min_gland == None:
                min_gland = int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера'])
                modification = str(self.glands_correct_diametr[key_gland]['Модификация'])
                key_gland_main = key_gland
            else:
                if min_gland > int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера']):
                    min_gland = int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера'])
                    modification = str(self.glands_correct_diametr[key_gland]['Модификация'])
                    key_gland_main = key_gland
                elif min_gland == int(self.glands_correct_diametr[key_gland]['Типоразмер резьбы штуцера']):
                    if modification == 'Нет':
                        continue
                    else:
                        modification = str(self.glands_correct_diametr[key_gland]['Модификация'])
                        key_gland_main = key_gland



class CableGlandInformation:

    def __init__(self,gland_dict):
        self.set_gland_dict(gland_dict=gland_dict)
        self.set_properties()
        self.create_name()

    def set_gland_dict(self, gland_dict):
        self.gland_dict = gland_dict

    def create_name(self):
        self.gland_russian_name = ''
        if hasattr(self,'material_gland'):
            self.gland_russian_name += self.material_gland + '-' + self.cable_type + self.cable_type_size #Добавляем материал + тип кабеля

            if self.tube_type != None:
                if hasattr(self,'internal_tube_size'):
                    self.gland_russian_name += '-' + 'Т' + self.internal_tube_size + self.internal_tube_status + '(В)'
                elif hasattr(self,'external_tube_status'):
                    self.gland_russian_name += '-' + 'Т' + self.external_tube_size + self.external_tube_status + '(Н)'

            if self.metalhose != None:
                self.gland_russian_name += '-' + self.metalhose

    def set_properties(self):
        self.set_material()
        self.set_cable_type()
        self.set_cable_type_size()
        self.set_metalhose()
        self.set_tube()

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


if __name__ == '__main__':
    gland_main_dict = GlandMainDictQt(gland_csv_path=gland_csv_path)
    gland_main_dict.set_main_dict(main_path=gland_csv_path)
    gland_main_dict.set_only_gland_type()
    gland_main_dict = gland_main_dict.gland_main_dict



    # print(gland_main_dict)

    dict_all_names = dict()
    for key_number in gland_main_dict:
        gland_dict = gland_main_dict[key_number]
        cable_gland = CableGlandInformation(gland_dict)
        dict_all_names[key_number] = cable_gland.gland_russian_name
        # print(cable_gland.gland_russian_name)

    wb = openpyxl.Workbook()
    sheet1 = wb.active
    for row_number, value in dict_all_names.items():
        print(row_number+1)
        print(value)
        sheet1.cell(row=int(row_number+1),column=1,value=value)
    wb.save('test.xlsx')


    print(len(dict_all_names))


    print(gland_main_dict)


