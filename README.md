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
- [] PostgreSQL  - будем использовать "голые" запросы к БД при помощи pg8000 https://github.com/tlocke/pg8000/
- [] SQL ALchemy (diffieculties with config and connection issues)