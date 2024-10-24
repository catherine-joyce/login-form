from wtforms import StringField, PasswordField, validators
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired(
        message="Username should not be empty.")])
    password = PasswordField('Password', [validators.InputRequired(
        message="Password should not be empty.")])
    
class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired(
        message="Username should not be empty.")])
    password = PasswordField('Password', [validators.InputRequired(
        message="Password should not be empty.")])
