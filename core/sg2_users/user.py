# This file is for user class
from ..database.users_database_utils import users_database
import numpy as np
import get_config as gc
# Here we are using wp_users table as user info storage.
cf = gc.get_config('config.dat')
class USER(object):
    """This is a class for sg2 user
    """
    def __init__(self, username, **kwargs):
        self.name = username
        self.user_info = None
        self.privilege_level = None
        self.num_images_processed = 0
        self.accurate_rate = 0.0
        self.last_ranked_image = 0
        self.db = users_database(user=cf['user_db_usr'],password=cf['user_db_pw'])
        self.get_user_info(self.name, 'wp_users')
        self.time_unit_type = {'day': ('user_statistics_day', 'Hour'),
                               'week': ('user_statistics_week', 'Day'),
                               'year': ('user_statistics_year', 'Week')}
    def get_user_info(self, username, tablename):
        self.user_info = self.db.get_user(tablename, username)
        return self.user_info

    def update_user_info(self, username, tablename):
        pass

    def get_user_statistics(self, username, time_unit):
        table_name = self.time_unit_type[time_unit][0]
        time_bin_unit = self.time_unit_type[time_unit][1]
        x,y = self.db.get_user_statistics(table_name, username)
        xval = [int(v[:-1]) for v in x]
        yval = [v1 for (v2,v1) in sorted(zip(xval,y))]
        xval.sort()
        xaxis = -1 * (np.array(xval[::-1]) - 1)
        yaxis = yval[::-1]
        return xaxis, yaxis, time_bin_unit
