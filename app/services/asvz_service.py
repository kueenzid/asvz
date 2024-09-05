from app.services import api_client

def enroll(lesson_id):
    try:
        response = api_client.enroll_in_lesson(lesson_id)
        if response.status_code == 201:
            return True
        else:
            return False
    except Exception as e:
        return False
    
def unenroll(lesson_id):
    try:
        response = api_client.unenroll_from_lesson(lesson_id)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False

def enrollment(lesson_id):
    try:
        response = api_client.enrollment_status(lesson_id)
        if response.status_code == 200:
            data = response.json()
            match(data['data']['status']):
                case 1:
                    return "Code 1"
                case 2:
                    return "Code 2"
                case 3:
                    return "Code 3"
                case 4:
                    return "4 - definitiv"
                case 5:
                    return "Code 5"
                case 6:
                    return "6 - abgemeldet"
                case _:
                    return "Unknown Code"
    except Exception as e:
        return "Error"
        
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