from user import User
from postgresql_singleton import PostgreSQLSingleton
from werkzeug.security import generate_password_hash, check_password_hash

class UserStoragePostgreSQL:
    def create_user(self, login, hashed_password) -> None:
        PostgreSQLSingleton.getConnection().run(
            "INSERT INTO users (login, password) VALUES (:login, :hashed_password)",
            login=login,
            hashed_password=hashed_password,
        )

    def user_exists(self, username: str) -> bool:
        result = PostgreSQLSingleton.getConnection().run(
            "SELECT COUNT(*) FROM users WHERE login = :login", login=username
        )
        count = result[0][0]
        return count > 0

    def verify_user(self, username: str, password) -> bool:
        result = PostgreSQLSingleton.getConnection().run(
            "SELECT password FROM users WHERE login = :login", login=username
        )
        row = result[0]
        if row:
            db_pwd = row[0]
            if check_password_hash(db_pwd, password):
                return True
        return False
