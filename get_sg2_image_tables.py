#!/usr/bin/python
"""
This is a python script for getting database project tables.
useage:
    $python get_sg2_image_table.py username project_name index_in_db
"""
from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import json
import sys
import argparse
mport get_config as gc

cf = gc.get_config('config.dat')
db = image_database(user=cf['img_db_usr'], password=cf['img_db_pw'])

def search_projects(keywd = ''):
    sg2_projects = db.get_table_column_data('projects', ['project_name',])[0]

    result = []
    for p in sg2_projects:
        if keywd in p[0]:
            result.append(p[0])
    return json.dumps(result)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description="SG2 search projects")
    parser.add_argument("-k",help="keywords for searching", default='')
    args = parser.parse_args()
    print search_projects(keywd=args.k)
