#!/usr/bin/env python
from core.sg2_users import user as u
from core.database.sg2_database_utils import image_database
from core.database.users_database_utils import users_database
import numpy as np
import datetime
import json
import sys
import get_config as gc
cf = gc.get_config('config.dat')
img_db = image_database(**cf['sg2'])
user_db = users_database(**cf['wordpress'])

def get_user_stat(time_unit):
    now = datetime.datetime.now()
    # setup time stemp
    if time_unit == 'day':
        time_start = ndatetime.datetime(now.year, now.month, now.day, now.hour-1)
    elif time_unit == 'week':
        time_start = datetime.datetime(now.year, now.month, now.day)+ datetime.timedelta(days=float(-7))
    elif time_unit == 'month':
        time_start = datetime.datetime(now.year, now.month - 1, now.day)
    elif time_unit == 'year':
        time_start = datetime.datetime(now.year - 1, now.month, now.day)
    else:
        raise ValueError("Unknow time unit.")
    # setup user list
    users_result = user_db.get_table_element('wp_users', 'user_login', "user_activation_key=''")
    result = {}
    for user in users_result:
        if user[0]=='':
            continue
        db_result = img_db.get_rate_time('sg2_image_rate', user[0], time_start, now)
        result[user[0]] = len(db_result)
    print json.dumps((result, time_start.strftime('%a %d %b %Y %I %p'), now.strftime('%a %d %b %Y %I %p')))

if __name__== "__main__":
    timeu = sys.argv[1]
    print get_user_stat(timeu)
