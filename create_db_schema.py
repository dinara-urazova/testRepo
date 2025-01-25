import sqlite3
connection = sqlite3.connect("users.db") # создание БД (если к ней) + подключение к ней

cursor = connection.cursor() # enables traversal over the records in a database

sql_create_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT, 
    password TEXT)
"""

cursor.execute(sql_create_table)

connection.close()