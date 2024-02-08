from ezdxf.document import Drawing
import ezdxf

class DxfBase:

    def __init__(self,dxf_base_path):
        self.dxf_base_path = dxf_base_path

    def set_doc_dxf(self):
        if self.dxf_base_path != '':
            self.doc_base = ezdxf.readfile(self.dxf_base_path)

    def set_doc_existed(self,doc):
        self.doc_base = doc_base

    def delete_all_entities(self):
        if hasattr(self,'doc_base'):
            self.doc_base.modelspace().delete_all_entities()

    def delete_not_used_block(self,block_needed_for_draw:list):
        '''Удалить нужно только те блоки, которые не будут использоваться ВО ВСЕХ ЛИСТАХ
        Т.е. один doc будет использоваться для всех всех листов.
        ДЛЯ ГЛАВНОГО ЛИСТА, ДЛЯ ШИЛЬДА, ДЛЯ БОМА И ТД
        '''
        if hasattr(self, 'doc_base'):
            self.block_not_used = [block.dxf.name for block in self.doc_base.blocks
                                                      if block.dxf.name not in block_needed_for_draw and
                                                      '*' not in block.dxf.name]

            for block in self.block_not_used:
                try:
                    seld.doc_base.blocks.delete_block(name=block)
                except:
                    continue
            return doc_dxfbase

    def give_all_blocks(self):
        '''Получение словаря {имя блока:сам blocklayout}'''
        if hasattr(self,'doc_base'):
            self.doc_dict_blocks = {block.dxf.name:block for block in self.doc_base.blocks
                                                             if '*' not in block.dxf.name}

    def give_names_terminal(self):
        '''Получение имен всех клемм'''
        if hasattr(self, 'doc_dict_blocks'):
            self.terminal_full_names = [block_name for block_name in self.doc_dict_blocks if 'viewside' in block_name]

    def check_shell(self,shell_translite_name):
        '''Проверка возможности создания оболочки'''
        shell_block_names = ('topside','upside','downside',
                             'leftside','rightside','withoutcapside',
                             'cutside','installation_dimensions')

        possible_to_draw_shell = False
        if hasattr(self,'doc_dict_blocks'):
            for side_name in shell_block_names:
                block_name = shell_translite_name + '_' + side_name
                if block_name in self.doc_dict_blocks:
                    possible_to_draw_shell = True
                else:
                    possible_to_draw_shell = False
                    break
            if 'DIN_' + shell_translite_name in self.doc_dict_blocks:
                possible_to_draw_shell = True
            else:
                False
        return possible_to_draw_shell

    def check_gland(self,gland_translite_name):
        '''Проверка возможности создания кабельного ввода'''
        gland_blocks_names = ('exe','exd','topside','upside',
                              'downside','leftside','rightside',
                              'withoutcapside','cutside')
        possible_to_draw_gland = False
        if hasattr(self,'doc_dict_blocks'):
            for gland_name in gland_blocks_names:
                block_name = gland_translite_name + '_' + gland_name
                if block_name in self.doc_dict_blocks:
                    possible_to_draw_gland = True
                else:
                    possible_to_draw_gland = False
                    break
        return possible_to_draw_gland

    def get_block(self,block_name):
        try:
            self.block = self.doc_base.blocks[block_name]
        except:
            raise BaseException(f'Нет данного блока в self.doc.blocks {self.doc_base}')

    def define_extreme_lines(self):
        '''Поиск координат крайних точек по линиям в блоке
        :block: Блок из doc.blocks
        :return:  {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}
        '''
        x = list()
        y = list()
        if hasattr(self,'block'):
            for line in self.block:
                if line.dxftype() == 'LINE':
                    x.append(line.dxf.start[0])
                    x.append(line.dxf.end[0])
                    y.append(line.dxf.start[1])
                    y.append(line.dxf.end[1])
            if x and y:  # если есть коробка
                self.extreme_lines =  {'x_max': max(x), 'y_max': max(y), 'x_min': min(x), 'y_min': min(y)}
        else:
            print('base.BaseDxfBlock.define_extreme_lines')


class GeneralInformationBaseDxf:

    def __init__(self,doc:Drawing):
        self.set_doc(doc=doc)

    def set_doc(self,doc):
        '''Устанавливаем один раз doc, для сокращения времени обращения'''
        if isinstance(doc, Drawing):
            self.doc = doc


class BaseDxfBlock:

    def __init__(self,doc:Drawing):

        self.block_name = None

        if isinstance(doc,Drawing):
            self.doc = doc

    def define_block_parametrs(self,block_name):
        self.set_block_dxf_name(block_name=block_name)
        if hasattr(self,'block_name'):
            self.get_block()
            self.define_extreme_lines()


    def set_block_dxf_name(self,block_name):
        if isinstance(block_name,str):
            self.block_name = block_name
        else:
            raise ValueError('BlockName задан не текстом в блоке BaseDxfBlock')

    def get_block(self):
        try:
            self.block = self.doc.blocks[self.block_name]
        except:
            raise BaseException(f'Нет данного блока в self.doc.blocks {self.doc}')

    def define_extreme_lines(self):
        '''Поиск координат крайних точек по линиям в блоке
        :block: Блок из doc.blocks
        :return:  {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}
        '''
        x = list()
        y = list()
        if hasattr(self,'block'):
            for line in self.block:
                if line.dxftype() == 'LINE':
                    x.append(line.dxf.start[0])
                    x.append(line.dxf.end[0])
                    y.append(line.dxf.start[1])
                    y.append(line.dxf.end[1])
            if x and y:  # если есть коробка
                self.extreme_lines =  {'x_max': max(x), 'y_max': max(y), 'x_min': min(x), 'y_min': min(y)}
        else:
            print('base.BaseDxfBlock.define_extreme_lines')










