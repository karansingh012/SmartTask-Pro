import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from .db import init_db, db
from .routes import register_blueprints
from .utils.logger import setup_logging
from .socketio import socketio


login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    return User.query.get(int(user_id))


def create_app(config_object=None):
    load_dotenv()

    app = Flask(__name__, template_folder="templates", static_folder="static")
    config_path = config_object or os.getenv(
        "FLASK_CONFIG", "config.DevelopmentConfig"
    )
    app.config.from_object(config_path)

    setup_logging(app)

    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="threading",
    )

    register_blueprints(app)
    init_db(app)
    login_manager.init_app(app)

    # Import models before creating tables
    from .models import User, Task

    with app.app_context():
        db.create_all()

    app.logger.info("SmartTask application initialized")
    return app
