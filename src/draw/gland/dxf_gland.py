from src.draw.base import DxfBase
from src.csv.gland_csv import CableGlandInformation
class GlandDxfCircle(DxfBase):

    def set_gland_csv_information(self,gland_csv_information:CableGlandInformation):
        self.gland_csv = gland_csv_information


    def set_gland_dxf_block(self,block):
        self.block = block

    def calculate_length(self):
        self.define_extreme_lines()
        self.gland_length_dxf = self.extreme_lines['y_max'] - self.extreme_lines['y_min']


    # def y_insert_coordinate_on_topside(self,topside_extreme_lines):












    def set_gland_name(self):
        pass

