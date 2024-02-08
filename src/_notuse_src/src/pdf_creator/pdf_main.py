import sys

import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import matplotlib

import matplotlib.font_manager
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties, LayoutProperties
from ezdxf.addons.drawing.config import Configuration


def select_doc_new(path_to_dxf):
    '''Возращает просто dxf путь'''
    return path_to_dxf


def save_pdf(save_doc_path):
    path_to_dxf = save_doc_path

    try:
        doc, auditor = recover.readfile(select_doc_new(path_to_dxf=path_to_dxf))
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)

    if not auditor.has_errors:
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
            lineweight_scaling=0.1
        )
        ctx.set_current_layout(doc.modelspace())
        ctx.current_layout_properties.set_colors(bg='#FFFFFF')

        # --- Делает белый бэкграунд ---

        out = MatplotlibBackend(ax) #{"lineweight_scaling": 0.1})

        # Better control over the LayoutProperties used by the drawing frontend
        layout_properties = LayoutProperties.from_layout(doc.modelspace())
        layout_properties.set_colors(bg='#FFFFFF')

        Frontend(ctx, out, config=config).draw_layout(doc.modelspace(),layout_properties=layout_properties, finalize=True)
        path_to_pdf = path_to_dxf[:-3] + 'pdf'
        fig.savefig(path_to_pdf, format='pdf', dpi=300, facecolor='black', edgecolor='black')

if __name__ == '__main__':

    path_to_dxf = 'C:\\Users\\g.zubkov\\PycharmProjects\\Project_not_for_exe\\10._1check.dxf'
    save_pdf(path_to_dxf)

