import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import matplotlib

import matplotlib.font_manager
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties, LayoutProperties
from ezdxf.addons.drawing.config import Configuration
import ezdxf
import time
from ezdxf.addons import Importer

import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from src.interface_backend import dxf_shell_ui #ПОМЕНЯТЬ НА ИТОГОВЫЙ ИНТЕРФЕЙСНЫЙ МОДУЛЬ В ОЧЕРЕДНОСТИ
from src.draw.gland import dxf_gland


class DxfGlandQtCommunication(dxf_shell_ui.DxfShellQtCommunication):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        self.addButton_2.clicked.connect(self.setup_glands)

    @Qt.pyqtSlot()
    def setup_glands(self):
        self.set_dict_dxf_glands()
        self.calculate_max_length_glands()
        self.calculate_scale()
        self.draw_glands_in_sides()
        self.draw_shells_inserts()

    def set_dict_dxf_glands(self):
        self.glands_on_sides_dxf_dict = {"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        if hasattr(self.upside_block,'two_row_calculate') or\
                hasattr(self.rightside_block,'two_row_calculate') or\
                hasattr(self.leftside_block,'two_row_calculate') or\
                hasattr(self.downside_block,'two_row_calculate') or \
                hasattr(self.topside_block, 'two_row_calculate'):
            for side_rus_name in self.glands_on_sides_dict:
                self.glands_on_sides_dxf_dict[side_rus_name] = list()
                for gland_csv_current in self.glands_on_sides_dict[side_rus_name]:
                    gland_dxf = dxf_gland.GlandDxfCircle()
                    gland_dxf.set_gland_csv_information(gland_csv_information=gland_csv_current)
                    gland_block = self.base_dxf.doc_base.blocks[gland_csv_current.gland_dxf_name + '_' + gland_csv_current.side]
                    gland_dxf.set_gland_dxf_block(block=gland_block)
                    gland_dxf.calculate_length()
                    self.glands_on_sides_dxf_dict[side_rus_name].append(gland_dxf)

    def calculate_max_length_glands(self):
        if hasattr(self,'glands_on_sides_dxf_dict'):

            self.scale_class.calculate_len0_x(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len2_x(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len4_x(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len6_x()
            self.scale_class.calculate_len8_x()
            self.scale_class.calculate_len9_x()
            self.scale_class.calculate_len11_x()

            self.scale_class.calculate_len0_y()
            self.scale_class.calculate_len2_y(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len4_y(glands_on_sides_dxf_dict=self.glands_on_sides_dxf_dict)
            self.scale_class.calculate_len6_y()
        else:
            self.scale_class.set_zero_len_without_glands()

    def calculate_scale(self):
        if hasattr(self,'scale_class'):
            if hasattr(self,'shell_dict'):
                self.scale_class.calculate_scale()

    def topside_draw_glands(self):
        if hasattr(self, 'topside_block'):
            self.topside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            self.topside_block.draw_topside_exe_glands()
            if hasattr(self, 'rightside_block'):
                self.topside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines,
                                                         added_gland_dxf_name='_topside')
            if hasattr(self, 'leftside_block'):
                self.topside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines,
                                                         added_gland_dxf_name='_topside')
            if hasattr(self,'upside_block'):
                self.topside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines,
                                                         added_gland_dxf_name='_topside')
            if hasattr(self,'downside_block'):
                self.topside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines,
                                                         added_gland_dxf_name='_topside')
    def upside_draw_glands(self):
        if hasattr(self,'upside_block'):
            self.upside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            # self.rightside_block.draw_glands_in_block()
            self.upside_block.draw_upside_exe_glands()
            if hasattr(self,'rightside_block'):
                self.upside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self,'leftside_block'):
                self.upside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.upside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def downside_draw_glands(self):
        if hasattr(self,'downside_block'):
            self.downside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            # self.rightside_block.draw_glands_in_block()
            self.downside_block.draw_downside_exe_glands()
            if hasattr(self,'rightside_block'):
                self.downside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self,'leftside_block'):
                self.downside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.downside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def rightside_draw_glands(self):
        if hasattr(self,'rightside_block'):
            self.rightside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            # self.rightside_block.draw_glands_in_block()
            self.rightside_block.draw_rightside_exe_glands()
            if hasattr(self,'upside_block'):
                self.rightside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self,'downside_block'):
                self.rightside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
            if hasattr(self,'topside_block'):
                self.rightside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def leftside_draw_glands(self):
        if hasattr(self, 'leftside_block'):
            self.leftside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            # self.rightside_block.draw_glands_in_block()
            self.leftside_block.draw_leftside_exe_glands()
            if hasattr(self, 'upside_block'):
                self.leftside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self, 'downside_block'):
                self.leftside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.leftside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def cutside_draw_glands(self):
        if hasattr(self, 'cutside_block'):
            self.cutside_block.set_dict_glands_all_sizes(glands_on_sides_dict=self.glands_on_sides_dict)
            if hasattr(self, 'upside_block'):
                self.cutside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self, 'downside_block'):
                self.cutside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)
            if hasattr(self, 'topside_block'):
                self.cutside_block.draw_topside_glands(topside_extreme_lines=self.topside_block.extreme_lines)

    def withoutcapside_din(self):
        if hasattr(self, 'withoutcapside_block'):
            self.withoutcapside_block.draw_din()

    def withoutcapside_draw_glands(self):
        if hasattr(self,'withoutcapside_block'):

            self.withoutcapside_block.set_dict_glands_all_sizes(self.glands_on_sides_dict)
            # self.withoutcapside_block.set_dict_glands_all_sizes(glands_on_sides_dict=self.glands_on_sides_dict)
            if hasattr(self, 'rightside_block'):
                self.withoutcapside_block.draw_rightside_glands(rightside_extreme_lines=self.rightside_block.extreme_lines)
            if hasattr(self, 'leftside_block'):
                self.withoutcapside_block.draw_leftside_glands(leftside_extreme_lines=self.leftside_block.extreme_lines)
            if hasattr(self,'upside_block'):
                self.withoutcapside_block.draw_upside_glands(upside_extreme_lines=self.upside_block.extreme_lines)
            if hasattr(self,'downside_block'):
                self.withoutcapside_block.draw_downside_glands(downside_extreme_lines=self.downside_block.extreme_lines)

    def draw_glands_in_sides(self):
        self.topside_draw_glands()
        self.upside_draw_glands()
        self.downside_draw_glands()
        self.leftside_draw_glands()
        self.cutside_draw_glands()
        self.rightside_draw_glands()
        self.withoutcapside_draw_glands()


    def save_doc(self):#тест, потом удалить
        time2 = time.time()
        # self.base_dxf.doc_base=
        self.base_dxf.doc_for_save.saveas('check.dxf')
        print('Сохранение dxf: ',time.time()-time2)

    def save_pdf(self):

        time2 = time.time()

        # try:
        #     doc, auditor = recover.readfile('check.dxf')
        # except IOError:
        #     print(f'Not a DXF file or a generic I/O error.')
        #     sys.exit(1)
        # except ezdxf.DXFStructureError:
        #     print(f'Invalid or corrupted DXF file.')
        #     sys.exit(2)
        # # doc.save()
        # if not auditor.has_errors:
        #
        #     try:
        doc = self.base_dxf.doc_base
        # matplotlib.qsave(doc.modelspace(), 'your.png',bg='#FFFFFFFF',size_inches=(800,600))
        ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = '#FFFFFF'
        # prop = matplotlib.font_manager.FontProperties(family='GOST_A')
        # matplotlib.font_manager.findfont(prop, fontext='ttf')
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        # --- Делает белый бэкграунд ---
        config = Configuration()
        config = config.with_changes(
            min_lineweight=0.05,  # in 1/300 inch: 1 mm = 1mm / 25.4 * 300
            lineweight_scaling=0.1,
        )

        ctx.set_current_layout(doc.modelspace())
        ctx.current_layout_properties.set_colors(bg='#FFFFFF')

        # --- Делает белый бэкграунд ---

        out = MatplotlibBackend(ax)  # {"lineweight_scaling": 0.1})

        # Better control over the LayoutProperties used by the drawing frontend
        layout_properties = LayoutProperties.from_layout(doc.modelspace())
        layout_properties.set_colors(bg='#FFFFFF')

        Frontend(ctx, out, config=config).draw_layout(doc.modelspace(), layout_properties=layout_properties,
                                                      finalize=True)
        path_to_pdf = 'check.' + 'pdf'
        fig.savefig(path_to_pdf, format='pdf', dpi=300, facecolor='black', edgecolor='black')

        print('Сохранение pdf: ',time.time()-time2)

    def save_pdf_BOM(self,page_number):

        time2 = time.time()

        # try:
        #     doc, auditor = recover.readfile('check.dxf')
        # except IOError:
        #     print(f'Not a DXF file or a generic I/O error.')
        #     sys.exit(1)
        # except ezdxf.DXFStructureError:
        #     print(f'Invalid or corrupted DXF file.')
        #     sys.exit(2)
        # # doc.save()
        # if not auditor.has_errors:
        #
        #     try:
        doc = self.base_dxf.doc_for_save
        # matplotlib.qsave(doc.modelspace(), 'your.png',bg='#FFFFFFFF',size_inches=(800,600))
        ezdxf.addons.drawing.properties.MODEL_SPACE_BG_COLOR = '#FFFFFF'
        # prop = matplotlib.font_manager.FontProperties(family='GOST_A')
        # matplotlib.font_manager.findfont(prop, fontext='ttf')
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        # --- Делает белый бэкграунд ---
        config = Configuration()
        config = config.with_changes(
            min_lineweight=0.05,  # in 1/300 inch: 1 mm = 1mm / 25.4 * 300
            lineweight_scaling=0.1,
        )

        ctx.set_current_layout(doc.modelspace())
        ctx.current_layout_properties.set_colors(bg='#FFFFFF')

        # --- Делает белый бэкграунд ---

        out = MatplotlibBackend(ax)  # {"lineweight_scaling": 0.1})

        # Better control over the LayoutProperties used by the drawing frontend
        layout_properties = LayoutProperties.from_layout(doc.modelspace())
        layout_properties.set_colors(bg='#FFFFFF')

        Frontend(ctx, out, config=config).draw_layout(doc.modelspace(), layout_properties=layout_properties,
                                                      finalize=True)
        path_to_pdf = 'BOM_' + str(page_number) + '.pdf'
        fig.savefig(path_to_pdf, format='pdf', dpi=300, facecolor='black', edgecolor='black')

        print('Сохранение BOM: ',time.time()-time2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfGlandQtCommunication()
    welcome_window.show()
    sys.exit(app.exec_())





