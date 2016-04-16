#!/usr/bin/env python
from core.sg2_category import sg2_category as sg2c
from core.sg2_users import user as u
import numpy as np
import datetime
import json
import sys

def get_statistics(user_name, time_unit):
    fig_info = {'day': ((15,9), 0.35, 'Daily'),
                'week': ((12,9), 0.5, 'Weekly'),
                'year':((17,9), 0.5,'Yearly')}
    user = u.USER(user_name)
    time_bin_unit = user.time_unit_type[time_unit][1]
    x,y,tu = user.get_user_statistics(user_name, time_unit)
    now = datetime.datetime.now()
    if time_unit == 'day':
        times = [now+datetime.timedelta(hours=float(h)) for h in x]
        xlabels = [t.strftime('%I %p') for t in times]
    elif time_unit == 'week':
        times = [now+datetime.timedelta(days=float(d)) for d in x]
        xlabels = [t.strftime('%a %d %b %Y') for t in times]
    elif time_unit == 'year':
        times = [now+datetime.timedelta(days=float(w)*7) for w in x]
        xlabels = [''] * len(times)
        current_month = times[0].month
        for ii, t in enumerate(times):
            if t.month != current_month:
                xlabels[ii] = t.strftime('%b %Y')
                current_month = t.month
    return json.dumps((y, xlabels))


if __name__== "__main__":
    username = sys.argv[1]
    timeu = sys.argv[2]
    print get_statistics(username,timeu)
