#!/usr/bin/python
"""
"""
from core.sg2_category import sg2_category as sg2c
from core.database.users_database_utils import users_database

db = users_database(password='root')
db.create_statistics_tables()
