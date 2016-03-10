# A database basic utility fuctions.
import mysql.connector
from mysql.connector import errorcode
import database_utils as dbut
import os.path

class DataBase(object): # API to interact with database
    def __init__(self, local=True, user='root', password='****', host='localhost',
                 port='8889', database=None,
                 unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock'):

        self.server_info = {
                            'user': user, 'password': password,
                            'host': host, 'port': port,
                            'unix_socket': unix_socket,
                            'database': database
                           }
        self.data_type_sep = {'str': 'varchar(40)',
                              'int': 'int(20)',
                              'bool': 'TINYINT(1)'}

        self.table_template = {}

        if local:
            self.login_database()
            self.get_tables()

    def update_server_info(self, key, value):
        if key in self.server_info.keys():
            self.server_info[key] = value

    def login_database(self):
        info = self.server_info
        try:
            self.cnx = mysql.connector.connect(**self.server_info)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.cnx.cursor(buffered=True)

    def get_tables(self,):
        self.cursor.execute("SHOW TABLES")
        response = self.cursor.fetchall()
        self.tables = []
        for t in response:
            self.tables.append(t[0])

    def get_table_element(self, table_name, colname, condition):
        query = "SELECT %s FROM %s WHERE %s "%(colname, table_name, condition)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

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

    def get_table_columns(self, table_name):
        self.cursor.execute('SHOW COLUMNS FROM %s'%table_name)
        response = self.cursor.fetchall()
        return response

    def get_table_row(self, table_name, condition):
        query = "SELECT * FROM %s WHERE %s "%(table_name, condition)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

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

    def update_element(self, tablename, column, condition, value):
        query = ("UPDATE %s SET %s = '%s' "
                 "WHERE %s"%(tablename, column, value, condition))
        self.cursor.execute(query)

    def get_table_element(self, table_name, colname, condition):
        query = "SELECT %s FROM %s WHERE %s "%(colname, table_name, condition)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

    def display_database_info(self, showcommand):
        self.cursor.execute(showcommand)
        response = self.cursor.fetchall()
        print response

    def delete_table(self, tablename):
        self.cursor.execute("DROP TABLE " + tablename)

    def close(self):
        self.cnx.close()
