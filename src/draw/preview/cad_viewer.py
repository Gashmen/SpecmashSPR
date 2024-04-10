import signal
from typing import Optional

import ezdxf
from ezdxf.addons.drawing.qtviewer import CADGraphicsViewWithOverlay, CADWidget, CADViewer
from ezdxf.addons.xqt import QtCore as qc, QtGui as qg, QtWidgets as qw
from ezdxf.audit import Auditor
from ezdxf.document import Drawing
from ezdxf.entities import DXFGraphic


class ElementSelectorView(CADGraphicsViewWithOverlay):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = None

    def keyPressEvent(self, event: qg.QKeyEvent) -> None:
        if event.key() == qc.Qt.Key_Return:
            element = self.current_hovered_element
            if element is not None:
                self.selected = element
                self.close()


def select_element(doc: Drawing, layout: str = 'Model', show_controls: bool = False) -> Optional[DXFGraphic]:
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # handle Ctrl+C properly
    app = qw.QApplication.instance()
    if app is None:
        app = qw.QApplication([])

    view = ElementSelectorView()
    cad = CADWidget(view)
    if show_controls:
        viewer = CADViewer(cad=cad)
        view.closing.connect(viewer.close)
        viewer.set_document(doc, Auditor(doc), layout=layout)
        viewer.show()
    else:
        cad.set_document(doc, layout=layout)
        cad.show()
    app.exec()
    return view.selected

def preview_mode(doc):

    select_element(doc, show_controls=True)

# if __name__ == '__main__':
#     main()

