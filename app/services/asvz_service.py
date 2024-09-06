from app.services import api_client
from app.services import enrollment_scheduler
from dateutil import parser
from datetime import datetime
from config import Config

def loginAndStoreCreds(username, password):
    Config.update_credentials(username, password)
    if me():
        return "Login successful!", 200
    else:
        return "Login failed!", 500

def enroll(lesson_id):
    try:
        response = api_client.enroll_in_lesson(lesson_id)
        if response.status_code == 201:
            return True, "Successfully Enrolled!"
        elif response.status_code == 422:
            error_message = response.json()['errors'][0]['message']
            if error_message == "Der Anmeldebeginn liegt in der Zukunft - eine Anmeldung ist leider noch nicht möglich!":
                if enrollment_scheduler.check_already_scheduled(lesson_id):
                    return True, "The course is already scheduled!"
                response = api_client.get_lesson(lesson_id)
                enrollmentDateTime = response.json()['data']['enrollmentFrom']
                enrollment_scheduler.schedule_enrollment(lesson_id, parser.parse(enrollmentDateTime))
                return True, "Scheduled Enrollment!"
            elif error_message == "Das Angebot ist schon ausgebucht.":
                return False, "Full"
        else:
            return False, "Error " + str(response.status_code)
    except Exception as e:
        return False, "Error " + str(e)
    
def unenroll(lesson_id):
    try:
        if enrollment_scheduler.check_already_scheduled(lesson_id):
            enrollment_scheduler.remove_scheduled_enrollment(lesson_id)
            return True, "Scheduled Enrollment Removed"
        
        response = api_client.unenroll_from_lesson(lesson_id)
        if response.status_code == 200:
            return True, "Successfully Unenrolled!"
        else:
            return False, "Error " + str(response.status_code)
    except Exception as e:
        return False, "Error " + str(e)

def enrollment(lesson_id):
    try:
        response = api_client.enrollment_status(lesson_id)
        if response.status_code == 200:
            data = response.json()
            match(data['data']['status']):
                case 1:
                    return "Code 1", 500
                case 2:
                    return "Code 2", 500
                case 3:
                    return "Code 3", 500
                case 4:
                    return "4 - definitiv", 200
                case 5:
                    return "Code 5", 500
                case 6:
                    return "6 - abgemeldet", 500
                case x:
                    return "Unknown Code " + str(x), 500
        elif response.status_code == 404:
            return "Not Found", 404
    except Exception as e:
        return "Error " + str(e), 500
        
def lesson(lesson_id):
    response = api_client.get_lesson(lesson_id)
    if response.status_code == 200:
        return response.json()
    
def me():
    try:
        response = api_client.get_personal_data()
        if response.status_code == 200:
            return response.json()['firstName']
    except Exception as e:
        return False
    
def get_enrollments():
    try:
        response = api_client.my_enrollments()
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return False
    
def get_summary():
    return enrollment_scheduler.get_summary()

def get_scheduled_courses():
    jobs = enrollment_scheduler.get_jobs()
    courses = []
    for job in jobs:
        response = api_client.get_lesson(job.id)
        if response.status_code == 200:
            data = response.json()['data']
            course = {"lessonId": data['id'], "lessonName": data['title'], "lessonStart": data['starts'], "lessonEnd": data['ends'], 'location': data['facilities'][0]['name'], "sportName": data['sportName'], "status": "Sheduled"}
            courses.append(course)
    
    return courses

def status(lesson_id):
    courseResponse = api_client.get_lesson(lesson_id)
    if courseResponse.status_code == 200:
        courseData = courseResponse.json()['data']
        if courseData['cancellationDate'] != None:
            return "Canceled", 200
        response = api_client.enrollment_status(lesson_id)
        if response.status_code == 200:
            data = response.json()['data']['status']
            if data == 4:
                return "Enrolled", 200
        if enrollment_scheduler.check_already_scheduled(lesson_id):
            return "Scheduled", 200
        enrollment_until = parser.parse(courseData['enrollmentUntil'])
        if datetime.now(enrollment_until.tzinfo) > enrollment_until:
            return "Expired", 200
        if courseData['participantsMax'] == courseData['participantCount']:
            return "Full", 200
        return "Not Full", 200
    else:
        return "Not Found", 404

def inspect_response(response):
# Check the status code
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

    # If the response is in JSON format, you can use the .json() method
    try:
        print("\nJSON Content:")
        print(response.json())
    except ValueError:
        print("\nResponse is not in JSON format")

    # Check the URL that was requested
    print("\nURL:")
    print(response.url)

    # Check the history of redirects (if any)
    if response.history:
        print("\nRedirect History:")
        for resp in response.history:
            print(f"Status: {resp.status_code}, URL: {resp.url}")
    else:
        print("\nNo Redirect History")