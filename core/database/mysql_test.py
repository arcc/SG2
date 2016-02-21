import mysql.connector

cnx = mysql.connector.connect(user='root', password='root',
                              host='localhost', port='8889',
                              unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
                              database='sg2image')
cnx.close()
