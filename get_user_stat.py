#!/usr/bin/env python
from core.sg2_users import user as u
from core.database.sg2_database_utils import image_database
import numpy as np
import datetime
import json
import sys
import get_config as gc
cf = gc.get_config('config.dat')
db = image_database(**cf['sg2'])

def get_statistics(user_name, time_unit):
    now = datetime.datetime.now()
    if time_unit == 'day':
        x = range(-23,1)
        times = [now+datetime.timedelta(hours=float(h)) for h in x]
        xlabels = [t.strftime('%I %p') for t in times]
    elif time_unit == 'week':
        x = range(-6,1)
        times = [now+datetime.timedelta(days=float(d)) for d in x]
        xlabels = [t.strftime('%a %d %b %Y') for t in times]
    elif time_unit == 'year':
        x = range(-51,1)
        day_week = now.weekday()
        monday = now+datetime.timedelta(days=-float(day_week))
        week_start = datetime.datetime(monday.year, monday.month, monday.day)
        times = [week_start+datetime.timedelta(days=float(w)*7) for w in x]
        times.append(now)
        xlabels = [''] * len(times)
        current_month = times[0].month
        for ii, t in enumerate(times):
            if t.month != current_month:
                xlabels[ii] = t.strftime('%b %Y')
                current_month = t.month
    user = u.USER(user_name)
    y = []
    for ii in range(len(times)-1):
        result = db.get_rate_time('sg2_image_rate', user_name, times[ii], times[ii+1] )
        y.append(len(result))
    return json.dumps((y, xlabels))


if __name__== "__main__":
    username = sys.argv[1]
    timeu = sys.argv[2]
    print get_statistics(username,timeu)
