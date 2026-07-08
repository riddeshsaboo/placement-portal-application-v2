from flask import Flask
from extentions import db, mail
from models import *
from routes.company import company
from routes.auth import auth
from routes.admin import admin
from routes.student import student
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
from flask_cors import CORS
import config


def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY

    app.config["MAIL_SERVER"] = config.MAIL_SERVER
    app.config["MAIL_PORT"] = config.MAIL_PORT
    app.config["MAIL_USE_TLS"] = config.MAIL_USE_TLS
    app.config["MAIL_USE_SSL"] = config.MAIL_USE_SSL
    app.config["MAIL_USERNAME"] = config.MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = config.MAIL_PASSWORD
    app.config["MAIL_DEFAULT_SENDER"] = config.MAIL_DEFAULT_SENDER

    db.init_app(app)
    mail.init_app(app)

    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(company)
    app.register_blueprint(student)

    with app.app_context():
        db.create_all()
        Admin = User.query.filter_by(email="admin@gmail.com").first()
        if not Admin:
            hashed_pwd = generate_password_hash("admin@123")
            Admin = User(
                email="admin@gmail.com",
                password=hashed_pwd,
                role="admin"
            )
            db.session.add(Admin)
            db.session.commit()

    @app.route("/")
    def home():
        return "Placement Portal App is Running"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)