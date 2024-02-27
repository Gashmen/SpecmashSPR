from src.draw.base import DxfBase
from src.csv.gland_csv import CableGlandInformation
import src.algoritms.measure_length_base as measure_length_base
class GlandDxfCircle(DxfBase):
    _gland_blocks_names = ('topside', 'upside',
                           'downside', 'leftside',
                           'rightside','withoutcapside', 'cutside')
    def set_gland_csv_information(self,gland_csv_information:CableGlandInformation):
        self.gland_csv = gland_csv_information

    def set_gland_dxf_block(self,block):
        self.block = block

    def calculate_length(self):
        self.define_extreme_lines()
        # self.gland_length_dxf = abs(self.extreme_lines['y_min'])
        self.gland_length_dxf = measure_length_base.calculate_vertical_len_block(block=self.block)





