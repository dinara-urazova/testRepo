from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=25, message="Username should be between 4-25 characters")])
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField("Sign In")
