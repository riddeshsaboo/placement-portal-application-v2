from datetime import datetime
from extentions import db

class User(db.Model) :
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'company', 'student', name='user_roles'), nullable=False, default='student')
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(100), nullable = False)
    industry = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(150), nullable = False)
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    approval_status = db.Column(db.Enum('pending','approved','blacklisted','rejected',name='company_status'), nullable=False, default='pending')
    user = db.relationship("User", backref="company", uselist=False)

class Student(db.Model):
    __tablename__ = 'students' 
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable = False)
    cgpa = db.Column(db.Float, nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text, nullable = False)
    experience = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    user = db.relationship("User", backref="student", uselist=False)

class PlacementDrive(db.Model):    
    __tablename__ = "placement_drives"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    salary = db.Column(db.Float)
    skills_required = db.Column(db.Text)
    min_cgpa = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum("pending","approved","closed",name='drive_status'),nullable=False,default="pending")
    company = db.relationship("Company", backref="placement_drives")
    job_location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    deadline = db.Column(db.Date, nullable=False)
    vacancies = db.Column(db.Integer, nullable=False)

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    placement_drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    status = db.Column(db.Enum("applied","shortlisted","interview_scheduled","selected","rejected","placed",name="application_status"), nullable=False, default="applied")
    feedback = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.now)
    student = db.relationship("Student",backref="applications")
    placement_drive = db.relationship("PlacementDrive",backref="applications")

    # To Prevent duplicate applications:
    # One Student + One Drive = One Application
    # Validation handled in application route.


class Placement(db.Model):
    __tablename__ = "placements"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    position = db.Column( db.String(100), nullable=False)
    salary = db.Column(db.Float)
    joining_date = db.Column(db.Date)
    placed_at = db.Column(db.DateTime,default=datetime.now)
    student = db.relationship("Student",backref="placements")
    company = db.relationship("Company", backref="placements")