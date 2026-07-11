import os
from extentions import cache
from flask import Blueprint, request, send_file, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from models import * 
from datetime import datetime
from werkzeug.utils import secure_filename
import pdfplumber
import re


company = Blueprint("company", __name__)

@company.route("/company/addjobposting", methods=["POST"])
@jwt_required()
def addjobposting():
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message": "Access denied"}, 403

    data = request.get_json()
    if not data:
        return {"message": "No data provided"}, 400

    title = data.get("title")
    description = data.get("description") or None
    salary = data.get("salary") or None
    skills_required = data.get("skills_required") or None
    min_cgpa = data.get("min_cgpa") or None 
    job_location = data.get("job_location") or None
    deadline = data.get("deadline")
    vacancies = data.get("vacancies")

    if not title or not deadline or vacancies is None:
        return {"message": "Required fields missing"}, 400

    if int(vacancies) < 1:
        return {"message": "Vacancies must be at least 1"}, 400

    if min_cgpa is not None:
        min_cgpa = float(min_cgpa)
        if min_cgpa < 0 or min_cgpa > 10:
            return {"message": "Invalid CGPA"}, 400

    deadline = datetime.strptime(deadline,"%Y-%m-%dT%H:%M")

    if deadline <= datetime.now():
        return {"message": "Deadline must be in future"}, 400

    user_id = jwt_data["user_id"]

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message": "Company not found"}, 404

    job_posting = PlacementDrive(
        company_id=company.id,
        title=title,
        description=description,
        salary=salary,
        skills_required=skills_required,
        min_cgpa=min_cgpa,
        job_location=job_location,
        deadline=deadline,
        vacancies=vacancies,
        status="pending"
    )

    db.session.add(job_posting)
    db.session.commit()
    cache.clear()

    return {"message": "Job posting created successfully"}, 201


@company.route("/company/dashboard/<int:company_id>", methods=["GET"])
@jwt_required()
@cache.memoize()
def company_dashboard(company_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"}, 403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id, id=company_id).first()

    if not company:
        return {"message":"Company not found"}, 404
    
    company_name = company.company_name
    # print(company_name)
    total_job_postings = PlacementDrive.query.filter_by(company_id=company.id).count()
    active_job_postings = PlacementDrive.query.filter_by(company_id=company.id, status='approved').count()
    pending_job_postings = PlacementDrive.query.filter_by(company_id=company.id, status='pending').count()
    closed_job_postings = PlacementDrive.query.filter_by(company_id=company.id, status='closed').count()
    selected_candidates = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id,Application.status == "selected").count()
    interview_scheduled_candidates = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id,Application.status == "interview_scheduled").count()
    received_applications = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id).count()
    shortlisted_candidates = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id,Application.status == "shortlisted").count()
    placed_candidates = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id,Application.status == "placed").count()
    rejected_candidates = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id,Application.status == "rejected").count()
    # print(total_job_postings)
    return {
        "company_name": company_name,
        "total_job_postings": total_job_postings,
        "active_job_postings": active_job_postings,
        "received_applications": received_applications,
        "pending_job_postings": pending_job_postings,
        "closed_job_postings": closed_job_postings,
        "shortlisted_candidates": shortlisted_candidates,
        "selected_candidates": selected_candidates, 
        "interview_scheduled_candidates": interview_scheduled_candidates,
        "placed_candidates" : placed_candidates,
        "rejected_candidates" : rejected_candidates
    }, 200

@company.route("/company/job_postings/<int:company_id>", methods=['GET'])
@jwt_required()
@cache.memoize()
def get_job_postings(company_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message": "Access denied"}, 403
    
    user_id = get_jwt_identity()   
    company = Company.query.filter_by(user_id=user_id, id=company_id).first()
    if not company:
        return {"message":"Company not found"}, 404
    
    postings = PlacementDrive.query.filter_by(company_id=company.id).all()
    result = []

    for posting in postings:
        result.append({
            "id": posting.id,
            "title": posting.title,
            "salary": posting.salary,
            "min_cgpa": posting.min_cgpa, 
            "skills_required": posting.skills_required, 
            "vacancies": posting.vacancies,
            "created_at": posting.created_at, 
            "deadline": posting.deadline, 
            "status": posting.status,
            "applications":  Application.query.filter_by(placement_drive_id=posting.id).count()
        })

    return result, 200 

@company.route("/company/job_posting/<int:posting_id>/status", methods=["PUT"])
@jwt_required()
def update_job_posting_status(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message": "Access denied"}, 403
    
    user_id = get_jwt_identity()   
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"}, 404

    data = request.get_json()
    status = data.get("status")

    if status != "closed" : 
        return {"message" : "Unauthorised"}, 400

    posting = PlacementDrive.query.filter_by(id=posting_id).first()
    if not posting:
        return {"message": "Job posting not found"}, 404
    
    if posting.company_id != company.id : 
        return {"message" : "Unauthorised"}, 403

    posting.status = status
    db.session.commit()
    cache.clear()

    return {"message": "Status updated"}, 200

@company.route("/company/job_posting/<int:posting_id>", methods=["GET"])
@jwt_required()
def manage_job(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message": "Access denied"}, 403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return {"message": "Company not found"}, 404

    posting = PlacementDrive.query.filter_by(id=posting_id,company_id=company.id).first()

    if not posting:
        return {"message": "Job posting not found"}, 404

    return {
        "id": posting.id,
        "title": posting.title,
        "description": posting.description,
        "salary": posting.salary,
        "skills_required": posting.skills_required,
        "min_cgpa": posting.min_cgpa,
        "job_location": posting.job_location,
        "vacancies": posting.vacancies,
        "created_at": posting.created_at,
        "deadline": posting.deadline,
        "status": posting.status
    }, 200


@company.route("/company/job_posting/<int:posting_id>/applications", methods=["GET"])
@jwt_required()
@cache.memoize()
def get_applications(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"}, 403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return {"message":"Company not found"}, 404

    posting = PlacementDrive.query.filter_by(id=posting_id,company_id=company.id).first()
    if not posting:
        return {"message":"Job posting not found"}, 404

    applications = Application.query.filter_by( placement_drive_id=posting.id).all()

    result = []

    for application in applications:
        student = application.student
        result.append({
            "id": application.id,
            "student_name": student.full_name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "applied_at": application.applied_at,
            "status": application.status
        })

    return result, 200

@company.route("/company/job_posting/<int:posting_id>", methods=["PUT"])
@jwt_required()
def editjobposting(posting_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message": "Access denied"}, 403

    data = request.get_json()
    if not data:
        return {"message": "No data provided"}, 400

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return {"message":"Company not found"}, 404
    
    jobPosting = PlacementDrive.query.filter_by(id = posting_id, company_id = company.id).first()
    if not jobPosting :
        return {"message": "Job Posting not found"}, 404
    
    if jobPosting.status == "closed":
        return {"message":"Closed job postings cannot be edited"}, 400
    
    title = data.get("title")
    description = data.get("description") or None
    salary = data.get("salary") or None
    skills_required = data.get("skills_required") or None
    min_cgpa = data.get("min_cgpa") or None 
    job_location = data.get("job_location") or None
    deadline = data.get("deadline")
    vacancies = data.get("vacancies")

    placed_applications = Application.query.filter_by(placement_drive_id = jobPosting.id, status="placed").count()
    total_applications = Application.query.filter_by(placement_drive_id = jobPosting.id).count()

    if total_applications != 0 and jobPosting.status == "approved" :
        return {"message": "Editing not allowed for job postings with one or more applications"}, 400
        
    if not title:
        return {"message":"Title is required"},400
    
    if vacancies is None:
        return {"message":"Vacancies are required"},400

    vacancies = int(vacancies)
    if vacancies < max(placed_applications,1) :
        return {"message": "Vacancies must be greater than number of students placed or 1 whichever is greater"}, 400
    
    if min_cgpa == "":
        min_cgpa = None
    if min_cgpa is not None:
        min_cgpa = float(min_cgpa)
        if min_cgpa < 0 or min_cgpa > 10:
            return {"message": "Invalid CGPA"}, 400

    deadline = datetime.strptime(deadline,"%Y-%m-%dT%H:%M")

    if deadline <= datetime.now():
        return {"message": "Deadline must be in future"}, 400

    jobPosting.title = title 
    jobPosting.description = description
    jobPosting.salary = salary
    jobPosting.skills_required = skills_required
    jobPosting.min_cgpa = min_cgpa
    jobPosting.job_location = job_location
    jobPosting.deadline = deadline
    jobPosting.vacancies = vacancies      

    db.session.commit()
    cache.clear()

    return {"message": "Job posting updated successfully"}, 200


@company.route("/company/application/<int:application_id>", methods=["GET"])
@jwt_required()
def get_application(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    application = Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404

    posting = application.placement_drive
    if posting.company_id != company.id:
        return {"message":"Unauthorized"},403

    student = application.student

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
        }

    },200


@company.route("/company/application/<int:application_id>/shortlist", methods = ['PUT'])
@jwt_required()
def shortlist(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    application = Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404

    posting = application.placement_drive
    if posting.company_id != company.id:
        return {"message":"Unauthorized"},403
    
    #to ensure the sequencial flow applied -> shortlist/rejected -> interview_scheduled/rejected -> selected/rejected -> placed/rejected
    if application.status != 'applied' :  
        return {"message" : "Invalid request"}, 400
    
    data = request.get_json()
    feedback = data.get("feedback") or None 

    # print(feedback)

    application.feedback = feedback
    application.status = 'shortlisted'
    db.session.commit() 
    cache.clear()

    return {"message" : "Candidate Shortlisted successfully"}, 200

@company.route("/company/application/<int:application_id>/reject", methods = ['PUT'])
@jwt_required()
def reject(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    application = Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404

    posting = application.placement_drive
    if posting.company_id != company.id:
        return {"message":"Unauthorized"},403
    
    #to ensure the sequencial flow applied -> shortlist/rejected -> interview_scheduled/rejected -> selected/rejected -> placed/rejected
    if application.status in ["rejected", "placed"] : 
        return {"message" : "Invalid request"}, 400
    
    data = request.get_json()
    feedback = data.get("feedback") or None 

    # print(feedback)
    
    application.feedback = feedback
    application.status = 'rejected'
    db.session.commit() 
    cache.clear()

    return {"message" : "Candidate rejected successfully"}, 200

@company.route("/company/application/<int:application_id>/interview_scheduled", methods = ['PUT'])
@jwt_required()
def interview_scheduled(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403
    
    data = request.get_json()
    if not data:
        return {"message": "No data provided"}, 400

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    application = Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404

    posting = application.placement_drive
    if posting.company_id != company.id:
        return {"message":"Unauthorized"},403
    
    #to ensure the sequencial flow applied -> shortlist/rejected -> interview_scheduled/rejected -> selected/rejected -> placed/rejected
    if application.status != 'shortlisted' :  
        return {"message" : "Invalid request"}, 400
    
    interview_datetime = data.get("interview_datetime")
    meeting_link = data.get("meeting_link")
    feedback = data.get("feedback")

    interview_datetime = datetime.strptime(interview_datetime,"%Y-%m-%dT%H:%M")

    if not interview_datetime or not meeting_link : 
        return {"message" : "Required fields missing"}, 400
    
    if interview_datetime <= datetime.now():
        return {"message": "Interview must be in future"}, 400
    
    application.feedback = feedback
    application.interview_datetime = interview_datetime
    application.meeting_link = meeting_link
    application.status = 'interview_scheduled'
    db.session.commit() 
    cache.clear()

    return {"message" : "Inteview Scheduled for Candidate successfully"}, 200

@company.route("/company/application/<int:application_id>/select", methods = ['PUT'])
@jwt_required()
def select(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    application = Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404

    posting = application.placement_drive
    if posting.company_id != company.id:
        return {"message":"Unauthorized"},403
    
    #to ensure the sequencial flow applied -> shortlist/rejected -> interview_scheduled/rejected -> selected/rejected -> placed/rejected
    if application.status != 'interview_scheduled' :  
        return {"message" : "Invalid request"}, 400
    
    offer_letter = request.files.get("offer_letter")
    joining_date = request.form.get("joining_date")
    feedback = request.form.get("feedback")
    if not offer_letter:
        return {"message":"Offer letter required"},400
    if not joining_date:
        return {"message":"Joining date required"},400
    if not feedback:
        return {"message":"Feedback required"},400
    
    vacancies = posting.vacancies 
    # print(vacancies)
    filled_vacancies = Application.query.filter_by(placement_drive_id = posting.id, status = 'placed').count()
    # print(filled_vacancies)

    if vacancies <= filled_vacancies : 
        return {"message" : "All vacancies full, cannot shortlist"}, 400
    
    filename = f"Offer_{application.id}_{secure_filename(offer_letter.filename)}"
    os.makedirs("uploads/offer_letters", exist_ok=True)
    path = os.path.join("uploads","offer_letters",filename)

    offer_letter.save(path)

    application.offer_letter_path = filename
    application.joining_date = datetime.strptime(joining_date,"%Y-%m-%dT%H:%M").date()
    application.feedback = feedback
    application.status = "selected"
    db.session.commit() 
    cache.clear()

    return {"message" : "Candidate Selected successfully"}, 200

# After being selected its the candidate's call to accept the placement offer or not (first come first serve - as vacancies are limited)


@company.route("/company/student/<int:student_id>/resume")
@jwt_required()
def download_resume(student_id):
    jwt_data=get_jwt()
    if jwt_data["role"]!="company":
        return {"message":"Access denied"},403
    
    user_id=get_jwt_identity()
    company=Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404
    
    student=Student.query.get(student_id)
    if not student:
        return {"message":"Student not found"},404
    
    application=Application.query.join(PlacementDrive).filter(Application.student_id==student.id,PlacementDrive.company_id==company.id).first()
    if not application:
        return {"message":"Unauthorized"},403
    
    if not student.resume_path:
        return {"message":"Resume not found"},404
    
    return send_from_directory(os.path.join("uploads","resume"),student.resume_path,as_attachment=True)

@company.route("/company/application/<int:application_id>/offer_letter")
@jwt_required()
def download_offer_letter(application_id):
    jwt_data=get_jwt()
    if jwt_data["role"]!="company":
        return {"message":"Access denied"},403
    
    user_id=get_jwt_identity()
    company=Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404
    
    application=Application.query.get(application_id)
    if not application:
        return {"message":"Application not found"},404
    
    if application.placement_drive.company_id != company.id:
        return {"message":"Unauthorized"},403
    
    if not application.offer_letter_path:
        return {"message":"Offer letter not found"},404
    
    return send_from_directory(os.path.join("uploads","offer_letters"),application.offer_letter_path,as_attachment=True)

@company.route("/company/export", methods=["POST"])
@jwt_required()
def export_csv():
    from tasks import export_company_applications

    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404
    
    placementDrives = PlacementDrive.query.filter_by(company_id = company.id).all()
    
    # Student Name
    # Job Title
    # Application Status
    # Applied On
    # Joining Date

    rows = []
    for posting in placementDrives:

        applications = Application.query.filter_by(placement_drive_id = posting.id).all()
        for application in applications:
            rows.append({
                "Student Name": application.student.full_name,
                "Job Title": application.placement_drive.title,
                "Application Status": application.status,
                "Applied On": str(application.applied_at),
                "Joining Date": str(application.joining_date)
            })
    task = export_company_applications.delay(company.id, rows)

    return {
        "message":"CSV export started successfully",
        "task_id": task.id
    },200

@company.route("/company/export/download", methods=["GET"])
@jwt_required()
def download_export():
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403

    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    filename = f"company_{company.id}_applications.csv"
    path = os.path.join("exports/company", filename)
    if not os.path.exists(path):
        return {"message":"Export not found"},404

    return send_file(path, as_attachment=True)


@company.route("/company/resume_screener/<int:application_id>", methods=["POST"])
@jwt_required()
def resume_screener(application_id):
    jwt_data = get_jwt()
    if jwt_data["role"] != "company":
        return {"message":"Access denied"},403
    
    user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"message":"Company not found"},404

    application = Application.query.filter_by(id = application_id).first()
    if not application:
        return {"message":"Application not found"},404
    
    if application.placement_drive.company_id != company.id :
        return {"message": "Unauthorized"}, 403

    student = application.student
    drive = application.placement_drive
    # resume_path = f"/uploads/resume/{student.resume_path}"
    resume_path = os.path.join("uploads","resume",student.resume_path)
    skills_required = drive.skills_required.lower().split(",")
    text = ""

    with pdfplumber.open(resume_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.lower()

    matched = []
    missing = []

    for skill in skills_required:
        skill = skill.strip()
        if re.search(r"\b"+re.escape(skill)+r"\b",text):
            matched.append(skill)
        else:
            missing.append(skill)

    # score = int(len(matched)/len(skills_required)*100)

    # return {
    #     "ats_score":score,
    #     "matched_skills":matched,
    #     "missing_skills":missing
    # },200

    required_skills = [x.strip().lower() for x in drive.skills_required.split(",")]

    skill_map={
    "python":["python","python3"],
    "html":["html","html5"],
    "css":["css","css3"],
    "javascript":["javascript","js"],
    "vue":["vue","vuejs"],
    "react":["react","reactjs"],
    "node":["node","nodejs"],
    "git":["git","github"],
    "software development":["software development","developer","development","developing"],
    "django":["django"],
    "flask":["flask"],
    "orm":["orm"]
    }

    matched=[]
    missing=[]

    for skill in required_skills:
        if any(keyword in text for keyword in skill_map.get(skill,[skill])):
            matched.append(skill)
        else:
            missing.append(skill)

    score=int(len(matched)/len(required_skills)*100)

    recommendation="Poor Match"

    if score>=80:
        recommendation="Excellent Match"
    elif score>=60:
        recommendation="Good Match"
    elif score>=40:
        recommendation="Moderate Match"

    return{
        "resume_score":score,
        "recommendation":recommendation,
        "matched_skills":matched,
        "missing_skills":missing
    },200
