from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from models import * 

admin = Blueprint("admin", __name__)

@admin.route("/admin/dashboard", methods = ['GET'])
@jwt_required()
def dashboard():
    jwt_data = get_jwt()
    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403
    
    active_students = User.query.filter_by(role="student", is_active=True).count()
    active_companies = Company.query.filter_by(approval_status = "approved").count()
    active_job_postings = PlacementDrive.query.filter_by(status="approved").count()
    applicants_placed = Application.query.filter_by(status="placed").count()

    return {
        "total_students" : Student.query.count(),
        "active_students" : active_students, 
        "total_companies" : Company.query.count(),
        "active_companies" : active_companies,
        "total_job_postings" : PlacementDrive.query.count(),
        "active_job_postings" : active_job_postings , 
        "total_applications" : Application.query.count(),
        "applicants_placed" : applicants_placed
    }, 200


@admin.route("/admin/companies", methods=["GET"])
@jwt_required()
def get_companies():

    jwt_data = get_jwt()

    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403
    
    companies = Company.query.all()

    result = []

    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "approval_status": company.approval_status
        })

    return result, 200


@admin.route("/admin/company/<int:company_id>/status", methods=["PUT"])
@jwt_required()
def update_company_status(company_id):
    jwt_data = get_jwt()

    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403
    
    data = request.get_json()
    new_status = data.get("status")

    allowed_statuses = ["approved","rejected","blacklisted","pending"]

    if new_status not in allowed_statuses:
        return {"message": "Invalid status"}, 400

    company = Company.query.filter_by(id=company_id).first()

    if not company:
        return {"message": "Company not found"}, 404

    company.approval_status = new_status
    if(new_status in ['rejected','blacklisted']):
        company.user.is_active = False 
    else : 
        company.user.is_active = True 
    db.session.commit()

    return {"message": f"Company status changed to {new_status}"}, 200


@admin.route("/admin/students", methods=["GET"])
@jwt_required()
def get_students():
    jwt_data = get_jwt()

    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403
    
    students = Student.query.all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "full_name": student.full_name,
            "branch": student.branch,
            "contact": student.contact,
            "is_active": student.user.is_active
        })

    return result, 200

@admin.route("/admin/student/<int:student_id>/status", methods=["PUT"])
@jwt_required()
def update_student_status(student_id):
    jwt_data = get_jwt()

    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403
    
    data = request.get_json()
    new_status = data.get("status")

    allowed_statuses = [0,1]

    if new_status not in allowed_statuses:
        return {"message": "Invalid status"}, 400
    
    if new_status == 0 : 
        new_status = False
    else : 
        new_status = True 

    student = Student.query.filter_by(id=student_id).first()

    if not student:
        return {"message": "Student not found"}, 404

    student.user.is_active = new_status
    db.session.commit()

    print("Done")

    return {"message": f"Student status changed to {new_status}"}, 200


@admin.route("/admin/job_postings", methods=["GET"])
@jwt_required()
def get_job_postings():
    jwt_data = get_jwt()
    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403

    postings = PlacementDrive.query.all()
    result = []

    for posting in postings:
        result.append({
            "id": posting.id,
            "title": posting.title,
            "company_name": posting.company.company_name,
            "salary": posting.salary,
            "min_cgpa": posting.min_cgpa, 
            "skills_required": posting.skills_required, 
            "vacancies": posting.vacancies,
            "created_at": posting.created_at, 
            "deadline": posting.deadline, 
            "status": posting.status
        })

    return result, 200

@admin.route("/admin/job_posting/<int:posting_id>/status", methods=["PUT"])
@jwt_required()
def update_job_posting_status(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403

    data = request.get_json()
    status = data.get("status")

    posting = PlacementDrive.query.filter_by(id=posting_id).first()
    if not posting:
        return {"message": "Job posting not found"}, 404

    posting.status = status
    db.session.commit()

    return {"message": "Status updated"}, 200

@admin.route("/admin/applications", methods=["GET"])
@jwt_required()
def get_applications():
    jwt_data = get_jwt()
    if jwt_data["role"] != "admin":
        return {"message": "Access denied"}, 403

    applications = Application.query.all()
    result = []

    for application in applications:
        result.append({
            "id": application.id,
            "student_name": application.student.full_name,
            "company_name": application.placement_drive.company.company_name,
            "job_title": application.placement_drive.title,
            "status": application.status,
            "applied_at": application.applied_at
        })

    return result, 200