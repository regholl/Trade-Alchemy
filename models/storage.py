import sqlite3
from sqlite3 import Error

def db_connection(db_name):
	con = sqlite3.connect(f'data/{db_name}.db')
	cur = con.cursor()
	return cur

