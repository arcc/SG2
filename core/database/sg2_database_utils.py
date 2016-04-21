# This is a utils for sg2 image database
#Author Jing Luo
import mysql.connector
from mysql.connector import errorcode
from .database_utils import DataBase
import os.path


class image_database(DataBase): # API to interact with database
    def __init__(self, **login_info):
        super(image_database, self).__init__(**login_info)
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

        self.table_template.update({'rate':
                           lambda x:( "CREATE TABLE `%s` ("
                             "  `rate_index` int(11) NOT NULL AUTO_INCREMENT,"
                             "  `image_ID` varchar(20) NOT NULL,"
                             "  `info_table_index` int(11) NOT NULL,"
                             "  `rater_name` varchar(20) NOT NULL,"
                             "  `rate_time` TIMESTAMP,"
                             "  `c1` TINYINT(1) NOT NULL,"
                             "  `c2` TINYINT(1) NOT NULL,"
                             "  `c3` TINYINT(1) NOT NULL,"
                             "  `c4` TINYINT(1) NOT NULL,"
                             "  `c5` TINYINT(1) NOT NULL,"
                             "  `c6` TINYINT(1) NOT NULL,"
                             "  `c7` TINYINT(1) NOT NULL,"
                             "  `c8` TINYINT(1) NOT NULL,"
                             "  `c9` TINYINT(1) NOT NULL,"
                             "  `c10` TINYINT(1) NOT NULL,"
                             "  `c11` TINYINT(1) NOT NULL,"
                             "  `c12` TINYINT(1) NOT NULL,"
                             "  `c13` TINYINT(1) NOT NULL,"
                             "  `other` varchar(40) NOT NULL,"
                             "  `rate_check` TINYINT(1) NOT NULL,"
                             "  PRIMARY KEY (`rate_index`)"
                             ") ENGINE=InnoDB")%x,
                              })

        self.table_template.update({'image_info':
                           lambda x:( "CREATE TABLE `%s` ("
                             "  `image_index` int(11) NOT NULL AUTO_INCREMENT,"
                             "  `image_ID` varchar(20) NOT NULL,"
                             "  `mission` varchar(20) NOT NULL,"
                             "  `project` varchar(20) NOT NULL,"
                             "  `time_added` TIMESTAMP DEFAULT 0,"
                             "  `c1` int(11) NOT NULL COMMENT 'Number of rate in category 1',"
                             "  `c2` int(11) NOT NULL COMMENT 'Number of rate in category 2',"
                             "  `c3` int(11) NOT NULL COMMENT 'Number of rate in category 3',"
                             "  `c4` int(11) NOT NULL COMMENT 'Number of rate in category 4',"
                             "  `c5` int(11) NOT NULL COMMENT 'Number of rate in category 5',"
                             "  `c6` int(11) NOT NULL COMMENT 'Number of rate in category 6',"
                             "  `c7` int(11) NOT NULL COMMENT 'Number of rate in category 7',"
                             "  `c8` int(11) NOT NULL COMMENT 'Number of rate in category 8',"
                             "  `c9` int(11) NOT NULL COMMENT 'Number of rate in category 9',"
                             "  `c10` int(11) NOT NULL COMMENT 'Number of rate in category 10',"
                             "  `c11` int(11) NOT NULL COMMENT 'Number of rate in category 11',"
                             "  `c12` int(11) NOT NULL COMMENT 'Number of rate in category 12',"
                             "  `c13` int(11) NOT NULL COMMENT 'Number of rate in category 13',"
                             "  `number_rated` int(11) NOT NULL,"
                             "  `max_rate` int(11) NOT NULL,"
                             "  `rate_result` varchar(40) NOT NULL,"
                             "  `other_category` varchar(40) NOT NULL,"
                             "  `time_finished` TIMESTAMP DEFAULT 0,"
                             "  `quality_control` TINYINT(1) NOT NULL,"
                             "  PRIMARY KEY (`image_index`)"
                             ") ENGINE=InnoDB")%x,
                              })

        self.table_template.update({'project_info':
                           lambda x:( "CREATE TABLE `%s` ("
                             "  `project_index` int(11) NOT NULL AUTO_INCREMENT,"
                             "  `project_name` varchar(20) NOT NULL,"
                             "  `time_added` TIMESTAMP DEFAULT 0,"
                             "  `finish` TINYINT(1) NOT NULL,"
                             "  `time_finished` TIMESTAMP DEFAULT 0,"
                             "  `number_image` int(11) NOT NULL,"
                             "  `start_image_index` int(11) NOT NULL COMMENT 'Project first image index in image_info table',"
                             "  `end_image_index` int(11) NOT NULL COMMENT 'Project last image index in image_info table',"
                             "  PRIMARY KEY (`project_index`)"
                             ") ENGINE=InnoDB")%x,
                              })

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

    def get_image_row(self, table_name, index=None, ID=None):
        if index is not None:
            query = "SELECT * FROM %s WHERE image_index=%d"%(table_name, index)
        elif ID is not None:
            query = "SELECT * FROM %s WHERE image_ID='%s'"%(table_name, ID)
        else:
            raise RuntimeError('Index or ID has to be provide.')
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return response



    def load_image_list_file(self, table_name, filename, field_spe, line_sep,
                             colnames):
        """Load image list file to table
        """
        if not os.path.isfile(filename):
            raise ValueError('Please provide the full path of file '+ filename)
        query =( "LOAD DATA LOCAL INFILE '%s'  INTO TABLE %s"
                 " FIELDS TERMINATED BY '%s'"
                 " LINES TERMINATED BY '%s'"
                 " ("%(filename, table_name, field_spe, line_sep))
        for cn in colnames:
            query += "%s,"%cn
        query = query[:-1]+ ")"
        self.cursor.execute(query)

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

    def get_all_rating(self, table_name, image_id):
        """Get all users from data table
        """
        ratings = self.get_table_row(table_name, "image_id='%s'"%image_id)
        print ratings
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

    def get_rate_time(self, datatable, rater_name, time_start, time_end):
        query = ("SELECT rate_time FROM %s WHERE rater_name='%s' AND")%(datatable, rater_name)
        query +=" rate_time BETWEEN %s AND %s"
        self.cursor.execute(query, (time_start, time_end))
        response = self.cursor.fetchall()
        return response
