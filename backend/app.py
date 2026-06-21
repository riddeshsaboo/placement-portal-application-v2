from flask import Flask
from extentions import db
from models import *
from routes.auth import auth
from flask_jwt_extended import JWTManager
from routes.admin import admin

from werkzeug.security import generate_password_hash

from flask_cors import CORS



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "jwt_key"


app.register_blueprint(auth)
app.register_blueprint(admin)


db.init_app(app)

CORS(app)


jwt = JWTManager(app)

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@gmail.com").first()
    if not admin:
        hashed_pwd = generate_password_hash("admin@123")
        admin = User(
            email="admin@gmail.com",
            password=hashed_pwd,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created")

@app.route("/")
def home():
    return "Placement Portal App is Running"

if __name__ == "__main__":
    app.run(debug=True)