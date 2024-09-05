from apscheduler.schedulers.background import BackgroundScheduler

from app.services.enrollment_bot import enroll

scheduler = BackgroundScheduler()

def schedule_enrollment(lesson_id, date):
    scheduler.add_job(enroll, 'date', run_date=date, args=[lesson_id], id=lesson_id)
    return True