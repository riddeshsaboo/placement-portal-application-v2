# Placement Portal V2

A full-stack Placement Management System built using **Vue.js**, **Flask**, **SQLite**, **JWT Authentication**, **Celery**, **Redis**, **Chart.js**, and **Bootstrap**.

The system provides separate dashboards for **Students**, **Companies**, and **Administrators**, enabling complete campus placement management with analytics, background jobs, caching, and ATS-style resume screening.

---

# Features

## Authentication & Authorization

- JWT-based Authentication
- Role-based Access Control
- Student Registration
- Company Registration
- Admin Login
- Password Hashing
- Company Approval System
- Blacklist / Activate Students and Companies

---

# Student Features

- Student Dashboard
- Update Profile
- Upload Resume
- View Approved Placement Drives
- Apply for Placement Drives
- View Application History
- Track Application Status
- Resume Match Analysis before applying
- ATS-style Resume Screening
    - Resume Match Score
    - Recommendation
    - Matched Skills
    - Missing Skills

---

# Company Features

- Company Dashboard
- Create Placement Drives
- Edit Placement Drives
- Close Placement Drives
- View Applications
- Review Candidate Profiles
- Download Resume
- Shortlist Candidates
- Schedule Interviews
- Reject Candidates
- Select Candidates
- Provide Feedback
- ATS Resume Screening
    - Resume Match Score
    - Recommendation
    - Matched Skills
    - Missing Skills
- Export Applications (CSV)

---

# Admin Features

- Admin Dashboard
- Approve / Reject Companies
- Manage Students
- Manage Companies
- Manage Placement Drives
- Manage Applications
- Placement Statistics
- Manual Monthly Report Generation
- Manual Interview Reminder Trigger

---

# Analytics & Charts

Chart.js powered dashboards

- Admin Analytics Dashboard
- Company Analytics Dashboard
- Public Landing Page Analytics

Displays

- Students
- Companies
- Placement Drives
- Applications
- Placements

---

# Background Jobs

Implemented using Celery + Redis

- Monthly Placement Reports
- Interview Reminder Emails
- CSV Export
- Manual Job Triggers
- Scheduled Background Tasks

---

# ATS Resume Screening

Implemented using **pdfplumber**

Workflow

- Extract text from uploaded PDF resume
- Compare resume against required job skills
- Calculate Resume Match Score
- Display Recommendation
- Display Matched Skills
- Display Missing Skills

The ATS can be used by both Students and Companies.

---

# Reports

- Monthly HTML Placement Report
- Email Reports
- HTML Report Export
- CSV Export

---

# Redis Caching

Implemented using Flask-Caching + Redis

Cached APIs

- Admin Dashboard
- Company Dashboard
- Student Dashboard
- Public Dashboard
- Job Listings
- Company Applications

Automatic cache invalidation after updates.

---

# Email Features

Brevo SMTP Integration

- Registration Emails
- Interview Reminder Emails
- Monthly Placement Reports

---

# Frontend

- Vue.js
- Vue Router
- Axios
- Bootstrap 5
- Chart.js
- Responsive UI

---

# Backend

- Flask
- SQLAlchemy
- JWT
- Celery
- Redis
- Flask-Mail
- Flask-Caching

---

# Database

SQLite

Main Tables

- Users
- Students
- Companies
- Placement Drives
- Applications
- Placements

---

# Tech Stack

## Frontend

- Vue.js
- Bootstrap 5
- Axios
- Chart.js

## Backend

- Flask
- SQLAlchemy
- JWT
- Celery
- Redis
- Flask-Mail
- Flask-Caching

## Database

- SQLite

---

# Project Structure

```
placement-portal-v2/
│
├── backend/
│   ├── routes/
│   ├── uploads/
│   ├── exports/
│   ├── reports/
│   ├── app.py
│   ├── models.py
│   ├── tasks.py
│   ├── celery_app.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│
└── README.md
```

---

# Installation

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python app.py
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Redis

```bash
redis-server
```

---

## Celery Worker

```bash
celery -A celery_app.celery worker --loglevel=info
```

---

## Celery Beat

```bash
celery -A celery_app.celery beat --loglevel=info
```

---

# Future Enhancements

- Progressive Web App (PWA)
- SMS Notifications
- Advanced Resume Parsing
- AI-powered Resume Suggestions
- Multi-College Support

---

# Developed By

**Riddesh Saboo**

Bachelor of Technology (Computer Science)

MIT Academy of Engineering