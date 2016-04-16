# This is a class for sg2 category
# Author Jing Luo
from ..getIMG.sg2_img import ASTRO_IMG
from ..database.sg2_database_utils import image_database
from ..sg2_users.user import USER
import datetime
import numpy


class image_category(object):
    """ This core class for sg2 image category """
    def __init__(self, database, user, project_name=None):
        self.database = database
        self.user = user
        self.project_name = project_name
        self.current_image = None
        self.current_index = 0
        self.current_img_status = None
        self.current_user_result = None
        self.category_dict = {1:'Astronomical Objects', 2:'Atmospheric Limb',
                              3:'Aurora', 4:'Blank', 5:'Camera Malfunction',
                              6:'Clouds', 7:'Dark Earthobs', 8:'Earth Limb',
                              9:'Light Earthobs', 10:'Non Earthobs',
                              11:'Not Specified',12:'Partial Frame',
                              13:'Unfocused Earthobs'}
        self.user_specify = ''
        self.image_info = 'sg2_image_info'
        self.image_rate = 'sg2_image_rate'
        #self.table_in_database = self.check_data_table()

    def check_data_table(self,tablename):
        tables = self.database.tables
        if tablename in tables:
            return True
        else:
            return False

    def create_data_table(self,tablename):
        self.database.creat_table(tablename, 'category')
        self.database.cnx.commit()

    def create_new_user_column(self,tablename):
        self.database.add_column(tablename, self.user.name, str,
                                 'mission')

    def get_all_users(self, tablename):
        """Get all the user name from data_table
        """
        users = self.database.get_all_users(tablename)
        return users

    def get_image_from_database(self,index=None, ID=None):
        row = self.database.get_image_row(self.image_info, index, ID)
        self.current_img_status = row
        self.current_index = index
        self.current_image = ASTRO_IMG(str(row[0][1]))


    def user_input(self, tablename, index, category_code, user_specify=''):
        """category_code is a list of int from 1 to 13
        """
        # Process the new vote and old vote
        new_vote = numpy.zeros(13, dtype=int)
        old_vote = numpy.zeros(13, dtype=int)
        new_vote[numpy.array(category_code)-1] = 1
        vote_col = ''
        vote_result = {}
        for ii,v in enumerate(new_vote):
            cat_name = 'c%d'%(ii+1)
            vote_col += cat_name+', '
            vote_result[cat_name] = v
        vote_col = vote_col[:-2]
        # Get user name
        usr = self.user.name
        uinput = ''
        info_row = self.database.get_image_row('sg2_image_info', index)[0]
        info_row_key = self.database.get_table_keys('sg2_image_info')
        # Get all image voting infp
        img_info = {}
        for rkey,val in zip(info_row_key, info_row):
            img_info[rkey[0]] = val

        condition = "info_table_index=%d"%index
        rate_cols = 'rater_name, rate_index, ' + vote_col
        # check if user_specified
        usrspc = ''
        if 11 in category_code:
            usrspc = user_specify

        rate_rows = self.database.get_table_element('sg2_image_rate', rate_cols, condition)
        raters = []
        for rate_r in rate_rows:
            raters.append(rate_r[0])



        rate_plus = 0
        if usr in raters:
            idx = raters.index(usr)
            rate_index = rate_rows[idx][1]
            old_vote = numpy.array(rate_rows[idx][2:])
            query = "UPDATE %s SET "%'sg2_image_rate'
            for key in vote_result.keys():
               query += "%s = %d, "%(key, vote_result[key])
            query += "other='%s'"%usrspc
            query += " WHERE rate_index=%d"%rate_index
        else:
            if img_info['number_rated']>img_info['max_rate'] or img_info['quality_control'] == 1:
                return 0
            # Check if there is an empty space
            if '' in raters:
                idx = raters.index('')
                rate_index = rate_rows[idx][1]
                query = "UPDATE %s SET "%'sg2_image_rate'
                for key in vote_result.keys():
                   query += "%s = %d, "%(key, vote_result[key])
                query += "rate_check=1, rater_name='%s', other='%s'"%(usr, usrspc)
                query += " WHERE rate_index=%d"%rate_index
            # No empty space add one for the change of max_rate
            else:
                insert_dict = {'image_ID':img_info['image_ID'],
                               'info_table_index': img_info['image_index'],
                               'rater_name': usr,
                               'rate_check': 1,
                               'other': usrspc}
                insetr_dict.update(cat_mapping)
                self.add_row('sg2_image_rate', insert_dict)
            rate_plus = 1
        vote_diff = new_vote - old_vote

        self.database.cursor.execute(query)

        # update image_info table
        query = "UPDATE %s SET "%'sg2_image_info'
        for ii,vn in enumerate(vote_diff):
           query += "%s = %s+%d, "%("c%d"%(ii+1), "c%d"%(ii+1), vn)
        query += "number_rated = number_rated+%d WHERE image_index=%d"%(rate_plus, index)

        self.database.cursor.execute(query)


        # update statistics
        if rate_plus != 0:
            for table in self.user.db.statistics_type_indentifier.keys():
                self.user.db.user_push_update(table, table, usr)
            self.update_user_last_index(index)
        self.database.cnx.commit()
        return 1

    def update_user_last_index(self, last_index):
        if self.user.user_info != []:
            uname = self.user.user_info['user_login']
        else:
            raise ValueError('User %s is not in database'%self.user.name)
        query = ("UPDATE %s SET user_last_index=%s"
                 " WHERE user_name='%s'"%('user_last_index',last_index,uname))
        self.user.db.cursor.execute(query)
        self.user.db.cnx.commit()

    def set_quailty_control(self, image_id, value):
        tname = self.image_info
        if value:
            v = 1
        else:
            v = 0

        query = ("UPDATE %s SET quality_control = %d "
                 "WHERE image_ID='%s'"%(tname, v, image_id))
        self.database.cursor.execute(query)


if __name__ == "__main__":
    pass
