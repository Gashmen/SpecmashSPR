'''ЛИСТ С ФУНКЦИЯМИ, КОТОРЫЕ ИЗ СУЩЕСТВУЮЩИХ КЛАССОВ СМОГУТ ЗАРАНЕЕ ПОСЧИТАТЬ ДЛИНУ МЕЖДУ ВСЕМИ БЛОКАМИ'''

def downside_insert_bottom_coordinate(max_length_gland_upside:float,topside_extreme_lines:dict):
    '''
    Расчет нижней координаты для downside
    :param max_length_gland_upside:самый длинный кабельный ввод на стороне upside,т.к. от него будет зависеть
    где стоит оболочка
    :param topside_extreme_lines: dict['y_max'] нужно, т.к. нужна верхняя точка topside
    :return:нижняя координата y для блока downside
    '''
    return topside_extreme_lines['y_max']+max_length_gland_upside

def upside_insert_top_coordinate(max_length_gland_downside:float, topside_extreme_lines:dict):
    '''
    Расчет нижней координаты для downside
    :param max_length_gland_downside:самый длинный кабельный ввод на стороне downside,т.к. от него будет зависеть
    где стоит оболочка
    :param topside_extreme_lines: dict['y_min'] нужно, т.к. нужна нижняя точка topside
    :return:Верхняя координата y для блока upside
    '''
    return topside_extreme_lines['y_min'] - max_length_gland_downside

def rightside_insert_right_coordinate(max_length_gland_leftside:float, topside_extreme_lines:dict):
    '''
    Расчет нижней координаты для downside
    :param max_length_gland_leftside:самый длинный кабельный ввод на стороне leftside,т.к. от него будет зависеть
    где стоит оболочка
    :param topside_extreme_lines: dict['x_min'] нужно, т.к. нужна левая точка topside
    :return:Правая координата для блока rightside
    '''
    return topside_extreme_lines['x_min'] - max_length_gland_leftside

def leftside_insert_left_coordinate(max_length_gland_rightside:float, topside_extreme_lines:dict):
    '''
    Расчет нижней координаты для downside
    :param max_length_gland_leftside:самый длинный кабельный ввод на стороне leftside,т.к. от него будет зависеть
    где стоит оболочка
    :param topside_extreme_lines: dict['x_max'] нужно, т.к. нужна левая точка topside
    :return:Левая координата для блока leftside
    '''
    return topside_extreme_lines['x_max'] + max_length_gland_rightside

def cutside_insert_left_coordinate(max_length_gland_topside:float, leftside_insert_left_coordinate:float,
                                   leftside_extreme_lines:dict):
    '''
    Получение левой координаты
    :param max_length_gland_topside: длина лампочки или шильда какого либа, или чего еще
    :param leftside_insert_left_coordinate: из функции leftside_insert_left_coordinate()
    :param leftside_extreme_lines: leftside_extreme_lines['x_max']
    :return:
    '''
    len_leftside_insert = leftside_extreme_lines['y_max'] - leftside_extreme_lines['y_min']
    return leftside_insert_left_coordinate + len_leftside_insert + max_length_gland_topside

# if __name__ == '__main__':


