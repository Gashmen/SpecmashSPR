from smb.SMBConnection import SMBConnection
import json
import urllib.request
import tempfile
from io import StringIO
import ezdxf
import logging


if __name__ == '__main__':
    # with open(f'smb://192.168.10.244\\all\\exchange_Petersburg\\current_stock.JSON',"at", encoding="utf-8") as fcc_file:
    #     fcc_data = json.load(fcc_file)
    #     print(fcc_data)
    # destination = 'название файла'
    # url = '192.168.10.244\\all\\exchange_Petersburg\\current_stock.JSON'
    # urllib.request.urlretrieve(url, destination)


    userID = "g.zubkov"
    password = "QWErty!!11"
    client_machine_name = "SM_PC_21"
    remote_machine_name = "fs_spb"
    server_ip = "192.168.100.45"
    conn = SMBConnection(username=userID,
                         password=password,
                         my_name=client_machine_name,
                         remote_name=remote_machine_name,
                         domain='ZAVOD.RU',
                         use_ntlm_v2 = True)

    conn.connect(server_ip, 139)

#Каменск 192.168.10.244
#СПБ 192.168.100.45
#\\192.168.100.45\Docs\КД\ВЗОР\03 КД\10 Светильники\0. База КОМПАС\3D модели\_Документация\36. Библиотеки для ПО\Скрипты Python
file_obj = tempfile.NamedTemporaryFile(delete=False)#СОЗДАЕТ ФАЙЛ ВО ВРЕМЕННОЙ ПАПКЕ
path = file_obj.name
filelist = conn.listShares(timeout=30)
file_attributes, filesize = conn.retrieveFile('Docs', 'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\dxf_base\\DXF_BASE.dxf', file_obj)
file_obj.close()


# fffile = StringIO('1234')
doc = ezdxf.readfile(path)#ЧТЕНИЕ ФАЙЛА С СЕРВЕРА
print(doc)
#Сначала записываем в файл, а потом читаем его и как бы копируем на сервер
# print(path)
# with open(path,'rb') as f:
#     f.save

# general_dxf_string = ''
# with open(path,'rb') as f:
#     for i in f.readlines():
#         general_dxf_string += i
# print(general_dxf_string)
# doc = ezdxf.readfile(general_dxf_string,encoding="utf-8")
# print(doc)

    #
    # for i in f.readlines():
    #     print(i.decode())
    # print(f.readlines())
logger_file_obj = tempfile.NamedTemporaryFile(delete=False)
logger_path = logger_file_obj.name


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file = logging.FileHandler(filename=logger_path)
logger_file.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(name)s %(message)s'))
logger.addHandler(logger_file)
logger.debug('debug information')
logger.info('info')
logger_file_obj.close()

with open(logger_path,'rb') as f:
    conn.storeFile('Docs',
                   'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\Объединение Excel\\log1.txt',
                   f)
    # file_obj.write(b'123456')
    #Запись файла DOCS это service name, далее под каким именнем сохраняем условно, но надо также дать фул путь, далее объект который записываем

# with open('C:\\Users\\g.zubkov\\PycharmProjects\\Project_not_for_exe\\14._3.dxf','rb') as file_obj:
#     conn.storeFile('Docs','КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\Объединение Excel\\log1.dxf',file_obj)

