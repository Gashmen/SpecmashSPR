USERLOGIN = "SpecmashSPR"
PASSWORD = "N3m!kg^dcZ6TE7"

REMOTE_MACHINE_NAME_AVTOVO = "192.168.100.45"
SERVER_IP_AVTOVO = "192.168.100.45"

REMOTE_MACHINE_NAME_KIROVSKIY = "192.168.31.100"
SERVER_IP_KIROVSKIY = "192.168.31.100"

PORT = 139
DOMAIN='ZAVOD.RU'


LOGIN_EXCEPTION = ('Gashmen')
# LOGIN_EXCEPTION = ('Gashmen', 'i.shcherbakov','g.zubkov')
# LOGIN_EXCEPTION = ('Gashmen', 'i.shcherbakov','k.porohin','p.mogilev','a.pechenevskiy','i.maymistov')
SHELL_BASE_PATH = {REMOTE_MACHINE_NAME_AVTOVO:'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\Оболочки\\shell.csv',

                   REMOTE_MACHINE_NAME_KIROVSKIY:'Обмен\\SpecmashSpr\\shell_base\\shell.csv'}

GLAND_BASE_PATH = {REMOTE_MACHINE_NAME_AVTOVO:'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\34. Разработки\\Номенклатура кабельных вводов\\Кабельные вводы ВЗОР(САПР).csv',

                   REMOTE_MACHINE_NAME_KIROVSKIY:'Обмен\\SpecmashSpr\\gland_base\\Кабельные вводы ВЗОР(САПР).csv'}

DXF_BASE_PATH = {REMOTE_MACHINE_NAME_AVTOVO:'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\dxf_base\\DXF_BASE.dxf',

                 REMOTE_MACHINE_NAME_KIROVSKIY:'Обмен\\SpecmashSpr\\dxf_base\\DXF_BASE.dxf'}

PRICE_BASE_PATH = {REMOTE_MACHINE_NAME_AVTOVO:'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\Цены\\price.xlsx',

                   REMOTE_MACHINE_NAME_KIROVSKIY:'Обмен\\SpecmashSpr\\price_base\\price.xlsx'}

LOGGER_BASE_PATH = {REMOTE_MACHINE_NAME_AVTOVO:'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\Logs\\',

                    REMOTE_MACHINE_NAME_KIROVSKIY:'Обмен\\SpecmashSpr\\logs\\'}