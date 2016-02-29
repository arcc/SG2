#!/usr/bin/python
"""
This is a python script for creating a new user column in the database.
useage:
    $python create_user_column.py username project_name
Return:
    If user exists.
    print "User exists."
    if user does not exist
    print "Ok"
"""
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys

db = image_database(password='root')

def create_user_column(username, project_name):
    user = u.USER(username)
    imc = sg2c.image_category( db, user, project_name)
    imc.change_data_table(project_name)
    if user.name in imc.get_all_users(project_name):
        return json.dumps('User exists.')
    else:
        imc.create_new_user_column(project_name)
        return json.dumps('Ok')

if __name__== "__main__":
    username = str(sys.argv[1])
    project_name = str(sys.argv[2])
    result = create_user_column(username, project_name)
    print result
