from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt

admin = Blueprint("admin", __name__)

@admin.route("/admin/test")
@jwt_required()
def admin_test():

    jwt = get_jwt()

    if jwt["role"] != "admin":
        return {"message": "Access denied"}, 403

    return {
        "message": "Welcome Admin"
    }