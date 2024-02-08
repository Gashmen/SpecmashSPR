from src.things.input import CableGlandCsv

class LevelColumnType:

    def __init__(self,height_y):
        self._x_coordinate = None #
        self.height_free_space = height_y
        self.glands = list()

    @property
    def x_coordinate(self):
        return self._x_coordinate

    @x_coordinate.setter
    def x_coordinate(self,value):
        self._x_coordinate = value

    def add_gland(self,gland:CableGlandCsv):

        if isinstance(gland,CableGlandCsv):
            self.glands.append(gland)
            self.height_free_space -= gland.diametr - 5

    def align_glands(self):
        '''Установка по центру самого большого кабельного ввода'''
        if len(self.glands) > 0:
            main_gland = self.glands[0]
            # self.y_coordinate = main_gland.







