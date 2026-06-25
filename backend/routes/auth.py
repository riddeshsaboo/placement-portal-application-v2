from flask import Blueprint,request
from models import * 
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required

auth = Blueprint("auth", __name__)

@auth.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json() 

    if not data : 
        return {"message" : "No data provided"}, 400

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    full_name = data.get("full_name")
    cgpa = data.get("cgpa")
    branch = data.get("branch")
    contact = data.get("contact")
    education = data.get("education")
    skills = data.get("skills")
    experience = data.get("experience")

    if (not email or not password or not full_name or not branch or not education or not skills or cgpa is None or not contact):
        return {"message": "Required fields missing"}, 400
    
    if cgpa < 0 or cgpa > 10:
        return {"message": "Invalid CGPA"}, 400 

    existing_user = User.query.filter_by(email=email).first() 
    if(existing_user):
        return {"message": "Email already exists"}, 400
    
    hashed_password = generate_password_hash(password)

    user = User(email = email, password = hashed_password, role = 'student')
    db.session.add(user)
    db.session.commit()

    student = Student(
        user_id = user.id, full_name = full_name, cgpa = cgpa, branch = branch, contact = contact ,education = education, skills = skills, experience = experience
    )
    db.session.add(student)
    db.session.commit()

    return {"message" : "Student registered successfully"}, 201

    

@auth.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json() 

    if not data : 
        return {"message" : "No data provided"}, 400

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    company_name = data.get("company_name")
    location = data.get("location")
    industry = data.get("industry")
    website = (data.get("website") or None) 
    description = (data.get("description") or None) 

    if (not email or not password or not company_name or not location or not industry ):
        return {"message": "Required fields missing"}, 400
    
    existing_user = User.query.filter_by(email=email).first() 
    if(existing_user):
        return {"message": "Email already exists"}, 400
    
    hashed_password = generate_password_hash(password)

    user = User(email = email, password = hashed_password, role = 'company')
    db.session.add(user)
    db.session.commit()

    company = Company(
        user_id = user.id, company_name = company_name, location = location, industry = industry, website = website, description = description
    )
    db.session.add(company)
    db.session.commit()

    return {"message" : "Company registered successfully"}, 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json() 

    if not data : 
        return {"message" : "No data provided"}, 400

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    
    if (not email or not password):
        return {"message": "Required fields missing"}, 400
    
    existing_user = User.query.filter_by(email=email).first() 
    if(not existing_user):
        return {"message": "No user exists with that email, please register"}, 400
    
    if check_password_hash(existing_user.password, password):
        if existing_user.role == "company":
            company = Company.query.filter_by(user_id=existing_user.id).first()
            if company.approval_status != "approved":
                if company.approval_status == "pending":
                    return {"message": "Company account pending approval, contact admin at admin@gmail.com"}, 403
                else : 
                    return {"message": f"Company account is {company.approval_status}, contact admin at admin@gmail.com"}, 403
            else : 
                token = create_access_token(identity=str(existing_user.id),additional_claims={"role": existing_user.role, "user_id": existing_user.id})
                return {"message": "Login success", "token": token, "role": existing_user.role}, 200
        else : 
            token = create_access_token(identity=str(existing_user.id),additional_claims={"role": existing_user.role, "user_id": existing_user.id})
            return {"message": "Login success", "token": token, "role": existing_user.role}, 200
    else : 
        return {"message": "Incorrect password"}, 400
    

# @auth.route("/protected")
# @jwt_required()
# def protected():
#     return {
#         "message": "Access Granted"
#     }