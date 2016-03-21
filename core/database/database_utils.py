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
                              'int': 'INT(20)',
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

    def create_table(self, name, table_type):
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

    def get_table_keys(self, table_name):
        self.cursor.execute('SHOW COLUMNS FROM %s'%table_name)
        response = self.cursor.fetchall()
        return response

    def get_table_row(self, table_name, condition):
        query = "SELECT * FROM %s WHERE %s "%(table_name, condition)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

    def get_table_column_data(self, table_name, column_names, condition=''):
        """This a function to get the column from the database.
        """
        col_name = ''
        col = self.get_table_keys(table_name)
        col_keys = []
        for c in col:
            col_keys.append(c[0])
        for cn in column_names:
            if cn not in col_keys:
                raise ValueError("Column %s is not in the table %s."%(cn,
                                 table_name))
            col_name += cn +','
        col_name = col_name[:-1]
        if condition == '':
            query = "SELECT %s FROM %s"%(col_name, table_name)
        else:
            query = "SELECT %s FROM %s WHERE %s "%(col_name, table_name, condition)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response, column_names

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

    def add_row(self, table_name, col):
        """
        Parameter
        ---------
        table_name : str
            Name of table
        col : dict
            Column name ane column value
        """
        #"VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)"
        coln = " ("
        colv = "("
        for key in col.keys():
            coln += key + ","
            colv += "%("+ key + ")s,"
        coln = coln[:-1] + ") "
        colv = colv[:-1] + ") "
        query = ("INSERT INTO " + table_name + coln +
                     "VALUES " + colv)
        self.cursor.execute(query, col)


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
