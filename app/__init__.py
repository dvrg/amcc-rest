from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from config import config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .admin import admin as admin_blueprint
    from .api import api as api_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app

