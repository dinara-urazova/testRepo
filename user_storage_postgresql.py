from user import User
from postgresql_singleton import PostgreSQLSingleton
from werkzeug.security import generate_password_hash, check_password_hash

class UserStoragePostgreSQL:
    def create_user(self, login, hashed_password) -> None:
        user = PostgreSQLSingleton.getConnection().run(
            f"""
            INSERT INTO users (login, password) VALUES ($1, $1)
                ('{login}', 
                '{hashed_password}')
        """
        )
        print('😍',user)
    

    def user_exists(self, username: str) -> bool:
        result = PostgreSQLSingleton.getConnection().run("SELECT COUNT(*) FROM users WHERE login = $1", (username,))
        count = result[0][0]
        print(count, '🇸🇮')
        return count > 0
    

    def verify_user(self, username: str, password) -> bool:
        result = PostgreSQLSingleton.getConnection().run("SELECT password FROM users WHERE login = $1", (username,))
        row = result[0]
        if row:
            db_pwd = row[0]
            if check_password_hash(db_pwd, password):
                return True
        return False

    



