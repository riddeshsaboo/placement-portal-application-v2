from datetime import datetime, timedelta

from sqlalchemy import func
from extentions import mail
from flask_mail import Message
from celery_app import celery
import pandas as pd
import os
from extentions import db
from models import Application, Placement, PlacementDrive, Student, Company

@celery.task
def export_student_applications(student_id, rows):
    os.makedirs("exports/student", exist_ok=True)
    filename = f"student_{student_id}_applications.csv"
    df = pd.DataFrame(rows)
    df.to_csv(f"exports/student/{filename}", index=False)
    
    student = Student.query.get(student_id)

    msg = Message(subject="Placement Application Export Ready",recipients=['riddeshsaboo10@gmail.com'])  #student.user.email

    msg.body = f"""Hello {student.full_name},

    Your placement application export has been generated successfully.

    The CSV file is attached.

    Regards,

    Placement Portal

    """

    with open(f"exports/student/{filename}", "rb") as f:
        msg.attach(filename,"text/csv",f.read())

    mail.send(msg)

    return filename

@celery.task
def export_company_applications(company_id, rows):
    os.makedirs("exports/company", exist_ok=True)
    filename = f"company_{company_id}_applications.csv"
    df = pd.DataFrame(rows)
    df.to_csv(f"exports/company/{filename}", index=False)
    company = Company.query.get(company_id)

    msg = Message(subject="Placement Application Export Ready",recipients=['riddeshsaboo10@gmail.com'])  #company.user.email

    msg.body = f"""Hello {company.company_name},

    The application export has been generated successfully.

    The CSV file is attached.

    Regards,

    Placement Portal

    """

    with open(f"exports/company/{filename}", "rb") as f:
        msg.attach(filename,"text/csv",f.read())

    mail.send(msg)
    return filename

@celery.task
def send_interview_reminders():
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    applications = Application.query.filter_by(status="interview_scheduled").all()
    count = 0

    for application in applications:
        if application.interview_datetime is None:
            continue
        if application.interview_datetime.date() != tomorrow:
            continue
        msg = Message(
            subject="Interview Reminder",
            recipients=["riddeshsaboo10@gmail.com"]   #student.user.email
        )

        msg.body = f"""Hello {application.student.full_name},

                        Your interview is scheduled.

                        Company : {application.placement_drive.company.company_name}

                        Job : {application.placement_drive.title}

                        Interview :
                        {application.interview_datetime.strftime("%d/%m/%Y %I:%M %p")}

                        Best of Luck!
                    """

        mail.send(msg)
        count += 1

    return f"{count} mail(s) sent"

@celery.task
def generate_monthly_report(current_month = False):
    today = datetime.now()
    first_day_current_month = today.replace(day=1)
    if not current_month :
        last_day = first_day_current_month - timedelta(days=1)
        first_day = last_day.replace(day=1)
        month = last_day.strftime('%B_%Y')
    else :
        last_day = today
        first_day = first_day_current_month
        month = last_day.strftime('%B_%Y')

    placement_drives = PlacementDrive.query.filter(PlacementDrive.created_at >= first_day,PlacementDrive.created_at <= last_day).count()

    applications = Application.query.filter(Application.applied_at >= first_day,Application.applied_at <= last_day).count()

    selected = Application.query.filter(
        Application.status.in_(["selected", "placed"]),
        Application.applied_at >= first_day,
        Application.applied_at <= last_day
    ).count()

    students_placed = Placement.query.filter(
        Placement.placed_at >= first_day,
        Placement.placed_at <= last_day
    ).count()

    interviews = Application.query.filter(
        Application.status.in_(["interview_scheduled", "selected", "placed"]),
        Application.applied_at >= first_day,
        Application.applied_at <= last_day
    ).count()

    companies_participated = db.session.query(func.count(func.distinct(PlacementDrive.company_id))).filter(
        PlacementDrive.created_at >= first_day,
        PlacementDrive.created_at <= last_day
    ).scalar() or 0

    average_salary = db.session.query(func.avg(Placement.salary)).filter(
        Placement.placed_at >= first_day,
        Placement.placed_at <= last_day
    ).scalar()

    average_salary = round(average_salary or 0, 2)

    highest_salary = db.session.query(func.max(Placement.salary)).filter(
        Placement.placed_at >= first_day,
        Placement.placed_at <= last_day
    ).scalar()

    highest_salary = highest_salary or 0

    lowest_salary = db.session.query(func.min(Placement.salary)).filter(
        Placement.placed_at >= first_day,
        Placement.placed_at <= last_day
    ).scalar()

    lowest_salary = lowest_salary or 0

    html = f"""
            <html>
            <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet" />
            </head>
            <body>
            <h2 class="fw-bold bg-warning m-2 p-2 border border-dark" >Placement Portal Monthly Report for {month}</h2>
            <table class="table table-hover bg-tertiary" >
            <tr>
            <th>Metric</th>
            <th>Count</th>
            </tr>
            <tr>
            <td>Total Placement Drives</td>
            <td>{placement_drives}</td>
            </tr>
            <tr>
            <td>Total Applications</td>
            <td>{applications}</td>
            </tr>
            <tr>
            <td>Students Selected</td>
            <td>{selected}</td>
            </tr>
            <tr>
            <td>Students Placed</td>
            <td>{students_placed}</td>
            </tr>
            <tr>
            <td>Interview Scheduled</td>
            <td>{interviews}</td>
            </tr>
            <tr>
            <td>Companies Participated</td>
            <td>{companies_participated}</td>
            </tr>
            <tr>
            <td>Average Package(LPA)</td>
            <td>{average_salary}</td>
            </tr>
            <tr>
            <td>Highest Package(LPA)</td>
            <td>{highest_salary}</td>
            </tr>
            <tr>
            <td>Lowest Package(LPA)</td>
            <td>{lowest_salary}</td>
            </tr>
            </table>

            </body>

            </html>
    """

    os.makedirs("exports/reports", exist_ok=True)
    filename = f"Monthly_Report_{month}.html"
    filepath = os.path.join("exports", "reports", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    msg = Message(subject="Monthly Placement Report",recipients=["riddeshsaboo10@gmail.com"])   #admin's email
    msg.html = html

    with open(filepath, "rb") as f:
        msg.attach(filename,"text/html",f.read())

    mail.send(msg)

    return f"Report for {month} succesfully mailed to the admin"

