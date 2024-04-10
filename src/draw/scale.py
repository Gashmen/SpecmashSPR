import math

from src.draw.gland import dxf_gland
from src.const import BOUNDARIES,SCALE
class ScaleBorder:

    '''
    Расчет масштаба
    В нотион ссылка https://www.notion.so/di258/9212076572da402bba2c9453ff640b88
    Но здесь надо переписать будет на каждую длину
    len0_x = максимальная длина ввода или чего угодно от топ сайда###############
    len1_x = длина rightside блока############
    len2_x = максимальная длина кабельного ввода на стороне Г(leftside)############# - ###нужно оставить еще место для обозначения масштаба###
    len3_x = длина topside блока###############
    len4_x = максимальная длина кабельного ввода на стороне Б##############
    len5_x = длина leftside блока###########
    len6_x = len0 = максимальная длина ввода или чего угодно от топ сайда#################
    len7_x = len5 - Длина cutside блока##########
    len8_x = len0 = максимальная длина ввода или чего угодно от топ сайда################
    len9_x = len2 = максимальная длина кабельного ввода на стороне Г(leftside)################
    len10_x = len3 = длина topside блока##############
    len11_x = len4 = максимальная длина кабельного ввода на стороне Б###############


    len0_y - максимальная длина ввода или чего угодно от топ сайда############
    len1_y - длина upside блока#############
    len2_y - максимальная длина кабельного ввода сторона В(downside)###нужно оставить еще место для обозначения масштаба#########
    len3_y - ширина topside Блока############
    len4_y - максимальная длина кабельного ввода сторона А(upside)#############
    len5_y - длина downside Блока############
    len6_y = len0_y - максимальная длина ввода или чего угодно от топ сайда##############
    '''

    def calculate_len0_x(self,glands_on_sides_dxf_dict:dict[str:list[dxf_gland.GlandDxfCircle]]):
        '''Принимает glands_on_sides_dict c dxf информацией'''
        rus_cover_name = 'Крышка'
        max_length_gland = 0
        if len(glands_on_sides_dxf_dict[rus_cover_name])>0:
            max_length_gland = max([gland.gland_length_dxf for gland in glands_on_sides_dxf_dict[rus_cover_name]])
        self.len0_x = max_length_gland
        # return max_length_gland

    def calculate_len1_x(self,rightside_extreme_lines:dict[str:float]):
        '''Принимает словарь rightside_extreme_lines'''
        self.len1_x = rightside_extreme_lines['y_max'] - rightside_extreme_lines['y_min']
        # return len1_x

    def calculate_len2_x(self,glands_on_sides_dxf_dict:dict[str:list[dxf_gland.GlandDxfCircle]]):
        '''Получение максимального размера dxf для кабельного ввода на стороне Г(leftside)'''
        rus_side_name = 'Г'
        max_length_gland = 0
        if len(glands_on_sides_dxf_dict[rus_side_name]) > 0:
            max_length_gland = max([gland.gland_length_dxf for gland in glands_on_sides_dxf_dict[rus_side_name]])
        self.len2_x = max_length_gland
        # return max_length_gland

    def calculate_len3_x(self,topside_extreme_lines:dict[str:float]):
        '''len3_x = длина topside блока'''
        self.len3_x = topside_extreme_lines['x_max'] - topside_extreme_lines['x_min']
        # return len3_x

    def calculate_len4_x(self,glands_on_sides_dxf_dict:dict[str:list[dxf_gland.GlandDxfCircle]]):
        '''максимальная длина кабельного ввода на стороне Б'''
        rus_side_name = 'Б'
        max_length_gland = 0
        if len(glands_on_sides_dxf_dict[rus_side_name]) > 0:
            max_length_gland = max([gland.gland_length_dxf for gland in glands_on_sides_dxf_dict[rus_side_name]])
        self.len4_x = max_length_gland
        # return max_length_gland

    def calculate_len5_x(self,leftside_extreme_lines:dict[str:float]):
        '''длина leftside блока'''
        self.len5_x = leftside_extreme_lines['y_max'] - leftside_extreme_lines['y_min']
        # return len5_x

    def calculate_len6_x(self):
        '''len6_x = len0:calculate_len0_x = максимальная длина ввода или чего угодно от топ сайда'''
        if hasattr(self,'len0_x'):
            self.len6_x = self.len0_x
        # return len6_x

    def calculate_len7_x(self):
        '''len7_x = len5 - Длина cutside блока'''
        if hasattr(self,'len5_x'):
            self.len7_x = self.len5_x
        # return len7_x

    def calculate_len8_x(self):
        '''len8_x = len0:calculate_len0_x = максимальная длина ввода или чего угодно от топ сайда'''
        if hasattr(self, 'len0_x'):
            self.len8_x = self.len0_x
        # return len8_x

    def calculate_len9_x(self):
        '''len9_x = len2 = максимальная длина кабельного ввода на стороне Г(leftside)'''
        if hasattr(self,'len2_x'):
            self.len9_x = self.len2_x
            # return len9_x
    def calculate_len10_x(self):
        '''len10_x = len3 = длина topside блока'''
        if hasattr(self,'len3_x'):
            self.len10_x = self.len3_x
            # return len10_x

    def calculate_len11_x(self,):
        '''len11_x = len4 = максимальная длина кабельного ввода на стороне '''
        if hasattr(self,'len4_x'):
            self.len11_x = self.len4_x
            # return len11_x

    def calculate_len0_y(self):
        '''len0_y - максимальная длина ввода или чего угодно от топ сайда'''
        if hasattr(self,'len0_x'):
            self.len0_y = self.len0_x
            # return len0_y

    def calculate_len1_y(self,upside_extreme_lines:dict[str:float]):
        '''len1_y - длина upside блока'''
        self.len1_y = upside_extreme_lines['y_max'] - upside_extreme_lines['y_min']
        # return len1_y

    def calculate_len2_y(self,glands_on_sides_dxf_dict:dict[str:list[dxf_gland.GlandDxfCircle]]):
        '''len2_y - максимальная длина кабельного ввода сторона В(downside)###нужно оставить еще место для обозначения масштаба###'''
        rus_side_name = 'В'
        max_length_gland = 0
        if len(glands_on_sides_dxf_dict[rus_side_name]) > 0:
            max_length_gland = max([gland.gland_length_dxf for gland in glands_on_sides_dxf_dict[rus_side_name]])
        self.len2_y = max_length_gland
        # return max_length_gland

    def calculate_len3_y(self,topside_extreme_lines:dict[str:float]):
        '''len3_y = ширина topside блока'''
        self.len3_y = topside_extreme_lines['y_max'] - topside_extreme_lines['y_min']
        # return self.len3_y

    def calculate_len4_y(self,glands_on_sides_dxf_dict:dict[str:list[dxf_gland.GlandDxfCircle]]):
        '''len4_y - максимальная длина кабельного ввода сторона А(upside)'''
        rus_side_name = 'А'
        max_length_gland = 0
        if len(glands_on_sides_dxf_dict[rus_side_name]) > 0:
            max_length_gland = max([gland.gland_length_dxf for gland in glands_on_sides_dxf_dict[rus_side_name]])
        self.len4_y = max_length_gland
        # return max_length_gland


    def calculate_len5_y(self,installation_extreme_lines:dict[str:float]):
        '''len3_y = ширина topside блока'''
        self.len5_y = installation_extreme_lines['y_max'] - installation_extreme_lines['y_min']
        # return len5_y

    def calculate_len6_y(self):
        '''len0_y - максимальная длина ввода или чего угодно от топ сайда'''
        if hasattr(self,'len0_x'):
            self.len6_y = self.len0_x
        # return len6_y


    def calculate_len_x_bottom(self,len_x_bottom,scale_gost=1):
        needed_parametrs = [self.len0_x, self.len1_x,self.len2_x,self.len3_x,self.len4_x]
        sum_len_x_bottom = sum(needed_parametrs) + 1.5*max(self.len2_y,self.len2_x,self.len4_y,self.len4_x)#для вставки размера
        self.scale_len_x_bottom = math.floor(sum_len_x_bottom/scale_gost)
        if self.scale_len_x_bottom <= len_x_bottom:
            return True
        else:
            return False

    def calculate_len_x_top(self,len_x_top=BOUNDARIES.A3_BOUNDARIES['LEN_X_ВЕРХНЯЯ_ГРАНИЦА'],scale_gost=1):
        needed_parametrs = [self.len0_x,self.len1_x,self.len2_x,self.len3_x,self.len4_x,
                            self.len5_x,self.len6_x,self.len7_x,self.len8_x,self.len9_x,
                            self.len10_x,self.len11_x]
        sum_len_x_top = sum(needed_parametrs) + 1.5*max([self.len2_y,self.len2_x,self.len4_y,self.len4_x])#для вставки размера
        self.scale_len_x_top = math.floor(sum_len_x_top / scale_gost)+1
        if self.scale_len_x_top <= len_x_top:
            return True
        else:
            return False

    def calculate_len_y_left(self,len_y_left=BOUNDARIES.A3_BOUNDARIES['LEN_Y_ЛЕВАЯ_ГРАНИЦА'],scale_gost=1):
        needed_parametrs = [self.len0_y,self.len1_y,self.len2_y,self.len3_y,self.len4_y,self.len5_y,self.len6_y]
        sum_len_y_left = sum(needed_parametrs) + 1.5*max(self.len2_y,self.len2_x,self.len4_y,self.len4_x)#для вставки размера
        self.scale_len_y_left = math.floor(sum_len_y_left / scale_gost)
        if self.scale_len_y_left <= len_y_left:
            return True
        else:
            return False

    def calculate_len_y_right(self,len_y_right,scale_gost=1):
        needed_parametrs = [self.len2_y,self.len3_y,self.len4_y,self.len5_y,self.len6_y]
        sum_len_y_right = sum(needed_parametrs)
        self.scale_len_y_right = math.floor(sum_len_y_right / scale_gost)
        if self.scale_len_y_right <= len_y_right:
            return True
        else:
            return False

    def calculate_scale(self,boundaries:dict = BOUNDARIES.A3_BOUNDARIES):
        if hasattr(self,'len1_x'):
            conditions = False
            i=0
            while conditions == False:
                self.scale = SCALE.SCALE_GOST[i]
                self.scale_border = self.scale
                i += 1
                conditions = all([
                    self.calculate_len_x_bottom(len_x_bottom=boundaries['LEN_X_НИЖНЯЯ_ГРАНИЦА'],scale_gost=self.scale),
                    self.calculate_len_x_top(len_x_top=boundaries['LEN_X_ВЕРХНЯЯ_ГРАНИЦА'],scale_gost=self.scale),
                    self.calculate_len_y_left(len_y_left=boundaries['LEN_Y_ЛЕВАЯ_ГРАНИЦА'],scale_gost=self.scale),
                    self.calculate_len_y_right(len_y_right=boundaries['LEN_Y_ПРАВАЯ_ГРАНИЦА'],scale_gost=self.scale)
                ])
                self.calculate_free_space()


    def calculate_free_space(self,boundaries:dict = BOUNDARIES.A3_BOUNDARIES):
        self.free_space_x = boundaries['LEN_X_ВЕРХНЯЯ_ГРАНИЦА'] - self.scale_len_x_top
        self.free_space_y = boundaries['LEN_Y_ЛЕВАЯ_ГРАНИЦА'] - self.scale_len_y_left

    def set_zero_len_without_glands(self):
        self.len0_x = 0
        self.len2_x = 0
        self.len4_x = 0
        self.len6_x = 0
        self.len8_x = 0
        self.len9_x = 0
        self.len11_x = 0

        self.len0_y = 0
        self.len2_y = 0
        self.len4_y = 0
        self.len6_y = 0






