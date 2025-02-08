from flask import Flask, make_response, flash, request, render_template, redirect, abort
from user import User
from forms import LoginForm, RegisterForm
import uuid

from postgresql_singleton import PostgreSQLSingleton
from werkzeug.security import generate_password_hash, check_password_hash
from storage_postgresql import UserStoragePostgreSQL, SessionStoragePostgreSQL
from http import HTTPStatus
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

COOKIE_NAME = "session"

user_storage = UserStoragePostgreSQL()
session_storage = SessionStoragePostgreSQL()


@app.route("/", methods=["GET"])
def root():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if session_storage.find_session(user_uuid):
        return redirect("/secret")
    return render_template("base.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if session_storage.find_session(user_uuid):
        return redirect("/secret")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if user_storage.find_or_verify_user(
            username, password=None
        ):  # проверить, существует ли пользователь (без проверки пароля)
            flash("You are already registered, try to log in")
        else:  # пользователь не найден, нужно создать нового
            hashed_password = generate_password_hash(password)
            user_storage.create_user(username, hashed_password)
            flash("You have successfully registered")
            return redirect("/login")

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if session_storage.find_session(user_uuid):
        return redirect("/secret")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_data = user_storage.find_or_verify_user(
            username, password
        )  # поиск и проверка пользователя
        if user_data:
            user_uuid = str(uuid.uuid4())
            session_storage.create_session(user_uuid, username)
            r = make_response(redirect("/secret"))
            r.set_cookie(COOKIE_NAME, user_uuid, path="/", max_age=60 * 60)
            return r

        flash("Invalid username or password")

    elif form.csrf_token.errors:
        abort(HTTPStatus.FORBIDDEN.value)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if session_storage.find_session(user_uuid):
        session_storage.delete_session(user_uuid)  # delete on server

        r = make_response(redirect("/"))
        r.set_cookie(COOKIE_NAME, user_uuid, path="/", max_age=0)  # delete in browser
        return r
    return redirect("/")


@app.route("/secret", methods=["GET"])
def secret():
    user_uuid = request.cookies.get(COOKIE_NAME)
    session_data = session_storage.find_session(user_uuid)
    if session_data:
        user = session_data.username
        r = make_response(render_template("secret.html", user=user.title()))
        r.set_cookie(COOKIE_NAME, user_uuid, path="/", max_age=60 * 60)
        return r
    return abort(HTTPStatus.UNAUTHORIZED.value)
