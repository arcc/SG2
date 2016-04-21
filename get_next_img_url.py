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
import get_config as gc
cf = gc.get_config('config.dat')


db = image_database(**cf['sg2'])
def get_next_image_url(username, index_in_db, project_name=''):
    """This is a wrapper funciton for sg2 category php
    Parameter
    ----------
    username : str
        The user name who is categorating sg2 image
    index_in_db : int
        The image index in database
    projcet_name : str
        The projcet name, which project you want to select
    Return
    -----------
    JSON dump image url and image index in database
    """
    index_in_db = int(index_in_db)
    user = u.USER(username)
    imc = sg2c.image_category( db, user, project_name)
    img_table = 'sg2_image_info'
    rate_table = 'sg2_image_rate'
    total_img = imc.database.get_total_num_image(img_table)

    if index_in_db > total_img:
        return json.dumps(('-1', '-1', index_in_db))
    if index_in_db == 0:
        index_in_db = 1

    under_rate_image = imc.database.get_table_element(img_table, 'image_index, project, image_ID, '
                        'number_rated, max_rate', 'number_rated<max_rate AND image_index>=%d'%index_in_db)
    if under_rate_image ==[]:
        return json.dumps(('-1', '-1', '-1',index_in_db))

    condition = ("SELECT image_index FROM %s WHERE number_rated<max_rate and"
                 " image_index>=%d")%(img_table, index_in_db)

    user_rated = imc.database.get_table_element(rate_table, 'info_table_index, image_ID',
                        "rater_name='%s' and info_table_index IN (%s)"%(username, condition))
    rated = set()
    under_rated = set()
    for ur in user_rated:
        rated.add(ur[0])

    for unimg in under_rate_image:
        under_rated.add(unimg[0])

    usr_unrate = under_rated.symmetric_difference(rated)
    print rated
    print under_rated
    print usr_unrate
    if list(usr_unrate) == []:
        return json.dumps(('-1', '-1', '-1',index_in_db))
    target_index = min(list(usr_unrate))
    #result_image_index = imc.database.get_table_element(img_table, 'image_index', "image_ID='%s'"%target_id)[0][0]
    imc.get_image_from_database(index=target_index)
    url = imc.current_image.image_url
    url_large = imc.current_image.image_url_large
    url_page = imc.current_image.page_url
    return json.dumps((url, url_large, url_page, target_index))

if __name__== "__main__":
    username = sys.argv[1]
    img_index = int(sys.argv[2])
    if len(sys.argv) >= 4:
        project_name = sys.argv[3]
        print get_next_image_url(username, img_index, project_name)
    else:
        print get_next_image_url(username, img_index)
