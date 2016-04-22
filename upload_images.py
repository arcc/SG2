#!/usr/bin/python
"""
This is a python script to upload images to the database
each uploaded file is on project for sg2 image category.
useage: python upload_images.py filename maximum_rating
"""
from core.database.users_database_utils import users_database
from core.database.sg2_database_utils import image_database
import sys
import os
import datetime
import get_config as gc
cf = gc.get_config('config.dat')
#Author Jing Luo

imgdb = image_database(**cf['sg2'])

if __name__== "__main__":
    filename = sys.argv[1]
    max_rate = int(sys.argv[2])
    base = os.path.basename(filename)
    project = base.split('.')[0]
    # Check if project has been added.
    exist_projects = imgdb.get_table_column_data('projects',['project_name',])[0]
    # Get the exist projects to a list.
    if exist_projects != []:
        for p in exist_projects:
            exsp = p[0]
        if project in exsp:
            raise ValueError("Project %s is already in the database, file %s has "
                             "been uploaded to database "% (project, filename))

    # Get image_info database last image index
    exist_last_image = imgdb.get_table_last_row('sg2_image_info', 'image_index', colname='image_index')
    if exist_last_image == []:
        last_image_index = 0
    else:
        last_image_index = exist_last_image[0][0]

    project_start_index = last_image_index + 1
    colnames = ['image_ID', 'mission']
    imgdb.load_image_list_file('sg2_image_info', filename, ' ', '\n', colnames)
    imgdb.cnx.commit()
    project_end_index = imgdb.get_table_last_row('sg2_image_info', 'image_index', colname='image_index')[0][0]
    # update project table
    number_image_add = project_end_index - project_start_index + 1
    now = datetime.datetime.now()
    imgdb.add_row('projects', {'project_name': project, 'number_image': number_image_add,
                               'start_image_index': project_start_index,
                               'end_image_index': project_end_index,
                               'time_added': now})
    # Put project name in sg2_image_info
    condition = "image_index >= %d AND image_index <= %d"%(project_start_index, project_end_index)
    imgdb.update_element('sg2_image_info', 'project', condition, project)
    imgdb.update_element('sg2_image_info', 'max_rate', condition, max_rate)
    imgdb.update_element('sg2_image_info', 'time_added', condition, now)
    imgdb.cnx.commit()
    # Add rows to sg2_image_rate table
    up_loads = imgdb.get_table_element('sg2_image_info', 'image_ID, image_index',condition)
    ids = [ud[0] for ud in up_loads]
    idxs = [ud[1] for ud in up_loads]
    values = []
    for idx, im_id in zip(idxs, ids):
        values += [(im_id, idx)]* max_rate
    imgdb.add_rows('sg2_image_rate',('image_ID','info_table_index'), values)
    imgdb.cnx.commit()
    imgdb.cnx.close()
    print "ok"
