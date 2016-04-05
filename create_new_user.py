#!/usr/bin/python
"""
This is a python script for creating a new user in the database but not in
the wordpress database. The user has to register in the wordpress first.
New user will be add to table :
1. all image_category tables
2. user stat tables
3. user last_index table
useage:
    $python create_user.py username
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

imgdb = image_database(password='root')

def create_user(username):
    user = u.USER(username)

    userInfo = user.get_user_info(user.name, 'wp_users')
    if userInfo == []:
        raise RuntimeError("Finding user %s's information in wordpress "
                            "database failed." % username)
    # Add statistics table
    usr_tables = user.db.get_tables()
    for utb in usr_tables:
        if utb.startswith('user_statistics'):
            user.db.add_user_row(utb, userInfo['user_login'])
    user.db.add_user_row('user_last_index',userInfo['user_login'])

    # Add user to all image_category table
    imc = sg2c.image_category(imgdb, user)
    tbs = imgdb.get_tables()
    for tb in tbs:
        if tb.startswith('sg2'):
            if user.name in imc.get_all_users(tb):
                continue
            else:
                imc.create_new_user_column(tb)
    # Author Luo Jing
    imc.database.cnx.commit()
    user.db.cnx.commit()
    return json.dumps('Ok')

if __name__== "__main__":
    username = str(sys.argv[1])
    #project_name = str(sys.argv[2])
    result = create_user(username)
    print result
