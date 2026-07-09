# Placement Portal V2

A full-stack Placement Portal developed using Flask, Vue.js and SQLite for managing campus placements.

## Features

### Authentication
- JWT Authentication
- Role-Based Access Control
- Admin, Company and Student Modules

### Placement Management
- Placement Drives
- Student Applications
- Interview Scheduling
- Placement Tracking

### Background Jobs (Celery + Redis)
- Daily Interview Reminder Emails
- Monthly Placement Reports
- Asynchronous CSV Export
- Email Notifications

## Performance Optimization

The application uses Redis for API caching to improve response times.

### Cached APIs

- Admin Dashboard

- Company Dashboard

- Student Dashboard

- Student Job Listings

- Company Job Postings

- Company Applications

### Cache Policy

- Cache Backend: Redis

- Cache Expiry: 60 seconds

- Cache Refresh: Cache is cleared whenever placement-related data changes (job postings, applications, placements, approvals, etc.).

---

### Running Redis

```bash

redis-server

```

### Technologies

Backend
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Mail
- Celery
- Redis
- SQLite

Frontend
- Vue.js
- Bootstrap

## Installation

### Clone Repository

```bash
git clone <repository-url>
```

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### Redis

Start Redis server.

### Celery Worker

```bash
celery -A tasks worker --loglevel=info
```

### Celery Beat

```bash
celery -A tasks beat --loglevel=info
```

### Run Flask

```bash
python app.py
```

---

## Configuration

Update the SMTP credentials inside `config.py`.

```
MAIL_USERNAME
MAIL_PASSWORD
MAIL_DEFAULT_SENDER
JWT_SECRET_KEY
```

---

## Folder Structure

```
backend/
    routes/
    exports/
        student/
        company/
        reports/
    uploads/
    app.py
    tasks.py
    celery_app.py
```

---

## Developers

Final Year Project
Department of Computer Science