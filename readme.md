# Placement Portal V2

A full-stack Placement Management System developed using **Vue.js**, **Flask**, **SQLite**, **Redis**, **Celery**, **JWT Authentication**, and **Chart.js**.

The application provides dedicated portals for **Students**, **Companies**, and **Administrators**, enabling efficient campus placement management with secure authentication, background task processing, analytics, caching, and ATS-style resume screening.

---

## Features

### Authentication & Authorization

- JWT Authentication
- Role-Based Access Control
- Student Registration
- Company Registration
- Secure Password Hashing
- Company Approval Workflow
- Company Login Approval Validation

---

## Student Portal

- Student Dashboard
- Update Profile
- Upload Resume (PDF)
- Browse Approved Placement Drives
- View Placement Drive Details
- Resume Match Analysis before Applying
- Apply for Placement Drives
- Track Application Status
- View Placement Details
- Download Offer Letter

---

## Company Portal

- Company Dashboard
- Create Placement Drives
- Edit Placement Drives
- Close Placement Drives
- View Applications
- View Student Profiles
- Download Student Resumes
- Resume Match Analysis
- Shortlist Candidates
- Schedule Interviews
- Reject Applications
- Select Candidates
- Provide Candidate Feedback
- Export Applications as CSV

---

## Administrator Portal

- Admin Dashboard
- Manage Students
- Manage Companies
- Approve / Reject Company Registrations
- Blacklist / Activate Students
- Blacklist / Activate Companies
- Monitor Placement Drives
- Monitor Applications
- Trigger Monthly Reports
- Trigger Interview Reminder Emails

---

## ATS Resume Screening

The ATS Resume Screening module can be used by both Students and Companies.

Features include:

- Resume Match Score
- Recommendation
- Matched Skills
- Missing Skills
- PDF Resume Parsing using pdfplumber

---

## Reports & Analytics

- Chart.js Dashboard Analytics
- Public Landing Dashboard
- Placement Statistics
- Student & Company Analytics
- CSV Export
- Monthly Placement Reports

---

## Background Tasks

Implemented using **Celery** and **Redis**.

- Monthly Placement Reports
- Interview Reminder Emails
- CSV Export Tasks
- Scheduled Background Jobs

---

## Redis Caching

Implemented using Flask-Caching.

Cached APIs include:

- Admin Dashboard
- Student Dashboard
- Company Dashboard
- Public Dashboard
- Placement Drive Listings
- Application Listings

Automatic cache invalidation is performed after database updates.

---

## Email Services

Implemented using Flask-Mail.

- Company Registration Notifications
- Interview Reminder Emails
- Monthly Placement Reports

---

## Technology Stack

### Frontend

- Vue.js
- Vue Router
- Axios
- Bootstrap 5
- Chart.js

### Backend

- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Mail
- Flask-Caching
- Celery
- Redis

### Database

- SQLite

---

## Project Structure

```
placement-portal-v2/
│
├── backend/
│   ├── routes/
│   ├── uploads/
│   ├── reports/
│   ├── exports/
│   ├── app.py
│   ├── models.py
│   ├── celery_app.py
│   ├── tasks.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│
└── README.md
```

---

## Installation

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python app.py
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

### Redis

```bash
redis-server
```

---

### Celery Worker

```bash
celery -A celery_app.celery worker --loglevel=info
```

---

### Celery Beat

```bash
celery -A celery_app.celery beat --loglevel=info
```

---

## Future Enhancements

- Progressive Web App (PWA)
- AI-Based Resume Recommendations
- Multi-College Support
- SMS Notifications
- Advanced Resume Parsing

---

## Developed By

**Riddesh Saboo**

**Modern Application Development II Project May 2026 term**

**IIT Madras - BS Degree in Data Science and Applications**