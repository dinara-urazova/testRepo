from flask import Flask, make_response, flash, request, render_template, redirect, abort
from user import User
from forms import LoginForm, RegisterForm
import uuid

from sqlite_singleton import SQLiteSingleton
from werkzeug.security import generate_password_hash, check_password_hash
from user_storage_sqlite import UserStorageSQLite
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

COOKIE_NAME = 'session'

session_memory_storage = {}
user_storage = UserStorageSQLite()

@app.route("/", methods=["GET"])
def root():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if user_uuid in session_memory_storage:
        return redirect("/secret")
    return render_template("base.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if user_uuid in session_memory_storage:
        return redirect("/secret")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if user_storage.user_exists(username):
            flash("You are already registered")
            return redirect('/login')
        else:
            user_storage.create_user(username, password)
            flash('You have successfully registered')
            return redirect("/login")
          

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if user_uuid in session_memory_storage:
        return redirect("/secret")
    
    form = LoginForm()
  
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if user_storage.verify_user(username, password):

            user_uuid = str(uuid.uuid4())
            session_memory_storage[user_uuid] = {'user': username}
            # e.g. {'1e7545e4-2b9e-4669-970e-263416114f18': {'user': 'Felix'}}
            r = make_response(redirect('/secret'))
            r.set_cookie(COOKIE_NAME, user_uuid, path="/", max_age=60*60)
            return r
        
        flash('Invalid username or password')
        return redirect('/')
    
    return render_template('login.html', title='Sign In', form=form)

@app.route("/logout", methods=["GET"])
def logout():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if user_uuid in session_memory_storage:
        del session_memory_storage[user_uuid] # delete on server

        r = make_response(redirect('/'))
        r.set_cookie(COOKIE_NAME, user_uuid, path="/", max_age=0) # delete in browser (no other way to delete cookie but to set max_age to negative/zero )
        return r
    return redirect('/')
    

@app.route("/secret", methods=["GET"])
def secret():
    user_uuid = request.cookies.get(COOKIE_NAME)
    if user_uuid in session_memory_storage:
        user = session_memory_storage[user_uuid]['user']
        return render_template('secret.html', user=user.title())
    return redirect('/')



    




    