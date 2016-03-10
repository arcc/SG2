import mysql.connector
from mysql.connector import errorcode
from .database_utils import DataBase
import os.path


class users_database(DataBase): # API to interact with database
    def __init__(self, local=True, user='root', password='****', host='localhost',
                 port='8889', database='wordpress',
                 unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock'):
        if local:
            super(users_database, self).__init__(password=password,
                                                 database=database)
        else:
            super(users_database, self).__init__(local=loacl, user=user,
                                                 password=password, host=host,
                                                 port=port, database=database,
                                                 unix_socket=unix_socket)

    def get_user(self, datatable, user_name):
        condition = "user_login='%s'"%user_name
        response  = self.get_table_row(datatable, condition)
        if response == []:
            raise ValueError("Unknown user name %s or unknown database "
                             "table %s."%(user_name, datatable))
        response = response[0]
        result = {'user_index': response[0], 'user_login': response[1],
                  'user_email': response[4], 'user_url': response[5],
                  'user_registered_time': response[6],
                  'user_status': response[8], 'display_name': response[9],
                  'last_index': response[10]}
        return result
