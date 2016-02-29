import mysql.connector
from mysql.connector import errorcode
import os.path


class image_database(object): # API to interact with database
    def __init__(self, local=True, user='root', password='****', host='localhost',
                 port='8889', database='sg2image',
                 unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock'):
                  # right now it is only support localhost via MAMP
        self.server_info = {
                            'user': user, 'password': password,
                            'host': host, 'port': port,
                            'unix_socket': unix_socket,
                            'database': database
                           }
        self.table_template = {'category':
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
                              }
        self.data_type_sep = {'str': 'varchar(40)',
                              'int': 'int(20)',
                              'bool': 'TINYINT(1)'}
        self.table_default_columns = {'category':
                                       ['image_index', 'image_ID', 'mission',
                                        'other', 'number_categoried',
                                        'catelog_result', 'quality_control']}

        if local:
            self.login_database()
            self.get_tables()
    def update_server_info(self, key, value):
        if key in self.server_info.keys():
            self.server_info[key] = value

    def login_database(self):
        info = self.server_info
        self.cnx = mysql.connector.connect(**self.server_info)
        self.cursor = self.cnx.cursor(buffered=True)

    def get_tables(self,):
        self.cursor.execute("SHOW TABLES")
        response = self.cursor.fetchall()
        self.tables = []
        for t in response:
            self.tables.append(t[0])
    def get_table_columns(self, table_name):
        self.cursor.execute('SHOW COLUMNS FROM %s'%table_name)
        response = self.cursor.fetchall()
        return response

    def display_database_info(self, showcommand):
        self.cursor.execute(showcommand)
        response = self.cursor.fetchall()
        print response

    def creat_table(self, name, table_type):
        if table_type not in self.table_template.keys():
            raise ValueError('Undefined table type ' + table_type)
        try:
            print "Creating table %s as type %s: "%(name, table_type)
            self.cursor.execute(self.table_template[table_type](name))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print "OK"

    def delete_table(self, tablename):
        self.cursor.execute("DROP TABLE " + tablename)

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

    def get_table_element(self, table_name, colname, condition):
        query = "SELECT %s FROM %s WHERE %s "%(colname, table_name, condition)
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

    def add_column(self, table_name, column_name, col_type, after_col_name):
        """ Add a column to a table.
            Parameter
            ---------
            table_name : str
            column_name : str
            col_type : type
                New column type
            after_col_name : str
                New column is after one of the old column.
        """
        coltype_string = col_type.__name__
        if coltype_string not in self.data_type_sep.keys():
            raise ValueError('Unknown type '+ coltype_string)
        colt = self.data_type_sep[coltype_string]
        query  = ("ALTER TABLE %s ADD %s %s NOT NULL"
                  " after %s"%(table_name, column_name, colt, after_col_name))
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

    def close(self):
        self.cnx.close()
