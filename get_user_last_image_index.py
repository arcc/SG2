#!/usr/bin/python
"""
This is a python script for get next image from database.
useage:
    $python get_user_last_image.py username project_name users_table
Return:
    print User last ranked image index
    If anything wrong
    print -1
"""
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys
import get_config as gc
cf = gc.get_config('config.dat')

def get_last_image_index(username):
    user = u.USER(username)
    condition = "user_name='%s'"%username
    try:
        res = user.db.get_table_element('user_last_index','user_last_index', condition)
    except:
        return json.dumps('-1')
    return json.dumps(res[0][0])


if __name__== "__main__":
    username = sys.argv[1]
    print get_last_image_index(username)
# Author Jing Luo
