from datetime import datetime
import random
import time
from app.services import api_client
from dateutil import parser

max_tries = 5
delay = 0.2  # s
success = []
still_trying = []
failure = []


def enrollSpam(lesson_id):
    print(
        "Starting enrollment spam for lesson",
        lesson_id,
        "at ",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    tries = 0
    while tries < max_tries:
        tries += 1
        response = enroll(lesson_id)
        if response.status_code == 201:
            success.append(lesson_id)
            return
        else:
            time.sleep(delay)

    print("Failed to enroll in lesson", lesson_id)
    still_trying.append(lesson_id)
    failure.append(lesson_id)


def enroll(lesson_id):
    return api_client.enroll_in_lesson(lesson_id)


def try_enrollment(lesson_id):
    response = api_client.get_lesson(lesson_id)
    if response.status_code != 200:
        return False

    data = response.json()
    if data["data"]["participantsMax"] == data["data"]["participantCount"]:
        return False

    cancelation_deadline = parser.parse(data["data"]["cancelationUntil"])
    if datetime.now(cancelation_deadline.tzinfo) > cancelation_deadline:
        still_trying.remove(lesson_id)
        return False

    response = enroll(lesson_id)
    if response.status_code == 201:
        failure.remove(lesson_id)
        still_trying.remove(lesson_id)
        success.append(lesson_id)


def try_enrollment_for_still_trying():
    print(
        "Trying to enroll into full lessons, at ",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    random_delay = random.randint(20, 60)
    time.sleep(random_delay)
    for lesson_id in still_trying:
        try_enrollment(lesson_id)
