import time
from app.services import api_client

max_tries = 30;
delay = 0.1; # s
success = []
failure = []

def enroll(lesson_id):
    tries = 0
    while tries < max_tries:
        tries += 1
        response = api_client.enroll_in_lesson(lesson_id)
        if response.status_code == 201:
            success.append(lesson_id)
            return
        else:
            time.sleep(delay)

    failure.append(lesson_id)
    