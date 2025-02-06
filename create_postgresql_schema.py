import pg8000.native
from dotenv import load_dotenv
from config import Config

load_dotenv()  # загружает перем окружения из файла .env

db_name = Config.POSTGRESQL_DATABASE
db_user = Config.POSTGRESQL_USERNAME
db_password = Config.POSTGRESQL_PASSWORD
db_host = Config.POSTGRESQL_HOSTNAME
db_port = Config.POSTGRESQL_PORT

connection = pg8000.native.Connection(
    user=db_user,
    password=db_password,
    database=db_name,
    host=db_host,
    port=int(db_port),
)  # устанавливает соединение с БД

sql_create_table_sessions = """
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(36) UNIQUE NOT NULL, 
    username VARCHAR(25) NOT NULL
)
"""

connection.run(sql_create_table_sessions)


sql_create_table_users = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(25) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL
)
"""

connection.run(sql_create_table_users)


connection.close()
