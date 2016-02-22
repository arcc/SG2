#!/usr/bin/python
"""
This is a python script for push category result to database.
useage:
    $python push_result_2_database.py username project_name index_in_db category
    (user_specify or max_rate)
    or
    $python push_result_2_database.py username project_name index_in_db category
    user_specify max_rate

    The category should be like 1,2,3,12
"""
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys


db = image_database(password='root')
def push_result(username, project_name, index_in_db, category_code, user_specify='',
                max_rate=4):
    """A function pushes a result to database
    Parameter
    ----------
    username : str
        User name
    project_name : str
        Project name, database table name
    index_in_db : int
        Index of image of database
    category_code : list of int
        The category code input for the image from 1 to 13
    user_specify : str, optional default ''
        If no Specified, user input their answer
    max_rate : int optional default 4
        Maximum number of rated.
    """
    index_in_db = int(index_in_db)
    max_rate = int(max_rate)
    user = u.USER(username)
    imc = sg2c.image_category( db, user, project_name)
    imc.user_specify = user_specify
    imc.change_data_table(project_name)
    if index_in_db > imc.total_img_in_table:
        return
    num_rated = imc.database.get_table_element(project_name, 'number_categoried',
                                     'image_index=%d'%index_in_db)
    user_result_before = imc.database.get_table_element(project_name, username,
                                     'image_index=%d'%index_in_db)[0][0]

    if num_rated[0][0] > max_rate and user_result_before == '':
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



    if len(sys.argv) == 6:
        try:
            max_rate = int(sys.argv[5])
            push_result(username, project_name, img_index, user_result_dig,
                        max_rate=max_rate)
        except:
            user_specify = sys.argv[5]
            push_result(username, project_name, img_index, user_result_dig,
                        user_specify=user_specify)

    elif len(sys.argv) == 7:
        max_rate = int(sys.argv[6])
        user_specify = sys.argv[5]
        push_result(username, project_name, img_index, user_result_dig,
                    max_rate=max_rate, user_specify=user_specify)
