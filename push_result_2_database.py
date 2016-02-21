#!/usr/bin/python
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys


db = image_database(password='root')
def push_result(username, project_name, index_in_db, category_code, user_specify='',
                max_rate=4):
    """
    """
    index_in_db = int(index_in_db)
    max_rate = int(max_rate)
    user = u.USER(username)
    imc = sg2c.image_category( db, user, project_name)
    imc.user_specify = user_specify
    imc.change_data_table(project_name)
    num_rated = imc.database.get_table_element(project_name, 'number_categoried',
                                     'image_index=%d'%index_in_db)
    if num_rated[0][0] > max_rate:
        return
    else:
        imc.get_image_from_database(index_in_db)
        imc.user_input(category_code)
        imc.database.cnx.commit()
        return

if __name__== "__main__":
    username = sys.argv[1]
    project_name = sys.argv[2]
    img_index = int(sys.argv[3])
    user_result = sys.argv[4]
    user_result = user_result.split(',')
    user_result_dig = [int(x) for x in user_result if int(x) != 0]
    if user_result_dig == []:
        sys.exit()
    if len(sys.argv) >= 6:
        max_rate = sys.argv[5]
        push_result(username, project_name, img_index, user_result_dig, max_rate)
    else:
        push_result(username, project_name, img_index, user_result_dig)
