import os
from datetime import date
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-development-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Войдите в аккаунт, чтобы выполнить это действие."
login_manager.login_message_category = "warning"

@app.context_processor
def inject_current_year():
    return {"current_year": date.today().year}

from app import models  # noqa: E402,F401
from app import routes  # noqa: E402,F401

with app.app_context():
    db.create_all()
