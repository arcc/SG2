from core.database.users_database_utils import users_database
from core.sg2_users import user as u


db = users_database(password='root')
db.import_user_from_wp_users('user_statistics_day')
db.import_user_from_wp_users('user_statistics_week')
db.import_user_from_wp_users('user_statistics_year')
