import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from login_form.forms import LoginForm, RegisterForm

from login_form.db import get_db
from login_form.user import User

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if not username:
            error = 'Username is required.'

        if error is None:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            User.create(username, hashed_password)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = User.find_by_username(username) 
        if user != None and bcrypt.check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('auth.index'))
        else:
            error = 'Incorrect username or password.'            

        flash(error)

    return render_template('login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.find_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view