from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json
import sys

def plot_statistics_bar(user_name, time_unit):
    fig_info = {'day': ((15,9), 0.35, 'Daily'),
                'week': ((12,9), 0.5, 'Weekly'),
                'year':((17,9), 0.5,'Yearly')}
    db = image_database(password='root')
    user = u.USER('luojing')
    time_bin_unit = user.time_unit_type[time_unit][1]
    x,y,tu = user.get_user_statistics(user_name, time_unit)
    now = datetime.datetime.now()
    if time_unit == 'day':
        times = [now+datetime.timedelta(hours=h) for h in x]
        xlabels = [t.strftime('%I\n%p') for t in times]
    elif time_unit == 'week':
        times = [now+datetime.timedelta(days=d) for d in x]
        xlabels = [t.strftime('%a \n%d %b \n%Y') for t in times]
    elif time_unit == 'year':
        times = [now+datetime.timedelta(days=w*7) for w in x]
        xlabels = [''] * len(times)
        current_month = times[0].month
        for ii, t in enumerate(times):
            if t.month != current_month:
                xlabels[ii] = t.strftime('%b \n%Y')
                current_month = t.month

    # Plot
    finfo = fig_info[time_unit]
    plt.figure(figsize=finfo[0])
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    plt.xticks(fontsize=14)
    ind = np.arange(len(x))
    width = finfo[1]
    rects1 = ax.bar(ind+ width/2, y, width, color="#3F5D7D")
    ax.set_ylabel('Number of image categoried')
    ax.set_title(finfo[2] + ' image category report for '+ username + '.', position=(0.45,1.05))
    ax.set_xticks(ind + width)
    ax.set_xticklabels(xlabels)
    autolabel(rects1, ax)
    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="on", right="off", labelleft="on")
    plt.savefig("bar_"+ time_unit + "_" +username + ".png", bbox_inches="tight")

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height + 0.05,
                '%d' % int(height),
                ha='center', va='bottom')

if __name__== "__main__":
    username = sys.argv[1]
    timeu = sys.argv[2]
    plot_statistics_bar(username,timeu)
    print "ok"
