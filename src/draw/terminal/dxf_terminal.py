from ezdxf.document import Drawing

from src.draw.base import DxfBase
from config import terminal_config


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

    def set_BOM_name(self):
        if hasattr(self,'terminal_dxf_name'):
            split_full_name = self.terminal_dxf_name.split('_')
            #SUPU#VZOR
            manufacturer = split_full_name[0]
            #SPRING#SCREW
            type = split_full_name[1]
            #WHITE#BLUE#GREEN
            color = split_full_name[2]
            #1.5#2.5#4#6#10#16#35#50#70#95
            size = split_full_name[3]

            article_name = ''
            bom_name = ''
            if manufacturer == 'SUPU':
                article_name += 'T'
                bom_name += 'Клемма'

                if str(color).lower() == 'white':
                    bom_name += ' проходная'
                elif str(color).lower() == 'blue':
                    bom_name += ' нулевая'
                else:
                    bom_name += ' заземления'

                if type == 'SCREW':
                    article_name += 'U'
                    bom_name += ' винтовая'
                else:
                    article_name += 'C'
                    bom_name += ' пружинная'

                if size in terminal_config.SQUARE_CURRENT:
                    bom_name +=f' #Iном. ={terminal_config.SQUARE_CURRENT[size]}А, {size} мм.кв, {manufacturer}'
                    article_name +=size

                if str(color).lower() == 'white':
                    article_name += '-2-GY'
                elif str(color).lower() == 'blue':
                    article_name += '-2-BU'
                else:
                    article_name += '-2-PE'
            elif manufacturer == 'VZOR':
                article_name += 'К'
                bom_name += 'Клемма'

                if str(color).lower() == 'white':
                    bom_name += ' проходная'
                elif str(color).lower() == 'blue':
                    bom_name += ' нулевая'
                else:
                    bom_name += ' заземления'

                if type == 'SCREW':
                    article_name += 'В-'
                    bom_name += ' винтовая'
                else:
                    article_name += 'П-'
                    bom_name += ' пружинная'

                if size in terminal_config.SQUARE_CURRENT:
                    bom_name += f' #Iном. ={terminal_config.SQUARE_CURRENT[size]}А, {size} мм.кв, ВЗОР'
                    article_name += size

            self.article_name = [article_name]
            self.bom_name = bom_name.split('#')


    def create_BOM_dict(self):
        self.bom_dict = \
            {tuple(self.bom_name):
                {
                'Формат':"А4",
                'Зона':"",
                'Поз.':"",
                'Обозначение':self.article_name,
                'Наименование':self.bom_name,
                'Кол.':'',
                'Примечание':'ВЗОР',
                'Свойство':'Прочие изделия'
                }
            }
        print(self.bom_dict)