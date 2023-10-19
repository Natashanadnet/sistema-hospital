from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "site.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .routes import routes, page_not_found

    app.register_blueprint(routes, url_prefix="/")
    app.register_error_handler(404, page_not_found)

    from .models import Paciente, Signos

    with app.app_context():
        db.create_all()

    return app
