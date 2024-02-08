from src.examples import create_inputs_check
from src.examples import create_inputs

class InputsLevelX:

    def __init__(self):
        self.x_coordinate:float = None
        self.include_inputs:dict = None
        self.free_space_y:float = None
        self.free_space_x:float = None

    def define_free_space_y(self,width):
        if self.free_space_y == None:
            self.free_space_y = width
        else:
            self.free_space_y = width - list(self.include_inputs.values())[-1]


def check_existence_levels(level_dict:dict):
    '''
    Проверка, существует ли уровень
    :param level_dict: {}
    :return: True or False
    '''

    if level_dict == {} or level_dict == None:
        return False
    else:
        return True

def calculate_start_rectangle(start_rectangle_now:float=None, last_level_coordinates_x:float=None):
    '''
     Получение координаты x для установки кабельного ввода
     :param start_rectangle_for_paint: Координата начала зоны сверления для данного уровня. получается так, что к предыдущему началу прибавляем диаметр и 5мм
     :param last_level_coordinates_x: координата x для предыдущего уровня
     :return: x_coordinate
     '''
    if start_rectangle_for_paint == None:
        raise ValueError('Не была задана координата начального уровня для зоны сверления уровня')
    if last_level_coordinates_x == None:
        raise ValueError('Не задан предыдущий уровень координаты x')
    start_rectangle_now = last_level_coordinates_x
    return start_rectangle_now

def create_level(level_dict, input_information:list, start_rectangle:float):
    '''
    Создание нового уровня в словаре уровня
    :param level_dict: {x_coordinate: [input_information]...
    :param input_information:['ВЗ-Н25' : 42.6]
    :param start_rectangle: 78
    :return:level_dict с новой инфой {x_coordinate:[['ВЗ-Н25' : 42.6],...]}
    '''
    if level_dict != None and isinstance(level_dict, dict):
        diametr_gland = input_information[-1]
        x_coordinate = start_rectangle + diametr_gland/2
        level_dict[x_coordinate] = [input_information]
        # return level_dict

def calculate_x_for_many_row_algoritm(level_x_coordinate:float=None):
    '''
    Расчет координаты x для случая друг под другом
    :param level_x_coordinate: координата данного уровня по x.
    :return:None or level_x_coordinate
    '''
    if level_x_coordinate == None:
        return None
    elif isinstance(level_x_coordinate, float):
        return level_x_coordinate
    else:
        raise BaseException('Не задана level_x_coordinate для случая расстановки второго уровня')


def search_inputs_can_insert_in_level(free_width:float=None,
                                      dict_inputs:float=None):
    '''
    Поиск ввода который поместится снизу
    :param free_width: свободное пространство
    :param dict_inputs: {0:['ВЗ-Н40',40], 1:['ВЗ-Н32',30], 2:['ВЗ-Н25',20]}
    :param number_input_in_second_level: 2
    :return:
    '''
    if dict_inputs is not None:
        for keynumber_input in dict_inputs:
            if free_width >= dict_inputs[keynumber_input][-1]:
                number_input_in_second_level = keynumber_input
                return number_input_in_second_level
                # break


def check_possible_to_create_level(dict_with_inputs_information:dict, width:float):
    '''
    Проверка, есть ли вообще окружности, которые могут быть друг под другом
    :param dict_with_inputs_information:{0: ['ВЗ-Н25', 37.3], 1: ['ВЗ-Н25', 37.3], 2: ['ВЗ-Н25', 37.3], 3: ['ВЗ-Н25', 37.3], 4: ['ВЗ-Н25', 37.3], 5: ['ВЗ-Н25', 37.3]}
    :param width: 62.2
    :return:
    '''
    possible_create_levels = False
    if len(list(dict_with_inputs_information.keys())) > 1:
        list_with_diams = [i[1] for i in dict_with_inputs_information.values()]

        for i in list_with_diams:
            diam_width = list()
            for j in list_with_diams:
                if width >= i+j+5:
                    possible_create_levels = True
                    break
            break

    return possible_create_levels

def create_new_level(level_dict:dict, dict_with_inputs_information:dict, min_size:float,max_size:float):

    '''
    :param level_dict = {16.6:{0:['ВЗ-Н32', {’x’:x_0, ‘y’:y_0,'D':diam_0}],1:{’x’:x_1, ‘y’:y_1,'D':diam_1}….., 57.5:..}
    :param dict_with_inputs_information:{0: ['ВЗ-Н25', 37.3], 1: ['ВЗ-Н25', 37.3], 2: ['ВЗ-Н25', 37.3], 3: ['ВЗ-Н25', 37.3], 4: ['ВЗ-Н25', 37.3], 5: ['ВЗ-Н25', 37.3]}
    :param min_size: 62.6
    :param max_size 216
    :return:
    '''

    if level_dict == {} or level_dict == None:
        x_coordinate = dict_with_inputs_information[0][1]/2
        y_coordinate = dict_with_inputs_information[0][1]/2
        name_cable_input = dict_with_inputs_information[0][0]
        level_dict[dict_with_inputs_information[0][1]/2] = \
            {0:[name_cable_input,{'x':x_coordinate,
                                  'y':y_coordinate,
                                  'D':dict_with_inputs_information[0][1]}]}

        min_size -= dict_with_inputs_information[0][1]

    else:
        number_of_diam = min(list(dict_with_inputs_information.keys()))
        x_coordinate = dict_with_inputs_information[number_of_diam][1]/2
        y_coordinate = dict_with_inputs_information[number_of_diam][1]/2
        name_cable_input = dict_with_inputs_information[number_of_diam][0]

        previous_coordinate = list_dict[min(list(list_dict.keys()))]
        previous_biggest_diam = list_dict[previous_coordinate][0]['D']

        level_dict[previous_coordinate + 5 + previous_biggest_diam/2 + x_coordinate] = \
            {0:[name_cable_input,{'x':previous_coordinate + 5 + previous_biggest_diam/2 + x_coordinate,
                                  'y':y_coordinate,
                                  'D':dict_with_inputs_information[number_of_diam][1]}]}

        min_size -= dict_with_inputs_information[number_of_diam][1]

def check_free_space_in_level(dict_with_inputs_information:dict, widht:float):
    '''
    Проверка на возможность добавление какого-либо кабельного ввода
    :param dict_with_inputs_information: {0: ['ВЗ-Н25', 37.3], 1: ['ВЗ-Н25', 37.3], 2: ['ВЗ-Н25', 37.3], 3: ['ВЗ-Н25', 37.3], 4: ['ВЗ-Н25', 37.3], 5: ['ВЗ-Н25', 37.3]}
    :param widht: 14.5
    :return:
    '''
    if widht <= min([i[1] for i in dict_with_inputs_information.values()]):
        return False
    else:
        return True

def add_to_level_input(dict_with_inputs_information:dict, level_dict:dict,widht:float):
    '''
    Добавление кабельного ввода в уровень, когда уже там есть кабельный ввод
    Функция должна использоваться после check_free_space_in_level -> смотри функцию выше

    :param dict_with_inputs_information: {0: ['ВЗ-Н25', 37.3], 1: ['ВЗ-Н25', 37.3], 2: ['ВЗ-Н25', 37.3], 3: ['ВЗ-Н25', 37.3], 4: ['ВЗ-Н25', 37.3], 5: ['ВЗ-Н25', 37.3]}
    :param level_dict: {16.6:{0:['ВЗ-Н32', {’x’:x_0, ‘y’:y_0,'D':diam_0}],1:{’x’:x_1, ‘y’:y_1,'D':diam_1}….., 57.5:..}
    :param current_level: 16.6
    :return: current_input ['ВЗ-Н25', 37.3]
    '''

    #Если проверка на check_free_space_in_level пройдена
    #Если уровень создан, т.к. создается за счет create_new_level
    current_level = list(level_dict.keys())[-1]
    current_inputs_level = level_dict[current_level]

    level_dict[list(level_dict.keys())[-1]]

if __name__ == '__main__':

    list_inputs_gland = ['ВЗ-Н25', 'ВЗ-Н32', 'ВЗ-Н40']
    list_inputs_gland = [20, 30, 40]

    dict_inputs = {0: ['ВЗ-Н12', 21.9], 1: ['ВЗ-Н12', 21.9], 2: ['ВЗ-Н12', 21.9], 3: ['ВЗ-Н12', 21.9], 4: ['ВЗ-Н12', 21.9], 5: ['ВЗ-Н12', 21.9], 6: ['ВЗ-Н12', 21.9], 7: ['ВЗ-Н12', 21.9]}

    dict_inputs_copy = dict_inputs.copy()
    max_size = 96.3
    min_size = 56.8
    keynumber_for_delete_input = 0
    number_input_in_second_level = None
    start_rectangle = 0
    width = min_size
    level_dict = dict()
    #Если нельзя в один уровень
    check_possible = check_possible_to_create_level(dict_with_inputs_information=dict_inputs,width=width)
    result_dict = dict()
    keynumber_for_delete_input = None

    while create_inputs.checking_clear_inputs_dict(dict_with_inputs_name_and_diam=dict_inputs):
        #Если не помещается в одну линию
        if check_possible:
            if width == min_size:

                #получаем первый кабельный ввод
                keynumber_for_delete_input = list(dict_inputs.keys())[0]
                input_information = dict_inputs[keynumber_for_delete_input]

                #создаем уровень
                create_level(level_dict=level_dict,
                             input_information=input_information,
                             start_rectangle=start_rectangle)

                x_coordinate = list(level_dict.keys())[-1]
                diametr_gland = input_information[-1]
                if x_coordinate + diametr_gland/2 > max_size:
                    break

                start_rectangle += diametr_gland + 5

                y_coordinate = diametr_gland/2

                coordinate_input = [x_coordinate,y_coordinate]
                name_gland = input_information[0]
                result_dict[keynumber_for_delete_input] = {name_gland:coordinate_input}

                width -= y_coordinate + diametr_gland/2

                del dict_inputs[keynumber_for_delete_input]

            elif 0 <= width < min_size:

                number_input_in_second_level = search_inputs_can_insert_in_level(free_width=width,
                                                                                 dict_inputs=dict_inputs)
                if number_input_in_second_level == None:
                    width = min_size
                    continue

                input_information = dict_inputs[number_input_in_second_level]

                x_coordinate = list(level_dict.keys())[-1]
                previous_y = list(result_dict[keynumber_for_delete_input].values())[-1][-1]
                y_coordinate = 5 + diametr_gland/2 + previous_y

                keynumber_for_delete_input = number_input_in_second_level

                coordinate_input = [x_coordinate, y_coordinate]
                name_gland = input_information[0]
                result_dict[keynumber_for_delete_input] = {name_gland:coordinate_input}

                width -= 5 + diametr_gland

                del dict_inputs[keynumber_for_delete_input]

            else:
                width = min_size

    print(result_dict)
                # if width:
                #     width = min_size
                #     # start_rectangle =
                #
                # else:
                #     width -= list(level_dict.values())[-1][-1] - 5




