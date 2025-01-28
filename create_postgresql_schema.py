import pg8000.native

connection = pg8000.native.Connection("dinaraurazova")

sql_create_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    login TEXT, 
    password TEXT)
"""

connection.run(sql_create_table)


connection.close()