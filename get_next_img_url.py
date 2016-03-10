#!/usr/bin/python
"""
This is a python script for get next image from database.
useage:
    $python get_next_image_url.py username project_name index_in_db
    or
    $python get_next_image_url.py username project_name index_in_db max_rate
Return:
    print [small image url, large image url, index]
    If the index execcds from the database
    print ['-1', '-1', index]
"""
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys



db = image_database(password='root')

def get_next_image_url(username, project_name, index_in_db, max_rate=4):
    """This is a wrapper funciton for sg2 category php
    Parameter
    ----------
    username : str
        The user name who is categorating sg2 image
    projcet_name : str
        The projcet name, which represents the database table name
    index_in_db : int
        The image index in database
    max_rate :  int
        The maximum number one picture should be rated
    Return
    -----------
    JSON dump image url and image index in database
    """
    index_in_db = int(index_in_db)
    max_rate = int(max_rate)
    user = u.USER(username)
    imc = sg2c.image_category( db, user, project_name)
    imc.change_data_table(project_name)
    if index_in_db > imc.total_img_in_table:
        return json.dumps(('-1', '-1', index_in_db))
    if index_in_db == 0:
        index_in_db = 1
    num_rated = imc.database.get_table_element(project_name, 'number_categoried',
                                     'image_index=%d'%index_in_db)
    user_result = imc.database.get_table_element(project_name, username,
                                     'image_index=%d'%index_in_db)
    user_result = user_result[0][0]

    while num_rated[0][0] >= max_rate or user_result != '':
        index_in_db += 1
        if index_in_db > imc.total_img_in_table:
            return json.dumps(('-1', '-1', index_in_db))
        num_rated = imc.database.get_table_element(project_name, 'number_categoried',
                                         'image_index=%d'%index_in_db)
        user_result = imc.database.get_table_element(project_name, username,
                                         'image_index=%d'%index_in_db)
        user_result = user_result[0][0]

    imc.get_image_from_database(index_in_db)
    url = imc.current_image.image_url
    url_large = imc.current_image.image_url_large
    index = imc.current_index
    return json.dumps((url, url_large, index))

if __name__== "__main__":
    username = sys.argv[1]
    project_name = sys.argv[2]
    img_index = int(sys.argv[3])
    if len(sys.argv) >= 5:
        max_rate = int(sys.argv[4])
        print get_next_image_url(username, project_name, img_index,
                                 max_rate)
    else:
       print get_next_image_url(username, project_name, img_index)
