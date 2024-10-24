import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='super_secret_key',
        DATABASE=os.path.join(app.instance_path, 'login_form.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.after_request
    def add_security_headers(resp):
        resp.headers['Content-Security-Policy']= "default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self';base-uri 'self';form-action 'self'; frame-ancestors 'none';"
        resp.headers['X-Content-Type-Options'] = 'nosniff'
        return resp

    return app