import os

from smb.SMBConnection import SMBConnection
import ezdxf
import tempfile
import time
import socket
from config import smb_config


class SMBCONNECT_SPECMASH_SERVER:

    def __init__(self):
        self.userID = smb_config.USERLOGIN#const
        self.password = smb_config.PASSWORD#const

        self.client_machine_name = socket.gethostname()#имя компа в сети
        self.client_ip_addres = socket.gethostbyname(self.client_machine_name)#айпи адрес компа
        if self.client_ip_addres.split('.')[2] == '200':
            self.remote_machine_name = smb_config.REMOTE_MACHINE_NAME_AVTOVO
            self.server_ip = smb_config.SERVER_IP_AVTOVO #сервер тот что в спб
        elif self.client_ip_addres.split('.')[2] == '31':
            self.remote_machine_name = smb_config.REMOTE_MACHINE_NAME_KIROVSKIY
            self.server_ip = smb_config.SERVER_IP_KIROVSKIY #сервер тот что в спб

    def install_connect(self):
        if os.getlogin() not in smb_config.LOGIN_EXCEPTION:
            self.conn = SMBConnection(username=self.userID,
                                      password=self.password,
                                      my_name=self.client_machine_name,
                                      remote_name=self.remote_machine_name,
                                      domain=smb_config.DOMAIN,
                                      use_ntlm_v2 = True)

            self.connection_status = self.conn.connect(self.server_ip, smb_config.PORT)#True or False

    def get_shell_csv_path(self):
        if os.getlogin() not in smb_config.LOGIN_EXCEPTION:
            if self.connection_status:#Если установлена коннект с сервером
                self.file_obj_SHELL_CSV = tempfile.NamedTemporaryFile(delete=False)
                self.shell_csv_path = self.file_obj_SHELL_CSV.name
                filelist = self.conn.listShares(timeout=30)

                file_attributes, filesize = self.conn.retrieveFile\
                    ('Docs',
                     smb_config.SHELL_BASE_PATH[self.remote_machine_name],
                     self.file_obj_SHELL_CSV)
                self.file_obj_SHELL_CSV.close()
        else:
            self.shell_csv_path = 'backlog_bd\\shell.csv'

    def get_gland_csv_path(self):
        if os.getlogin() not in smb_config.LOGIN_EXCEPTION:
            if self.connection_status:#Если установлена коннект с сервером
                self.file_obj_GLAND_CSV = tempfile.NamedTemporaryFile(delete=False)
                self.gland_csv_path = self.file_obj_GLAND_CSV.name
                filelist = self.conn.listShares(timeout=30)

                file_attributes, filesize = self.conn.retrieveFile\
                    ('Docs',
                     smb_config.GLAND_BASE_PATH[self.remote_machine_name],
                     self.file_obj_GLAND_CSV)
                self.file_obj_GLAND_CSV.close()
        else:
            self.gland_csv_path = 'backlog_bd\\Кабельные вводы ВЗОР(САПР).csv'

    def get_base_dxf_path(self):
        if os.getlogin() not in smb_config.LOGIN_EXCEPTION:
            if self.connection_status:#Если установлена коннект с сервером
                self.file_obj_BASE_DXF = tempfile.NamedTemporaryFile(delete=False)
                self.dxf_base_path = self.file_obj_BASE_DXF.name
                filelist = self.conn.listShares(timeout=30)
                file_attributes, filesize = self.conn.retrieveFile\
                    ('Docs',
                     smb_config.DXF_BASE_PATH[self.remote_machine_name],
                     self.file_obj_BASE_DXF)
                self.file_obj_BASE_DXF.close()
        else:
            self.dxf_base_path = 'backlog_bd\\DXF_BASE.dxf'

    def get_base_pricexlsx_path(self):
        if os.getlogin() not in smb_config.LOGIN_EXCEPTION:
            if self.connection_status:  # Если установлена коннект с сервером
                self.file_obj_PRICE_XLSX = tempfile.NamedTemporaryFile(suffix=".xlsx",delete=False)
                self.price_xlsx_path = self.file_obj_PRICE_XLSX.name
                filelist = self.conn.listShares(timeout=30)
                file_attributes, filesize = self.conn.retrieveFile \
                    ('Docs',
                     smb_config.PRICE_BASE_PATH[self.remote_machine_name],
                     self.file_obj_PRICE_XLSX)
                self.file_obj_PRICE_XLSX.close()
        else:
            self.price_xlsx_path = 'backlog_bd\\price.xlsx'

    def save_log(self,logger_path):
        # self.install_connect()
        if os.getlogin() not in smb_config.LOGIN_EXCEPTION:
            if self.connection_status:
                with open(logger_path, 'rb') as f:
                    self.conn.storeFile('Docs',
                                        smb_config.LOGGER_BASE_PATH[self.remote_machine_name] + f'{os.getlogin()}_{time.time()}.txt',
                                         f)
        else:
            with open(logger_path, 'r') as fr,open(f'{os.getlogin()}_{time.time()}.txt','w') as fw:
                for line in fr:
                    fw.write(line)

