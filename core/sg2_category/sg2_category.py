from ..getIMG.sg2_img import ASTRO_IMG
from ..database.sg2_database_utils import image_database
from ..sg2_users.user import USER


class image_category(object):
    """ This core class for sg2 image category """
    def __init__(self, database, user, project_name):
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
        self.data_table = None

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

    def change_data_table(self,tablename):
        if self.check_data_table(tablename):
            self.data_table = tablename
        else:
            raise RuntimeError("Table " + tablename + " not in database.")

    def create_new_user_column(self,):
        self.database.add_column(self.data_table, self.user.name, str,
                                 'mission')

    def get_image_from_database(self,index):
        row = self.database.get_image_row(self.data_table, index)
        self.current_img_status = row
        self.current_index = index
        self.current_image = ASTRO_IMG(str(row[0][1]))
        user_result = self.database.get_table_element(self.data_table ,
                                                      self.user.name,
                                                      'image_index=%d'%index)
        self.current_user_result = str(user_result[0][0])

    def user_input(self, category_code):
        """category_code is a list of int from 0 to 12
        """
        if not isinstance(category_code,(list,tuple)):
            category_code = [category_code,]
        tname = self.data_table
        usr = self.user.name
        uinput = ''
        index = self.current_index
        for res in category_code:
            uinput += str(res)+','
        query = ("UPDATE %s SET %s = '%s' "
                 "WHERE image_index=%s"%(tname, usr, uinput, index))
        self.database.cursor.execute(query)
        if 11 in category_code:
            query = ("UPDATE %s SET other = '%s' "
                     "WHERE image_index=%d"%(tname, self.user_specify, index))
        self.database.cursor.execute(query)
        query = ("UPDATE %s SET number_categoried=number_categoried+1"
                 " WHERE image_index=%d"%(tname, index))
        self.database.cursor.execute(query)

    def set_quailty_control(self, image_id, value):
        tname = self.data_table
        if value:
            v = 1
        else:
            v = 0

        query = ("UPDATE %s SET quality_control = %d "
                 "WHERE image_ID='%s'"%(tname, v, image_id))
        self.database.cursor.execute(query)


if __name__ == "__main__":
    pass
