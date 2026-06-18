from flask import Flask
from extentions import db
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@gmail.com").first()
    if not admin:
        admin = User(
            email="admin@gmail.com",
            password="admin@123",
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