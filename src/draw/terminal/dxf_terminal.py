from src.draw.base import DxfBase
from ezdxf.document import Drawing

def define_len_terminals(list_terminal_dxf):
    sum_len = sum([terminal_dxf.horizontal_length for terminal_dxf in list_terminal_dxf])
    return sum_len


class TerminalDxf(DxfBase):

    def set_doc_base(self, doc_base: Drawing):
        '''
        Установка doc
        :param doc: doc_base общая dxf база
        :return:
        '''
        self.doc_base = doc_base

    def set_terminal_dxf_name(self,terminal_dxf_name):
        self.terminal_dxf_name = terminal_dxf_name

    def set_terminal_block_from_dxf_base(self):
        '''Получение блока shell name_topside'''
        self.get_block(block_name=self.terminal_dxf_name)

    def calculate_horizontal_length(self):
        self.set_terminal_block_from_dxf_base()
        self.define_extreme_lines()
        self.horizontal_length = self.extreme_lines['x_max'] - self.extreme_lines['x_min']



