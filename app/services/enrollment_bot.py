import time
from app.services import api_client

max_tries = 30;
delay = 0.1; # s

def enroll(lesson_id):
    tries = 0
    while tries < max_tries:
        tries += 1
        response = api_client.enroll_in_lesson(lesson_id)
        if response:
            return "Success", 200
        else:
            time.sleep(delay)

    return "Failure", 500
    