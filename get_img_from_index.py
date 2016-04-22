#!/usr/bin/python
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys
import get_config as gc
cf = gc.get_config('config.dat')

db = image_database(**cf['sg2'])

def serach_img_from_database_by_index(index):
    img_table = 'sg2_image_info'
    rate_table = 'sg2_image_rate'
    img_val = db.get_table_row(img_table, "image_index='%s'"%index)
    img_key = db.get_table_keys(img_table)
    image = {}
    for key, val in zip(img_key, img_val[0]):
        image[key[0]] = val
    return image

if __name__== "__main__":
    index = sys.argv[1]
    print serach_img_from_database_by_index(index)
