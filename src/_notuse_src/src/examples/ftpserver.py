from ezdxf import recover
from ezdxf.addons.drawing import matplotlib
import ezdxf
import copy
import transliterate
# Exception handling left out for compactness
# doc = ezdxf.readfile('1._1.dxf')
# doc_new = copy.copy(doc)
# doc_doc_doc, auditor = recover.readfile('1._1.dxf')
# if not auditor.has_errors:
#     matplotlib.qsave(doc_doc_doc.modelspace(), '1._1.dxf.png')

a = 'ВЗ-Н12-Т1/2G(В)'

print(transliterate.translit(a, language_code='ru', reversed=True))

