from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.sg2_users import user as u
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json
import sys

def plot_statistics_line(user_name, time_unit):
    fig_info = {'day': ((15,9), 0.35, 'Daily'),
                'week': ((12,9), 0.5, 'Weekly'),
                'year':((20,9), 0.5,'Yearly')}
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
    color = np.array([31, 119, 180])/225.0
    finfo = fig_info[time_unit]
    plt.figure(figsize=finfo[0])
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    plt.tick_params(axis="both", which="both", bottom="on", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")
    plt.xticks(fontsize=14)
    ymax = max(y)
    yline = np.linspace(0,ymax + (5-ymax % 5), 5)
    for yl in yline:
        plt.plot(range(len(y)), [yl] * len(range(len(y))), "--", lw=0.5, color="black", alpha=0.3)

    plt.plot(y,lw=2.5, color=color)
    ax.set_ylabel('Number of image categoried')
    ax.set_title(finfo[2] + ' image category report for '+ username + '.', position=(0.45,1.05))
    ax.set_xticks(range(len(y)))
    ax.set_xticklabels(xlabels)
    #autolabel(rects1, ax)
    plt.savefig("line_"+ time_unit + '_' + username + ".png", bbox_inches="tight")

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
    plot_statistics_line(username,timeu)
    print "ok"
