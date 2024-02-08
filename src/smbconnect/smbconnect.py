import os

from smb.SMBConnection import SMBConnection
import ezdxf
import tempfile
import time
import socket
from config import smb_config


class SMBCONNECT_SPECMASH_SERVER:

    def __init__(self):
        self.userID = smb_config.USERLOGIN
        self.password = smb_config.PASSWORD
        self.client_machine_name = socket.gethostname()
        self.remote_machine_name = smb_config.REMOTE_MACHINE_NAME
        self.server_ip = smb_config.SERVER_IP

    def install_connect(self):
        self.conn = SMBConnection(username=self.userID,
                                  password=self.password,
                                  my_name=self.client_machine_name,
                                  remote_name=self.remote_machine_name,
                                  domain=smb_config.DOMAIN,
                                  use_ntlm_v2 = True)

        self.connection_status = self.conn.connect(self.server_ip, smb_config.PORT)#True or False

    def get_shell_csv_path(self):
        if self.connection_status:#Если установлена коннект с сервером
            self.file_obj_SHELL_CSV = tempfile.NamedTemporaryFile(delete=False)
            self.shell_csv_path = self.file_obj_SHELL_CSV.name
            filelist = self.conn.listShares(timeout=30)

            file_attributes, filesize = self.conn.retrieveFile\
                ('Docs',smb_config.SHELL_BASE_PATH,self.file_obj_SHELL_CSV)
            self.file_obj_SHELL_CSV.close()

    def get_gland_csv_path(self):
        if self.connection_status:#Если установлена коннект с сервером
            self.file_obj_GLAND_CSV = tempfile.NamedTemporaryFile(delete=False)
            self.gland_csv_path = self.file_obj_GLAND_CSV.name
            filelist = self.conn.listShares(timeout=30)

            file_attributes, filesize = self.conn.retrieveFile\
                ('Docs',smb_config.GLAND_BASE_PATH,self.file_obj_GLAND_CSV)
            self.file_obj_GLAND_CSV.close()

    def get_base_dxf_path(self):
        if self.connection_status:#Если установлена коннект с сервером
            self.file_obj_BASE_DXF = tempfile.NamedTemporaryFile(delete=False)
            self.dxf_base_path = self.file_obj_BASE_DXF.name
            filelist = self.conn.listShares(timeout=30)

            file_attributes, filesize = self.conn.retrieveFile\
                ('Docs',smb_config.DXF_BASE_PATH,self.file_obj_BASE_DXF)
            self.file_obj_BASE_DXF.close()


