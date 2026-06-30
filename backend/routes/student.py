from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import * 
from datetime import datetime


student = Blueprint("student", __name__)

@student.route("/student/job_postings", methods=["GET"])
@jwt_required()
def get_job_postings():
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    postings = PlacementDrive.query.filter(PlacementDrive.status == "approved",PlacementDrive.deadline > datetime.now()).all()
    result = []
    for posting in postings:
        company = Company.query.get(posting.company_id)
        result.append({
            "id": posting.id,
            "company_name": company.company_name,
            "title": posting.title,
            "salary": posting.salary,
            "min_cgpa": posting.min_cgpa,
            "deadline": posting.deadline,
            "vacancies": posting.vacancies
        })

    return result,200

@student.route("/student/job_posting/<int:posting_id>", methods=["GET"])
@jwt_required()
def get_job_posting(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    posting = PlacementDrive.query.filter_by(id=posting_id,status="approved").first()
    if not posting:
        return {"message":"Job posting not found"},404

    company = Company.query.get(posting.company_id)
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()

    application = Application.query.filter_by(student_id=student.id,placement_drive_id=posting.id).first()

    return {
        "id":posting.id,
        "company_name":company.company_name,
        "title":posting.title,
        "description":posting.description,
        "salary":posting.salary,
        "skills_required":posting.skills_required,
        "min_cgpa":posting.min_cgpa,
        "job_location":posting.job_location,
        "vacancies":posting.vacancies,
        "deadline":posting.deadline,
        "already_applied": application is not None
    },200


@student.route("/student/job_posting/<int:posting_id>/apply", methods=["POST"])
@jwt_required()
def apply_job(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404

    posting = PlacementDrive.query.filter_by(id=posting_id,status="approved").first()
    if not posting:
        return {"message":"Job posting not found"},404

    if posting.deadline <= datetime.now():
        return {"message":"Application deadline has passed"},400

    existing = Application.query.filter_by(student_id=student.id,placement_drive_id=posting.id).first()
    if existing:
        return {"message":"Already applied"},400

    application = Application(student_id=student.id,placement_drive_id=posting.id,status="applied")
    db.session.add(application)
    db.session.commit()
    return {"message":"Application submitted successfully"},201


@student.route("/student/applications", methods=["GET"])
@jwt_required()
def get_student_applications():
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404

    applications = Application.query.filter_by(student_id=student.id).all()
    result = []

    for application in applications:
        posting = PlacementDrive.query.get(application.placement_drive_id)
        company = Company.query.get(posting.company_id)
        result.append({
            "id":application.id,
            "company_name":company.company_name,
            "title":posting.title,
            "status":application.status,
            "applied_at":application.applied_at
        })

    return result,200


@student.route("/student/application/<int:application_id>/accept", methods=["PUT"])
@jwt_required()
def accept_offer(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404

    application = Application.query.filter_by(id=application_id, student_id=student.id).first()
    if not application : 
        return {"message": "Application not found"}, 404
    
    if application.status != 'selected' : 
        return {"message": "Invalid request"}, 400
    
    application.status = 'placed'
    posting = application.placement_drive
    placement = Placement(
        student_id=student.id,
        company_id=posting.company_id,
        position=posting.title,
        salary=posting.salary,
        joining_date=application.joining_date
    )

    db.session.add(placement)

    placed_count = Application.query.filter_by(placement_drive_id=posting.id,status="placed").count()
    if placed_count >= posting.vacancies:
        posting.status = "closed"

    other_applications = Application.query.filter(Application.student_id == student.id,Application.id != application.id,Application.status.in_(["applied","shortlisted","interview_scheduled", "selected"])).all()
    for application in other_applications:
        application.status = "rejected"
        application.feedback = "Application closed automatically as the student accepted another placement offer."

    db.session.commit()
    return {"message": "Offer accepted successfully"}, 200

@student.route("/student/application/<int:application_id>/reject", methods=["PUT"])
@jwt_required()
def reject_offer(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404

    application = Application.query.filter_by(id=application_id, student_id=student.id).first()
    if not application : 
        return {"message": "Application not found"}, 404
    
    if application.status != 'selected' : 
        return {"message": "Invalid request"}, 400
    
    application.status = 'rejected'
    application.feedback = 'Offer rejected by the Candidate'

    db.session.commit()
    return {"message": "Offer rejected successfully"}, 200