from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from app.services.enrollment_bot import success, try_enrollment_for_still_trying
from app.services.enrollment_bot import failure, still_trying

from app.services.enrollment_bot import enroll
from app.services.api_client import get_bearer_token
from app.services.logger import setup_logger

logger = setup_logger("enrollment_scheduler_logger", "enrollment_scheduler")

scheduler = BackgroundScheduler()
refreshTokenScheduler = BackgroundScheduler()
check_course_interval = 60


def schedule_enrollment(lesson_id, date):
    logger.info("Scheduling enrollment for lesson %s", lesson_id, "at", date)
    scheduler.add_job(
        enroll, "date", run_date=date, args=[lesson_id], id=str(lesson_id)
    )
    date = date - timedelta(seconds=30)
    logger.info("Scheduling refresh token for lesson %s", lesson_id, "at", date)
    refreshTokenScheduler.add_job(
        get_bearer_token,
        "date",
        run_date=date,
        id="refresh_token_for_" + str(lesson_id),
    )


def schedule_missed_enrollment():
    logger.info("Scheduling missed enrollments")
    refreshTokenScheduler.add_job(
        try_enrollment_for_still_trying,
        "interval",
        seconds=check_course_interval,
        id="scheduler_for_still_trying",
    )


def remove_scheduled_enrollment(lesson_id):
    logger.info("Removing scheduled enrollment for lesson %s", lesson_id)
    scheduler.remove_job(str(lesson_id))
    refreshTokenScheduler.remove_job("refresh_token_for_" + str(lesson_id))


def remove_job(job_id):
    scheduler.remove_job(job_id)


def get_jobs():
    return scheduler.get_jobs()


def get_summary():
    return {
        "scheduled": [str(job.id) for job in get_jobs()],
        "success": success,
        "still_trying": still_trying,
        "failure": failure,
    }


def check_already_scheduled(lesson_id):
    jobs = get_jobs()
    for job in jobs:
        if job.id == str(lesson_id):
            return True
    return False
