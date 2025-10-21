from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import getenv
from dotenv import load_dotenv

# Extensions
_db = SQLAlchemy()
_login_manager = LoginManager()


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    _db.init_app(app)
    _login_manager.init_app(app)
    _login_manager.login_view = "auth.login"

    # Blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        from . import models  # noqa: F401
        _db.create_all()

    return app

# Re-exports for use in other modules
db = _db  # type: ignore
login_manager = _login_manager  # type: ignore
