import os

from smb.SMBConnection import SMBConnection
import ezdxf
import tempfile
import time
class SMBCONNECT_SPECMASH_SERVER:
    def __init__(self):
        self.userID = "g.zubkov"
        self.password = "QWErty!!11"
        self.client_machine_name = "SM_PC_21"
        self.remote_machine_name = "fs_spb"
        self.server_ip = "192.168.100.45"


    def install_connect(self):
        self.conn = SMBConnection(username=self.userID,
                                  password=self.password,
                                  my_name=self.client_machine_name,
                                  remote_name=self.remote_machine_name,
                                  domain='ZAVOD.RU',
                                  use_ntlm_v2 = True)
        self.connection_status = self.conn.connect(self.server_ip, 139)#True or False

    def get_auth_path(self):
        if self.connection_status:#Если установлена коннект с сервером
            self.file_obj = tempfile.NamedTemporaryFile(delete=False)
            self.authentication_path = self.file_obj.name
            filelist = self.conn.listShares(timeout=30)

            file_attributes, filesize = self.conn.retrieveFile\
                ('Docs',
                 'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\authentication\\database.xlsx',
                  self.file_obj)
            self.file_obj.close()

    def get_doc_path(self):
        self.file_obj = tempfile.NamedTemporaryFile(delete=False)
        # self.install_connect()
        self.path = self.file_obj.name
        filelist = self.conn.listShares(timeout=30)
        file_attributes, filesize = self.conn.retrieveFile('Docs',
                                                           'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\САПР\\dxf_base\\DXF_BASE.dxf',
                                                            self.file_obj)
        self.file_obj.close()

    def save_log(self,logger_path):
        # self.install_connect()
        with open(logger_path, 'rb') as f:
            self.conn.storeFile('Docs',
                                f'КД\\ВЗОР\\03 КД\\10 Светильники\\0. База КОМПАС\\3D модели\_Документация\\36. Библиотеки для ПО\\Скрипты Python\\Объединение Excel\\{os.getlogin()}_{time.time()}.txt',
                                 f)
