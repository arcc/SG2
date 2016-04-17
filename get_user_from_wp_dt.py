from core.database.users_database_utils import users_database
from core.sg2_users import user as u
import get_config as gc
cf = gc.get_config('config.dat')

#Author Jing Luo

db = users_database(**cf['wordpress'])
db.import_user_from_wp_users('user_statistics_day')
db.import_user_from_wp_users('user_statistics_week')
db.import_user_from_wp_users('user_statistics_year')
db.import_user_from_wp_users('user_last_index')
db.cnx.commit()
