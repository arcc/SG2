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
    users_result = user_db.get_table_element('wp_users', 'user_login, display_name', "user_activation_key=''")
    result = []
    for user in users_result:
        if user[0]=='':
            continue
        db_result = img_db.get_rate_time('sg2_image_rate', user[0], time_start, now)
        display_name = user[1].split()
        if len(display_name)<2:
            display_name.append('')
        first_name = display_name[0]
        last_name = display_name[1]
        result.append((user[0], display_name[0], display_name[1], len(db_result)))
    result_sort = sorted(result, key = lambda x: (x[1], x[2]))
    return json.dumps((result_sort, time_start.strftime('%a %d %b %Y %I %p'), now.strftime('%a %d %b %Y %I %p')))

if __name__== "__main__":
    timeu = sys.argv[1]
    print get_user_stat(timeu)
