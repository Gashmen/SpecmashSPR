shell_side_dxf = 'upside'
main_surface = {'xy0': [0.0, 8.0], 'xy1': [120.0, 71.8]}
max_size = 120
min_size = 63.8

list_with_diametrs_float = [21.9, 21.9, 21.9]
list_on_side = [['ВЗ-Н12', 21.9], ['ВЗ-Н12', 21.9], ['ВЗ-Н12', 21.9]]

dict_on_side = {0: ['ВЗ-Н12', 21.9], 1: ['ВЗ-Н12', 21.9], 2: ['ВЗ-Н12', 21.9]}

keynumber_for_delete_input = 0
start_rectangle = 0

#Сначала идет проверка в целом на возможность вставки кабельного ввода самого большого
if input_create_expamles_check.check_possible_to_add_all_inputs_in_one_row(
        free_space=max_size - start_rectangle,
        list_with_diametrs_float=[list(i)[1] for i in dict_on_side.values()]):#сначала идет проверка на возможность вставки в один ряд оставшихся кабельнных вводов

    keynumber_for_delete_input = list(dict_on_side.keys())[0]#Номер ключа для установки на сторону
    diametr_gland = dict_on_side[keynumber_for_delete_input][1]#Диаметр этой окружности

    x_coordinate = input_create_expamles_check.calculate_x_one_row( # координата x в одну строчку
        start_rectangle_for_paint=start_rectangle,
        diametr_float=diametr_gland)
    y_coordinate = main_surface['xy0'][1] + min_size / 2 # середина зоны сверловки

    coordinate_input_one_row = input_create_expamles_check.set_coordinate_one_row( # получение [x_coordinate,y_coordinate]
        x_coordinate=x_coordinate, y_coordinate=y_coordinate)

    self.dict_with_list_coordinates_on_side_for_dxf[shell_side][keynumber_for_delete_input] = \
        {dict_on_side_copy[keynumber_for_delete_input][0]: coordinate_input_one_row}#записываем в словарь self.dict_with_list_coordinates_on_side_for_dxf координаты {'А': {0: {'ВЗ-Н12': [10.95, 39.9]}}, 'Б': {}, 'В': {}, 'Г': {}, 'Крышка': {}}

    start_rectangle = input_create_expamles_check.find_start_of_rectangle_one_row( #устанавливаем новый старт rectangle
        start_rectangle=start_rectangle,
        diametr_float=list_with_diametrs_float[keynumber_for_delete_input])

    # в конце удаление ввода
    input_create_examples.delete_input_from_dict(dict_with_inputs_name_and_diam=dict_on_side,
                                                 keynumber_for_delete_input=keynumber_for_delete_input)
    if dict_on_side == {}:
        free_space = max_size - start_rectangle + 5
        if max(list(self.dict_with_list_coordinates_on_side_for_dxf[shell_side].keys())) == 0:
            for number in self.dict_with_list_coordinates_on_side_for_dxf[shell_side]:
                for input_rus_name in self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number]:
                    self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number][
                        input_rus_name][0] = main_surface['xy0'][0] + max_size / 2
        else:
            for number in self.dict_with_list_coordinates_on_side_for_dxf[shell_side]:
                for input_rus_name in self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number]:
                    self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number][input_rus_name][0] = \
                        self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number][
                            input_rus_name][0] + free_space * (number + 1) / (
                                    max(list(self.dict_with_list_coordinates_on_side_for_dxf[shell_side].keys())) + 2)
#Сначала идет проверка в целом на возможность вставки кабельного ввода самого большого
#Здесь должна появится переменная отвечающая за ширину widht и level_dict для создания уровней
#проверка на возможность вставки кабельного ввода хотя бы одного по оставшейся ширине
#далее, если widht == min_size то создать уровень

