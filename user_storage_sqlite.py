
from user import User
from sqlite_singleton import SQLiteSingleton
from werkzeug.security import generate_password_hash, check_password_hash


class UserStorageSQLite:

    def create_user(self, username: str, password: str) -> int:
        connection = SQLiteSingleton.getConnection()
        with connection:
            cursor = SQLiteSingleton.getConnection().cursor()
            hashed_password = generate_password_hash(password)
            cursor.execute(
                """
                INSERT INTO users (login, password) VALUES (?, ?)
                """,
                    (username, hashed_password)
            )
        return cursor.lastrowid
    
    def user_exists(self, username: str) -> bool:
        connection = SQLiteSingleton.getConnection()
        with connection:
            cursor = SQLiteSingleton.getConnection().cursor()
            result = cursor.execute("SELECT COUNT(*) FROM users WHERE login = ?", (username,))
            count = result.fetchone()[0]
            return count > 0
        
    
    def verify_user(self, username: str, password) -> bool:
        connection = SQLiteSingleton.getConnection()
        with connection:
            cursor = SQLiteSingleton.getConnection().cursor()
            result = cursor.execute("SELECT password FROM users WHERE login = ?", (username,))
            row = result.fetchone()
            if row:
                db_pwd = row[0]
                if check_password_hash(db_pwd, password):
                    return True
            return False

    


