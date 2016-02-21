#!/usr/bin/python
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys

db = image_database(password='root')

def get_img_from_id(username, project_name, img_id):
    user = u.USER(username)
    imc = sg2c.image_category( db, user, project_name)
    imc.change_data_table(project_name)
    #TODO write a function in sg2_category to get image form img_id
    return 0
