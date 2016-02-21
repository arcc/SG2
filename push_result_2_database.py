#!/usr/bin/python
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys


db = image_database(password='root')
def push_result(username, project_name, index_in_db, category_code, user_specify='',
                max_rate=4,):
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
    push_result(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
