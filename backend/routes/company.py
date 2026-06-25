from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from models import * 
from datetime import datetime


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

    return {"message": "Job posting created successfully"}, 201