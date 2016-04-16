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
mport get_config as gc

cf = gc.get_config('config.dat')
db = image_database(user=cf['img_db_usr'], password=cf['img_db_pw'])
def push_result(username, index_in_db, category_code, user_specify=''):
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
    user = u.USER(username)
    imc = sg2c.image_category(db, user)
    result = imc.user_input('sg2_image_rate', index_in_db, category_code, user_specify=user_specify)
    return json.dumps((str(result), str(index_in_db)))

if __name__== "__main__":
    username = sys.argv[1]
    img_index = int(sys.argv[2])
    user_result = sys.argv[3]
    user_result = user_result.split(',')
    if user_result[-1] == '':
        user_result.remove(user_result[-1])
    user_result_dig = [int(x) for x in user_result if int(x) != 0]
    if user_result_dig == []:
        print json.dumps(("0", str(img_index)))
        exit()

    if len(sys.argv) == 5:
        user_specify = sys.argv[4]
        print push_result(username, img_index, user_result_dig, user_specify=user_specify)
    else:
        print push_result(username, img_index, user_result_dig)
    # # Author Jing Luo
