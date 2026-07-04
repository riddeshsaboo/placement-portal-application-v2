import os

from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import * 
from datetime import datetime
import uuid

student = Blueprint("student", __name__)

@student.route('/student/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404
    
    total_applications = Application.query.filter_by(student_id = student.id).count()
    applied = Application.query.filter_by(student_id = student.id, status = 'applied').count()
    shortlisted = Application.query.filter_by(student_id = student.id, status = 'shortlisted').count()
    interview_scheduled = Application.query.filter_by(student_id = student.id, status = 'interview_scheduled').count()
    selected = Application.query.filter_by(student_id = student.id, status = 'selected').count()
    placed = Application.query.filter_by(student_id = student.id, status = 'placed').count()
    rejected = Application.query.filter_by(student_id = student.id, status = 'rejected').count()

    return {
        "student" : {
            "id" : student.id ,
            "full_name" : student.full_name
        },
        "total_applications" : total_applications,
        "applied" : applied,
        "shortlisted" : shortlisted,
        "interview_scheduled" : interview_scheduled,
        "selected" : selected,
        "placed" : placed,
        "rejected" : rejected
    }, 200

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
            "vacancies": posting.vacancies,
            "skills_required": posting.skills_required 
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
    if application : 
        already_applied = True 
        applied_at = application.applied_at
        application_id = application.id
    else : 
        already_applied = False 
        applied_at = None
        application_id = None
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
        "already_applied": already_applied,
        "applied_at": applied_at,
        "application_id": application_id,
        "student_resume": student.resume_path
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
    
    if not student.resume_path : 
        return {"message": "Please upload resume in your profile to apply a job"}, 400

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
    
    posting = application.placement_drive
    vacancies = posting.vacancies 
    filled_vacancies = Application.query.filter_by(placement_drive_id = posting.id, status = 'placed').count()

    if vacancies <= filled_vacancies : 
        application.status = 'rejected'
        application.feedback = "Application auto rejected since vacancies were full"
        db.session.commit()
        return {"message" : "All vacancies are full, cannot be placed, auto rejecting the applicatin"}, 400

    
    application.status = 'placed'
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

@student.route("/student/application/<int:application_id>", methods=["GET"])
@jwt_required()
def get_application(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404

    application = Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404

    posting = application.placement_drive
    if application.student_id != student.id:
        return {"message":"Unauthorized"},403

    company = (Company.query.filter_by(id = posting.company_id)).first()
    if not company : 
        return {"message":"Company not found"},404

    return {
        "id":application.id,
        "status":application.status,
        "feedback":application.feedback,
        "applied_at":application.applied_at,
        "interview_datetime":application.interview_datetime,
        "meeting_link":application.meeting_link,
        "offer_letter_path":application.offer_letter_path,
        "joining_date": application.joining_date,
        "student":{
            "id":student.id,
            "name":student.full_name,
            "email":student.user.email,
            "branch":student.branch,
            "cgpa":student.cgpa,
            "contact":student.contact,
            "resume":student.resume_path
        },
        "job":{
            "id":posting.id,
            "title":posting.title
        },
        "company": {
            "id": company.id,
            "company_name": company.company_name,
            "industry" : company.industry,
            "location" : company.location,
            "website": company.website,
            "description": company.description
        }

    },200


@student.route('/student/profile', methods=['GET'])
@jwt_required()
def profile():
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404
    
    applications = Application.query.filter_by(student_id = student.id).count()
    
    return {
        "id" : student.id ,
        "full_name" : student.full_name ,  
        "cgpa" : student.cgpa ,
        "branch" : student.branch ,
        "education" : student.education ,
        "skills" : student.skills ,
        "experience" : student.experience ,
        "resume_path" : student.resume_path ,
        "contact" : student.contact,
        "applications" : applications,
        "github_url" : student.github_url,
        "linkedin_url" : student.linkedin_url
    }, 200


@student.route('/student/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    jwt_data = get_jwt()
    if jwt_data["role"] != "student":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404
    
    # data = request.get_json()
    # if not data :
    #     return {"message": "Data not found"}, 404
    applications = Application.query.filter_by(student_id = student.id).count()

    try:
        if applications == 0 : 
            cgpa = request.form.get("cgpa")
            branch = request.form.get("branch")
            education = request.form.get("education")
            skills = request.form.get("skills")
            experience = request.form.get("experience")
            resume = request.files.get("resume") or None
            contact = request.form.get("contact")
            github_url = request.form.get("github_url")
            linkedin_url = request.form.get("linkedin_url")

            student.cgpa = cgpa 
            student.branch = branch 
            student.education = education
            student.skills = skills 
            student.experience = experience
            student.contact = contact
            student.github_url = github_url
            student.linkedin_url = linkedin_url 

            if resume : 
                # Delete old resume if it exists
                if student.resume_path:
                    old_resume = os.path.join("uploads", "resume", student.resume_path)
                    if os.path.exists(old_resume):
                        os.remove(old_resume)

                unique_id = uuid.uuid4()
                filename = f"Resume_{student.id}__{unique_id}.pdf"
                os.makedirs("uploads/offer_letters", exist_ok=True)
                path = os.path.join("uploads","offer_letters",filename)
                resume.save(path)
                student.resume_path = filename

            db.session.commit()
            return {"message": "Profile updated successfully"}, 200

        else :
            skills = request.form.get("skills")
            experience = request.form.get("experience")
            resume = request.files.get("resume") or None
            contact = request.form.get("contact")
            github_url = request.form.get("github_url")
            linkedin_url = request.form.get("linkedin_url")

            student.skills = skills 
            student.experience = experience
            student.contact = contact
            student.github_url = github_url
            student.linkedin_url = linkedin_url 

            if resume : 
                # Delete old resume if it exists
                if student.resume_path:
                    old_resume = os.path.join("uploads", "resume", student.resume_path)
                    if os.path.exists(old_resume):
                        os.remove(old_resume)

                unique_id = uuid.uuid4()
                filename = f"Resume_{student.id}__{unique_id}.pdf"
                os.makedirs("uploads/resume", exist_ok=True)
                path = os.path.join("uploads","resume",filename)
                resume.save(path)
                student.resume_path = filename
            
            db.session.commit()
            return {"message": "Profile updated successfully"}, 200
    except:
        return {"message": "Something went wrong"}, 500


@student.route("/student/resume")
@jwt_required()
def download_resume():
    jwt_data=get_jwt()
    if jwt_data["role"]!="student":
        return {"message":"Access denied"},403
    
    user_id=get_jwt_identity()
    student=Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404
    
    if not student.resume_path:
        return {"message":"Resume not found"},404
    
    return send_from_directory(os.path.join("uploads","resume"),student.resume_path,as_attachment=True)


@student.route("/student/application/<int:application_id>/offer_letter")
@jwt_required()
def download_offer_letter(application_id):
    jwt_data=get_jwt()
    if jwt_data["role"]!="student":
        return {"message":"Access denied"},403
    
    user_id=get_jwt_identity()
    student=Student.query.filter_by(user_id=user_id).first()
    if not student:
        return {"message":"Student not found"},404
    
    application=Application.query.filter_by(id=application_id,student_id=student.id).first()
    if not application:
        return {"message":"Application not found"},404
    
    if not application.offer_letter_path:
        return {"message":"Offer letter not found"},404
    
    return send_from_directory(os.path.join("uploads","offer_letters"),application.offer_letter_path,as_attachment=True)