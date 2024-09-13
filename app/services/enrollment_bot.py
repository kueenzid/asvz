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
        datetime.now(),
    )
    tries = 0
    while tries < max_tries:
        tries += 1
        response = enroll(lesson_id)
        if response.status_code == 201:
            print("Successfully enrolled in lesson", lesson_id, "at ", datetime.now())
            success.append(lesson_id)
            return
        else:
            time.sleep(delay)

    print("Failed to enroll in lesson", lesson_id, "at ", datetime.now())
    still_trying.append(lesson_id)
    failure.append(lesson_id)


def enroll(lesson_id):
    print("Enrolling in lesson", lesson_id, "at ", datetime.now())
    return api_client.enroll_in_lesson(lesson_id)


def try_enrollment(lesson_id):
    print("Check lesson", lesson_id, ":")
    response = api_client.get_lesson(lesson_id)
    if response.status_code != 200:
        return False

    data = response.json()
    if data["data"]["participantsMax"] == data["data"]["participantCount"]:
        print("Lesson", lesson_id, "is still full")
        return False

    cancelation_deadline = parser.parse(data["data"]["cancelationUntil"])
    if datetime.now(cancelation_deadline.tzinfo) > cancelation_deadline:
        still_trying.remove(lesson_id)
        print("Removed lesson", lesson_id, "from still_trying because it is expired")
        return False

    response = enroll(lesson_id)
    if response.status_code == 201:
        print("Enrolled in lesson", lesson_id)
        failure.remove(lesson_id)
        still_trying.remove(lesson_id)
        success.append(lesson_id)


def try_enrollment_for_still_trying():
    print("Trying to enroll into full lessons, at ", datetime.now(), ":")
    random_delay = random.randint(20, 60)
    time.sleep(random_delay)
    for lesson_id in still_trying:
        try_enrollment(lesson_id)
