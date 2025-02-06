import pg8000.native
import os
from dotenv import load_dotenv
from config import Config

load_dotenv() # загружает перем окружения из файла .env

db_name = Config.POSTGRESQL_DATABASE
db_user = Config.POSTGRESQL_USERNAME
db_password = Config.POSTGRESQL_PASSWORD
db_host = Config.POSTGRESQL_HOSTNAME
db_port = Config.POSTGRESQL_PORT

connection = pg8000.native.Connection(user=db_user, password=db_password, database=db_name, host=db_host, port=int(db_port)) # устанавливает соединение с БД

sql_create_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login TEXT UNIQUE NOT NULL, 
    password TEXT)
"""

connection.run(sql_create_table)


connection.close()
