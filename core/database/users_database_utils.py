# This is a sg2 user database utils.
# Author Jing Luo
import mysql.connector
from mysql.connector import errorcode
from .database_utils import DataBase
import datetime
import os.path
import numpy as np

class users_database(DataBase): # API to interact with database
    def __init__(self, **login_info):
        super(users_database, self).__init__(**login_info)

        self.table_template.update({'user_statistics_day':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `user_name` varchar(20) NOT NULL,"
                         "  `Day_Total` int(20) NOT NULL,"
                         "  PRIMARY KEY (`user_ID`)"
                         ") ENGINE=InnoDB")%x,})

        self.table_template.update({'user_statistics_week':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `user_name` varchar(20) NOT NULL,"
                         "  `Week_Total` int(20) NOT NULL,"
                         "  PRIMARY KEY (`user_ID`)"
                         ") ENGINE=InnoDB")%x,})

        self.table_template.update({'user_statistics_year':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `user_name` varchar(20) NOT NULL,"
                         "  `Year_Total` int(20) NOT NULL,"
                         "  PRIMARY KEY (`user_ID`)"
                         ") ENGINE=InnoDB")%x,})
        self.table_template.update({'statistics_table_status':
                       lambda x:( "CREATE TABLE `%s` ("
                         "  `table_ID` int(11) NOT NULL AUTO_INCREMENT,"
                         "  `table_name` varchar(40) NOT NULL,"
                         "  `last_update_time` TIMESTAMP,"
                         "  PRIMARY KEY (`table_ID`)"
                         ") ENGINE=InnoDB")%x,})

        self.table_template.update({'user_last_index':
                        lambda x:( "CREATE TABLE `%s` ("
                          "  `user_ID` int(11) NOT NULL AUTO_INCREMENT,"
                          "  `user_name` varchar(20) NOT NULL,"
                          "  `user_last_index` int(11) NOT NULL,"
                          "  `user_last_input_time` TIMESTAMP,"
                          "  PRIMARY KEY (`user_ID`)"
                          ") ENGINE=InnoDB")%x,})

        self.statistics_type_indentifier = {'user_statistics_day': (24,'h','Day_Total'),
                                            'user_statistics_week': (7,'d','Week_Total'),
                                            'user_statistics_year': (52,'w','Year_Total')}

    def get_user(self, datatable, user_name):
        condition = "user_login='%s'"%user_name
        response  = self.get_table_row(datatable, condition)
        if response == []:
            return response
        response = response[0]
        result = {'user_index': response[0], 'user_login': response[1],
                  'user_email': response[4], 'user_url': response[5],
                  'user_registered_time': response[6],
                  'user_status': response[8], 'display_name': response[9],
                  'in_stat': response[10]}
        return result

    def create_statistics_tables(self):
        tables = self.get_tables()
        if 'statistics_table_status' not in tables:
            self.create_table('statistics_table_status', 'statistics_table_status')
        for key in self.statistics_type_indentifier.keys():
            status = self.create_table(key, key)
            if status == "already exists.":
                continue
            # Add to status table
            now = datetime.datetime.now()
            nowstr = now.strftime('%Y-%m-%d %H:%M:%S')
            row = {'table_name': key, 'last_update_time': nowstr}
            self.add_row('statistics_table_status', row)
            for ii in range(self.statistics_type_indentifier[key][0]):
                 self.add_column(key, str(ii+1) + self.statistics_type_indentifier[key][1] , int, 'user_name')

    def add_user_row(self, tablename, username):
        condition = "user_ID>0"
        response1 = self.get_table_element(tablename, 'user_name', condition)
        usr_in = []
        for ele in response1:
            usr_in.append(ele[0])
        if username in usr_in:
            print "User %s already in the table %s."%(username, tablename)
            return
        else:
            self.add_row(tablename,{'user_name':username})
            return
    def create_user_last_input_table(self):
        self.create_table('user_last_index', 'user_last_index')
        self.import_user_from_wp_users('user_last_index')


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


    def update_statistics_time_column(self, datatable, time_blocks=1):
        """This is a function to update statistics data table information by
        time. With a new time block, old time's data will be pushed back.
        For examples, when it is a new hour, the data at recent hour will be pushed
        to the column represents one hour eariler.
        The data is not really get move, it is the column names get moved.
        """
        keys = self.get_table_keys(datatable)
        time_bin = []
        for key in keys:
            keyname = key[0]
            if keyname in ['user_ID','user_name']:
                continue
            if keyname.endswith(('Total','Week','Day','Year')):
                continue
            time_bin.append(keyname)
        suffix = time_bin[0][-1]
        times = np.array([int(x[:-1]) for x in time_bin])
        times_new = times + time_blocks
        msk = np.where(times_new>times.max())
        times_new[msk] = times_new[msk] % times.max()
        msk2 = np.where(times_new == 0 )
        times_new[msk2] = times.max()

        new_colname = [str(x)+'temp' for x in times_new]
        dtype = self.data_type_sep['int']
        # Rotate column names.
        for name_old, name_new in zip(time_bin, new_colname):
            query = "alter table %s change %s %s %s NOT NULL"%(datatable,
                     name_old, name_new, dtype)
            self.cursor.execute(query)

        name_new_suffix = [x.replace('temp',suffix) for x in new_colname]
        for name_temp, name_suffix in zip(new_colname, name_new_suffix):
            query = "alter table %s change %s %s %s"%(datatable,
                     name_temp, name_suffix, dtype)
            self.cursor.execute(query)
        # Updata data
        for index in msk[0]:
            name_zero = name_new_suffix[index]
            query = "update %s set %s=0"%(datatable, name_zero);
            self.cursor.execute(query)
        self.cnx.commit()

    def user_push_update(self, datatable, statistics_type, username):
        table_info = self.statistics_type_indentifier[statistics_type]
        target_col = '1' + table_info[1]
        total = table_info[2]
        query = ("UPDATE %s SET %s=%s+1"
                 " WHERE user_name='%s'"%(datatable, target_col, target_col,
                 username))
        self.cursor.execute(query)
        query = ("UPDATE %s SET %s=%s+1"
                 " WHERE user_name='%s'"%(datatable, total, total, username))
        self.cursor.execute(query)
        self.cnx.commit()
        return 'OK'

    def get_last_update_time(self):
        dt = 'statistics_table_status'
        colvals = self.get_table_column_data(dt, ['last_update_time',])
        rowname = self.get_table_column_data(dt, ['table_name',])
        last_update = {}
        for rown, colv in zip(rowname[0], colvals[0]):
            last_update[rown[0]] = colv[0]

        return last_update
