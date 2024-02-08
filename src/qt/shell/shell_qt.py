class ShellQtInformation:

    def __init__(self):
        self._manufacture = None
        self._explosion_protection = None
        self._series = None
        self._size = None
        self._marking_explosion = None
        self._temperature_class = None
        self._temperature_minus = None
        self._temperature_plus = None

    @property
    def manufacture(self):
        return self._manufacture

    @manufacture.setter
    def manufacture(self,value):
        self._manufacture = value

    @property
    def explosion_protection(self):
        return self._explosion_protection

    @explosion_protection.setter
    def explosion_protection(self,value):
        self._explosion_protection = value

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self,value):
        self._series = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,value):
        self._size = value

    @property
    def marking_explosion(self):
        return self._marking_explosion

    @marking_explosion.setter
    def marking_explosion(self,value):
        self._marking_explosion = value

    @property
    def temperature_class(self):
        return self._temperature_class

    @temperature_class.setter
    def temperature_class(self,value):
        self._temperature_class = value

    @property
    def temperature_minus(self):
        return self._temperature_minus

    @temperature_minus.setter
    def temperature_minus(self,value):
        self._temperature_minus = value

    @property
    def temperature_plus(self):
        return self._temperature_plus

    @temperature_plus.setter
    def temperature_plus(self,value):
        self._temperature_plus = value


