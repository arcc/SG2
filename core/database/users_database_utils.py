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

        self.table_template.update({'user_statistics_day':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `user_name` varchar(20) NOT NULL,"
                         "  `Day_Tatol` int(20) NOT NULL,"
                         "  PRIMARY KEY (`user_ID`)"
                         ") ENGINE=InnoDB")%x,})

        self.table_template.update({'user_statistics_week':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `user_name` varchar(20) NOT NULL,"
                         "  `Week_Tatol` int(20) NOT NULL,"
                         "  PRIMARY KEY (`user_ID`)"
                         ") ENGINE=InnoDB")%x,})

        self.table_template.update({'user_statistics_year':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `user_name` varchar(20) NOT NULL,"
                         "  `Year_Tatol` int(20) NOT NULL,"
                         "  PRIMARY KEY (`user_ID`)"
                         ") ENGINE=InnoDB")%x,})

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

    def create_statistics_tables(self):
        dt_num_ele = {'user_statistics_day': (24,'h'),
                      'user_statistics_week': (7,'d'),
                      'user_statistics_year': (52,'w')}
        for key in dt_num_ele.keys():
            self.create_table(key, key)
            for ii in range(dt_num_ele[key][0]):
                 self.add_column(key, str(ii+1) + dt_num_ele[key][1] , int, 'user_name')

    def import_user_from_wp_users(self, datatable):
        condition = "user_ID>0"
        response1 = self.get_table_element(datatable, 'user_name', condition)
        usr_in = []
        for ele in response1:
            usr_in.append(ele[0])

        condition = "ID>0"
        response2 = self.get_table_element('wp_users', 'user_login', condition)
        for ele in response2:
            usr = ele[0]
            if usr in usr_in:
                continue
            else:
                self.add_row(datatable,{'user_name': usr})


    def get_user_statistics(self, datatable, user_name):
        condition = "user_name='%s'"%user_name
        response = self.get_table_row(datatable, condition)
        if response == []:
            raise ValueError("Unknown user name %s or unknown database "
                             "table %s."%(user_name, datatable))
        data = response[0]
        keys = self.get_table_keys(datatable)
        x = []
        y = []
        for ii, key in enumerate(keys):
            keyname = key[0]
            if keyname in ['user_ID','user_name']:
                continue
            if keyname.endswith(('Total','Week','Day','Year')):
                continue
            x.append(keyname)
            y.append(data[ii])
        return x, y
