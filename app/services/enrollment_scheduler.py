from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from app.services.enrollment_bot import success
from app.services.enrollment_bot import failure

from app.services.enrollment_bot import enroll

scheduler = BackgroundScheduler()

def schedule_enrollment(lesson_id, date):
    date = date - timedelta(seconds=1)
    scheduler.add_job(enroll, 'date', run_date=date, args=[lesson_id], id=str(lesson_id))

def remove_job(job_id):
    scheduler.remove_job(job_id)

def get_jobs():
    return scheduler.get_jobs()

def get_summary():
    return {"scheduled": [str(job.id) for job in get_jobs()], "success": success, "failure": failure}

def check_already_scheduled(lesson_id):
    jobs = get_jobs()
    for job in jobs:
        if job.id == str(lesson_id):
            return True
    return False