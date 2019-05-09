from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_babel import Babel, lazy_gettext as _l
from config import config


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = _l("Silahkan login untuk mengakses halaman")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
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

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config["LANGUAGES"])

    return app

