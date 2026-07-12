from celery import Celery
from app import create_app

flask_app = create_app()

celery = Celery(
    flask_app.import_name,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(flask_app.config)

from celery.schedules import crontab

celery.conf.beat_schedule = {
    "daily-interview-reminders": {
        "task": "tasks.send_interview_reminders",
        "schedule": crontab(hour=9, minute=0),
    },

    "monthly-placement-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1,hour=9,minute=30),
    }
}

celery.conf.timezone = "Asia/Kolkata"

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask

import tasks