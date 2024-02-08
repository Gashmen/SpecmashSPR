class CableGlandCsv:

    def __init__(self):
        self._series = None
        self._type_thread = None
        self._measure_thread = None
        self._additional_marking = None
        self._thread_pitch = None
        self._name_type_thread = None
        self._diametr_min = None
        self._diametr_max = None
        self._diametr = None
        self._weight = None

    @property
    def series(self):
        return self._series

    @series.setter
    def series(self,value):
        self._series = value

    @property
    def type_thread(self):
        return self._type_thread

    @type_thread.setter
    def type_thread(self,value):
        self._type_thread = value

    @property
    def measure_thread(self):
        return self._measure_thread

    @measure_thread.setter
    def measure_thread(self,value):
        self._measure_thread = value

    @property
    def additional_marking(self):
        return self._additional_marking

    @additional_marking.setter
    def additional_marking(self,value):
        self._additional_marking = value

    @property
    def thread_pitch(self):
        return self._thread_pitch

    @thread_pitch.setter
    def thread_pitch(self,value):
        self._thread_pitch = value

    @property
    def name_type_thread(self):
        return self._name_type_thread

    @name_type_thread.setter
    def name_type_thread(self,value):
        self._name_type_thread = value

    @property
    def diametr_min(self):
        return self._diametr_min

    @diametr_min.setter
    def diametr_min(self,value):
        self._diametr_min = value

    @property
    def diametr_max(self):
        return self._diametr_max

    @diametr_min.setter
    def diametr_max(self, value):
        self._diametr_max = value

    @property
    def diametr(self):
        return self._diametr

    @diametr.setter
    def diametr(self, value):
        self._diametr = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value



