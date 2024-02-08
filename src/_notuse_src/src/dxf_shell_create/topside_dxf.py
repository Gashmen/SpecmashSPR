class SideInsert:
    def __init__(self,
                 extreme_lines_all_blocks = None,
                 block_name = None,
                 doc = None,
                 angle_for_add = None):
        self.doc = doc
        self.insert_name = block_name
        self.extreme_lines_all_blocks = extreme_lines_all_blocks
        self.insert_angle = angle_for_add

        '''считаем за длину это размеры xmax - xmin
           считаем за ширину размеры ymax - ymin
        '''

    def search_length_widht(self):
        if self.insert_angle is not None:
            if self.insert_angle == 0 or self.insert_angle == 180:
                self.length = self.extreme_lines_all_blocks[self.insert_name]['x_max']-\
                              self.extreme_lines_all_blocks[self.insert_name]['x_min']
                self.width = self.extreme_lines_all_blocks[self.insert_name]['y_max']-\
                              self.extreme_lines_all_blocks[self.insert_name]['y_min']
            elif self.insert_angle == 90 or self.insert_angle == 270:
                self.length = self.extreme_lines_all_blocks[self.insert_name]['y_max'] - \
                              self.extreme_lines_all_blocks[self.insert_name]['y_min']
                self.width = self.extreme_lines_all_blocks[self.insert_name]['x_max'] - \
                             self.extreme_lines_all_blocks[self.insert_name]['x_min']



    # def search_insert_coordinate_first_iteration(self):
    #     if self.doc.blocks.get(insert_name):
    #         if self.insert_name.endswith('_topside'):
    #             self.insert_coordinate = (0, 0)
    #         elif self.insert_name.endswith('_downside'):








    # def define_extreme_lines_current_insert(self):



