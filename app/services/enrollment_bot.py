import time
from app.services import api_client

max_tries = 10;
delay = 0.3; # s
success = []
failure = []

def enroll(lesson_id):
    tries = 0
    while tries < max_tries:
        tries += 1
        response = api_client.enroll_in_lesson(lesson_id)
        inspect_response(response)
        if response.status_code == 201:
            success.append(lesson_id)
            return
        else:
            time.sleep(delay)

    failure.append(lesson_id)
    
def inspect_response(response):
    # Check the status code
    print("###############################################")
    print("Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print("Status Code:", response.status_code)

    # Check the response headers
    print("\nHeaders:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    # Check the cookies
    print("\nCookies:")
    for cookie in response.cookies:
        print(f"{cookie.name}: {cookie.value}")

    # Check the response content in bytes
    print("\nContent (in bytes):")
    print(response.content)

    # Check the response content as a string (decoded text)
    print("\nContent (decoded):")
    print(response.text)
    print("###############################################")