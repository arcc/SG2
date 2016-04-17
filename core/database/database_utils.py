# A database basic utility fuctions.
import mysql.connector
from mysql.connector import errorcode
import database_utils as dbut
from mysql.connector.constants import ClientFlag
import os.path

class DataBase(object): # API to interact with database
    # def __init__(self, local=True, user='root', password='****', host='127.0.0.1',
    #              port=3306, database=None, client_flags=[ClientFlag.LOCAL_FILES],
    #              unix_socket='/var/lib/mysql/mysql.sock'):
    def __init__(self, **login_info):

        self.server_info = login_info
        # self.server_info = {
        #                     'user': user, 'password': password,
        #                     'host': host, 'port': port,
        #                     'unix_socket': unix_socket,
        #                     'database': database,
        #                     'client_flags': [ClientFlag.LOCAL_FILES]
        #                    }
        self.data_type_sep = {'str': 'varchar(40)',
                              'int': 'INT(20)',
                              'bool': 'TINYINT(1)'}

        self.table_template = {}


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
        return self.tables

    def create_table(self, name, table_type):
        if table_type not in self.table_template.keys():
            raise ValueError('Undefined table type ' + table_type)
        try:
            print "Creating table %s as type %s: "%(name, table_type)
            self.cursor.execute(self.table_template[table_type](name))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
                return "already exists."
            else:
                print(err.msg)
                return "error"
        else:
            print "OK"
            return "OK"
    def is_empty(self, tablename):
        query = "SELECT 1 FROM %s LIMIT 1" % tablename
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        if response==[]:
            return True
        return False

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
        query  = ("ALTER TABLE %s ADD `%s` %s NOT NULL"
                  " after `%s`"%(table_name, column_name, colt, after_col_name))
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

    def add_rows(self, table_name, colname, values):
        coln = " ("
        colv = "("
        for key in colname:
            coln += key + ","
            colv += "%s,"
        coln = coln[:-1] + ") "
        colv = colv[:-1] + ") "
        query = ("""INSERT INTO %s %s VALUES %s"""%(table_name, coln, colv))
        self.cursor.executemany(query,values)

    def update_element(self, tablename, column, condition, value):
        query = ("UPDATE %s SET %s = '%s' "
                 "WHERE %s"%(tablename, column, value, condition))
        self.cursor.execute(query)

    def get_table_element(self, table_name, colname, condition):
        if self.is_empty(table_name):
            return []
        query = "SELECT %s FROM %s WHERE %s "%(colname, table_name, condition)
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response

    def get_table_last_row(self, table_name, sort_key, colname='*'):
        query = "SELECT %s FROM %s ORDER BY %s DESC LIMIT 1"%(colname, table_name, sort_key)
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
