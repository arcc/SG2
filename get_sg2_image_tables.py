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

db = image_database(password='root')

def get_sg2_img_tables(table_prefix):
    tables = db.get_tables()
    sg2_tables = []
    for tn in tables:
        if tn.startswith(table_prefix):
            sg2_tables.append(tn)
    return sg2_tables

if __name__== "__main__":
    prefix = sys.argv[1]
    print get_sg2_img_tables(prefix)
