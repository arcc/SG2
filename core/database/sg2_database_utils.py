# This is a utils for sg2 image database
#Author Jing Luo
import mysql.connector
from mysql.connector import errorcode
from .database_utils import DataBase
import os.path


class image_database(DataBase): # API to interact with database
    def __init__(self, local=True, user='root', password='****', host='localhost',
                 port='8889', database='sg2image',
                 unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock'):
                  # right now it is only support localhost via MAMP
        if local:
            super(image_database, self).__init__(password=password,
                                                 database=database)
        else:
            super(image_database, self).__init__(local=loacl, user=user,
                                                 password=password, host=host,
                                                 port=port, database=database,
                                                 unix_socket=unix_socket)
        self.table_template.update({'category':
                           lambda x:( "CREATE TABLE `%s` ("
                             "  `image_index` int(11) NOT NULL AUTO_INCREMENT,"
                             "  `image_ID` varchar(20) NOT NULL,"
                             "  `mission` varchar(20) NOT NULL,"
                             "  `other` varchar(40) NOT NULL,"
                             "  `number_categoried` int(11) NOT NULL,"
                             "  `catelog_result` varchar(40) NOT NULL,"
                             "  `quality_control` TINYINT(1) NOT NULL,"
                             "  PRIMARY KEY (`image_index`)"
                             ") ENGINE=InnoDB")%x,
                              })

        self.table_default_columns = {'category':
                                       ['image_index', 'image_ID', 'mission',
                                        'other', 'number_categoried',
                                        'catelog_result', 'quality_control']}
        self.image_table_prefix = 'sg2'

    def get_total_num_image(self, tablename):
        query = "SELECT COUNT(*) FROM %s"%tablename
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        return response[0]

    def get_image_row(self, table_name, index):
        query = "SELECT * FROM %s WHERE image_index=%s"%(table_name, index)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

    def load_image_list_file(self, table_name, filename, field_spe, line_sep,
                             colnames):
        """Load image list file to table
        """
        if not os.path.isfile(filename):
            raise ValueError('Please provide the full path of file '+ filename)
        query =( "LOAD DATA INFILE '%s'  INTO TABLE %s"
                 " FIELDS TERMINATED BY '%s'"
                 " LINES TERMINATED BY '%s'"
                 " ("%(filename, table_name, field_spe, line_sep))
        for cn in colnames:
            query += "%s,"%cn
        query = query[:-1]+ ")"
        self.cursor.execute(query)



    def search_image(self, table_name, image_ID):
        query = "SELECT * FROM " + table_name + " WHERE image_ID = %s"
        self.cursor.execute(query, (image_ID,))
        response = self.cursor.fetchall()
        return response

    def delete_image(self ,table_name, image_ID=None, index=None):
        if id is None:
            if index is None:
                raise ValueError('Please speicify the row index or image ID '
                                 'to delete image using optional argument id '
                                 ' or index.')
            else:
                query = "DELETE FROM " + table_name +" WHERE image_index = %s"
                self.cursor.execute(query,(index,))
                return
        else:
            query = "DELETE FROM " + table_name +" WHERE image_ID = %s"
            self.cursor.execute(query, (image_ID,))
            return

    def add_image(self, table_name,img_id):
        add_image = ("INSERT INTO " + table_name +
                     " (image_id) "
                     "VALUES (%s)")
        self.cursor.execute(add_image, (img_id,))

    def get_all_users(self, table_name):
        """Get all users from data table
        """
        col_name = self.get_table_keys(table_name)
        users = []
        for col in col_name:
            colkey = col[0]
            if colkey not in self.table_default_columns['category']:
                users.append(colkey)
        return users

    def get_final_result(self, table_name,img_id):
        usrs = self.get_all_users(table_name)
        col, colkeys = self.get_table_column_data(table_name, usrs,'image_index=%s'%img_id)
        user_result = {}
        compare = []
        for ii, res in enumerate(col[0]):
            res =  res.split(',')
            m = filter(bool, res)
            m = map(int,m)
            user_result[colkeys[ii]] = m
            if m != []:
                compare.append(set(m))

        result_int = list(reduce(set.intersection, compare))
        result_str = ''
        for res in result_int:
            result_str += str(res) + ','
        return result_str
