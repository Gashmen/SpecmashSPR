class DxfGlandSurfaceOnSide:

    def __init__(self):
        self._side = None
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self,value):
        self._side = value

    def set_main_coordinates(self, surface_coordinates:dict):
        '''
        Передача каждой координате данных
        :param surface_coordinates: {'xy0': [0.0, 8.0], 'xy1': [120.0, 71.8]}
        '''
        if isinstance(surface_coordinates,dict):
            if surface_coordinates.__getitem__('xy0') and surface_coordinates.__getitem__('xy1'):
                self._x0 = surface_coordinates['xy0'][0]
                self._y0 = surface_coordinates['xy0'][1]
                self._x1 = surface_coordinates['xy1'][0]
                self._y1 = surface_coordinates['xy1'][1]


if __name__ == '__main__':
    sideclass = DxfSidePolyline()

