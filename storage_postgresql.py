from postgresql_singleton import PostgreSQLSingleton
from werkzeug.security import check_password_hash
from typing import NamedTuple


class UserData(NamedTuple):
    id: int
    login: str
    password: str


class UserStoragePostgreSQL:

    def create_user(self, login, hashed_password) -> None:
        """
        пояснения по синтаксису 
        вставить в колонки Значения (через : передаются именованные параметры в sql-запросе), далее 
        login (именованный параметр) = login (фактическое значение, кот передается в аргументеь при вызове метода create_user)

        """
        PostgreSQLSingleton.getConnection().run(
            "INSERT INTO users (login, password) VALUES (:login, :hashed_password)",
            login=login,
            hashed_password=hashed_password,
        )

    def find_or_verify_user(self, username: str, password: str) -> UserData | None:
        """
        where login (from db) = :login (именов параметр), благодаря login (именов параметр)= username (фактич значение) на место :login подставляется фактич значение username 
        """
        result = PostgreSQLSingleton.getConnection().run(
            "SELECT id, login, password FROM users WHERE login = :login",
            login=username,
        )
        if result:
            user_id, login, hashed_password = result[0]
            if password is not None:
                if check_password_hash(hashed_password, password):
                    return UserData(user_id, login, hashed_password)
                return None  # неправильный пароль
            return UserData(
                user_id, login, hashed_password
            )  # пользователь найден, пароль не нужен
        return None  # пользователь не найден


class SessionData(NamedTuple):
    id: int
    uuid: str
    username: str


class SessionStoragePostgreSQL:

    def create_session(self, user_uuid: str, username: str) -> None:  # when logging in
        PostgreSQLSingleton.getConnection().run(
            "INSERT INTO sessions (user_uuid, username) VALUES (:user_uuid, :username)",
            user_uuid=user_uuid,
            username=username,
        )

    def find_session(self, user_uuid: str) -> None | SessionData:
        result = PostgreSQLSingleton.getConnection().run(
            "SELECT id, user_uuid as uuid, username FROM sessions WHERE user_uuid = :user_uuid",
            user_uuid=user_uuid,
        )
        if result:
            return SessionData(result[0][0], result[0][1], result[0][2])
        return None

    def delete_session(self, user_uuid: str) -> None:
        PostgreSQLSingleton.getConnection().run(
            "DELETE FROM sessions WHERE user_uuid = :user_uuid", user_uuid=user_uuid
        )
