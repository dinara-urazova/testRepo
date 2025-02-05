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

class SessionStoragePostgreSQL: 

    def create_session(self, user_uuid: str, username: str) -> None: # when logging in
            PostgreSQLSingleton.getConnection().run(
            "INSERT INTO sessions (user_uuid, username) VALUES (:user_uuid, :username)",
            user_uuid=user_uuid,
            username=username,
        )
    
    def session_exists(self, user_uuid: str): # д возвращать true если сессия есть и false если сессии нет
        result = PostgreSQLSingleton.getConnection().run(
            "SELECT COUNT(*) FROM sessions WHERE user_uuid = :user_uuid", user_uuid=user_uuid
        )
        count = result[0][0]
        return count > 0
    
    def get_username(self, user_uuid: str) -> str:
        result = PostgreSQLSingleton.getConnection().run(
            "SELECT username FROM sessions WHERE user_uuid = :user_uuid", user_uuid=user_uuid
        )
        db_user = result[0][0]
        return db_user

    def delete_session(self, user_uuid: str) -> None:
        PostgreSQLSingleton.getConnection().run(
         "DELETE FROM sessions WHERE user_uuid = :user_uuid", user_uuid=user_uuid
        )