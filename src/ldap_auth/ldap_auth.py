import ldap
from config import ldap_config
# Подключаемся к глобальному каталогу по LDAP
# try:

class LDAP_AUTH:
    def __init__(self):
        self.result_set = list()
        self.authorization_information = dict()

    def connect(self):
        try:
            self.lconn = ldap.initialize(f'ldap://{ldap_config.server_adres}:{ldap_config.port}')
            self.lconn.protocol_version = ldap.VERSION3
            self.lconn.set_option(ldap.OPT_REFERRALS, 0)
            self.lconn.simple_bind_s(f'{ldap_config.LOGIN}', f'{ldap_config.PASSWORD}')

            self.ldap_result_id = self.lconn.search_ext(base=ldap_config.base,
                                                        scope=ldap.SCOPE_SUBTREE,
                                                        filterstr=ldap_config.filter,
                                                        attrlist=ldap_config.attrs)

            ###блок проверки полученных данных
            try:
                while 1:
                    result_type, result_data = self.lconn.result(self.ldap_result_id, 0)
                    if (result_data == []):
                        break
                    else:
                        if result_type == ldap.RES_SEARCH_ENTRY:
                            self.result_set.append(result_data)
            except ldap.SIZELIMIT_EXCEEDED:
                print(1)
            ###

        except:
            print('Нет соединения с сервером, здесь нужно делать внутренний лог программы и подключаться к базе, '
                  'если она локально есть ')

    def give_employees_information(self):
        if self.result_set != list():
            for user_list in self.result_set:
                user = user_list[0]
                if ldap_config.attrs[0] in user[1]:
                    user_login = str(user[1][ldap_config.attrs[0]][0])[2:-1]
                    user_full_fio = str(user[0].split(',')[0])[3:]
                    if user_login != None and user_full_fio != None:
                        if ' ' in user_full_fio:
                            user_second_name = user_full_fio.split(' ')[0]
                            user_first_name = user_full_fio.split(' ')[1]
                            user_third_name = ''
                            if len(user_full_fio.split(' ')) == 3:
                                user_third_name = user_full_fio.split(' ')[2]

                            if user_third_name != '':
                                self.authorization_information[user_login] = \
                                    user_second_name + ' ' + user_first_name[0] + '.' + user_third_name[0] + '.'
                            else:
                                self.authorization_information[user_login] = \
                                    user_second_name + ' ' + user_first_name[0] + '.'


if __name__ == '__main__':
    auth = LDAP_AUTH()
    auth.connect()
    auth.give_employees_information()
    print(auth.authorization_information)


