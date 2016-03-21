# This file is for user class
from ..database.users_database_utils import users_database

db_login_pw = 'root'
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
        self.db = users_database(password=db_login_pw)

    def get_user_info(self, username, tablename):
        self.user_info = self.db.get_user(tablename, username)

    def update_user_info(self, username, tablename):
        pass

    def get_user_statistics(self, username, tablename):
        pass
