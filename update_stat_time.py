from core.sg2_category import sg2_category as sg2c
from core.database.sg2_database_utils import image_database
from core.database.users_database_utils import users_database as udb
import datetime
import json
import sys
mport get_config as gc

cf = gc.get_config('config.dat')
user_db = udb(user=cf['user_db_usr'], password=cf['user_db_pw'])
def update_stat_time(time_unit):
    time_indentifier = {'week':('user_statistics_week','days', 1.0),
                        'day':('user_statistics_day','seconds', 3600.0),
                        'year':('user_statistics_year','days', 7.0)}
    now = datetime.datetime.now()
    last_update = user_db.get_last_update_time()
    stattablename = time_indentifier[time_unit][0]
    time_diff = now - last_update[stattablename]
    time_diff_unit = getattr(time_diff, time_indentifier[time_unit][1]) / time_indentifier[time_unit][2]
    time_blocks = int(time_diff_unit)
    user_db.update_statistics_time_column(time_indentifier[time_unit][0], time_blocks=time_blocks)
    user_db.update_element('statistics_table_status', 'last_update_time',
                           "table_name='%s'"%stattablename, now.strftime('%Y-%m-%d %H:%M:%S'))
    user_db.cnx.commit()
    return json.dumps("ok")
if __name__== "__main__":
    timeunit = sys.argv[1]
    timeunit = timeunit.lower()
    print update_stat_time(timeunit)
