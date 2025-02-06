# Install project

To install project on a local machine run these commands:
```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
(venv) $ flask --debug --app app run
...работает сервер, ctrl + c для выхода
(venv) $ deactivate
```

or simply run this script:
```
$ ./install.sh
```

# Run project
```
$ ./run.sh
```

and then  open your browser.

# TODO
- [x] Сделать хранилище для списка пользователей на основании баз данных (самый простой вариант - БД SQLite)
- [x] SQLite
- [x] PostgreSQL  - будем использовать "голые" запросы к БД при помощи pg8000 https://github.com/tlocke/pg8000/
- [ ] Перенести storage из массива в БД (отдельная таблица в postgres)
session_storage, колонки - id, user_uuid(str), username
В модуле storage_postgres сделать ф-ции для созд-яб поиска и удаления сессии
Где исп-ся session_memory_storage - заменить на вызов storage_postgres
Проверить, что все раб-т Проверка - залог-ся, выкл сервер и снова вкл Сессия дб актуальной
- [ ] Перейти на flask инструменты по хранению сессий (flask session)