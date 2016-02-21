# This is a test file for sg2_category
from sg2_category import image_category
from ..database.sg2_database_utils import image_database
from ..sg2_users.user import USER

user1 = USER('user1')

db = image_database(password='root')

imc = image_category( db, user1, 'sg2_category_test')


if not imc.check_data_table('sg2_category_test'):
    #print imc.check_data_table('sg2_category_test')
    imc.create_data_table('sg2_category_test')

imc.change_data_table('sg2_category_test')

#img_list_file = '/Users/jingluo/Research_codes/sg2/database/test_upload.dat'
#imc.database.load_image_list_file(imc.data_table, img_list_file, ' ', '\n',
#                                  ['image_ID', 'mission']) # Put this as a function
#imc.create_new_user_column()
imc.get_image_from_database(5)
print imc.current_img_status
print imc.current_index
print imc.current_image
print imc.current_user_result

imc.user_input(11)

imc.set_quailty_control(imc.current_image.image_id, True)
imc.database.cnx.commit()
imc.database.display_database_info('SELECT * FROM %s'%imc.data_table)
