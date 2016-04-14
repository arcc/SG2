#!/usr/bin/python
"""
This is a python script to setup the database
"""
from core.database.users_database_utils import users_database
from core.database.sg2_database_utils import image_database

# setup the users database
usrdb = users_database(password='root')
usrdb.create_statistics_tables()
usr_tables = usrdb.get_tables()
for utb in usr_tables:
    if utb.startswith('user_statistics'):
        usrdb.import_user_from_wp_users(utb)
usrdb.create_user_last_input_table()
usrdb.import_user_from_wp_users('user_last_index')


# setup the image database
imgdb = image_database(password='root')
# Create project table
imgdb.create_table('projects', 'project_info')
# Create image info table
imgdb.create_table('sg2_image_info', 'image_info')
# Creat the image rate table
imgdb.create_table('sg2_image_rate', 'rate')
#


# Get two database work together
# add users to image category
# response1 = imgdb.get_table_keys('sg2_image_test')
# img_table_keys = []
# for ele in response1:
#     img_table_keys.append(ele[0])
# condition = "ID>0"
# response2 = usrdb.get_table_element('wp_users', 'user_login', condition)
# for ele in response2:
#     usr = ele[0]
#     if usr in img_table_keys or usr == '':
#         continue
#     else:
#         imgdb.add_column('sg2_image_test', usr, str, "mission")
# # Add table to user last index
# response1 = usrdb.get_table_keys('user_last_index')
# last_idx_table_keys = []
# for ele in response1:
#     last_idx_table_keys.append(ele[0])
# tables = imgdb.get_tables()
# sg2_tables = []
# for tn in tables:
#     if tn.startswith('sg2'):
#         sg2_tables.append(tn)
# for sg2_tn in sg2_tables:
#     if sg2_tn in last_idx_table_keys:
#         continue
#     else:
#         usrdb.add_column('user_last_index', sg2_tn, int, "user_name")
usrdb.cnx.commit()
imgdb.cnx.commit()
usrdb.cnx.close()
imgdb.cnx.close()
#author Luo Jing
