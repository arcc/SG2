#!/usr/bin/python
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys



db = image_database(password='root')

def get_next_image_url(username, project_name, index_in_db, max_rate):
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
    num_rated = imc.database.get_table_element(project_name, 'number_categoried',
                                     'image_index=%d'%index_in_db)
    user_result = imc.database.get_table_element(project_name, username,
                                     'image_index=%d'%index_in_db)
    user_result = user_result[0][0]

    while num_rated[0][0] >= max_rate or user_result != '':
        index_in_db += 1
        num_rated = imc.database.get_table_element(project_name, 'number_categoried',
                                         'image_index=%d'%index_in_db)
        user_result = imc.database.get_table_element(project_name, username,
                                         'image_index=%d'%index_in_db)
        user_result = user_result[0][0]

    imc.get_image_from_database(index_in_db)
    url = imc.current_image.image_url
    index = imc.current_index
    return json.dumps((url,index))

if __name__== "__main__":
    print get_next_image_url(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
