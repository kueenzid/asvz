import re
import requests
import secrets
from config import Config


def make_api_call(data):
    return get_bearer_token()


def get_bearer_token():
    url = "https://auth.asvz.ch/Account/Login"
    response = requests.get(url)

    requestVerificationToken = extract_request_verification_token(response.text)
    antiForgeryCookieName, antiForgeryCookieToken = extract_anti_forgery_token(response.cookies)

    data, headers = prepare_login_request(requestVerificationToken, antiForgeryCookieName, antiForgeryCookieToken)
    
    return login(data, headers, antiForgeryCookieName, antiForgeryCookieToken)


def login(data, headers, antiForgeryCookieName, antiForgeryCookieToken):
    url = "https://auth.asvz.ch/Account/Login"
    response = requests.post(url, data=data, headers=headers, allow_redirects=False)

    idscrvSessionCookieName, idscrvSessionCookieToken = extract_idscrv_session_cookie(response.cookies)
    identityApplicationCookieName, identityApplicationCookieToken = extract_identity_application_cookie(response.cookies)

    headers = prepare_authorize_request(idscrvSessionCookieName, idscrvSessionCookieToken, identityApplicationCookieName, identityApplicationCookieToken, antiForgeryCookieName, antiForgeryCookieToken)

    return authorize(headers)


def authorize(headers):
    state = secrets.token_hex(16)
    nonce = secrets.token_hex(16)

    url = f"https://auth.asvz.ch/connect/authorize?client_id=55776bff-ef75-4c9d-9bdd-45e883ec38e0&redirect_uri=https%3A%2F%2Fschalter.asvz.ch%2Ftn%2Fassets%2Foidc-login-redirect.html&response_type=id_token%20token&scope=openid%20profile%20tn-api%20tn-apiext%20tn-auth%20tn-hangfire&state={state}&nonce={nonce}"
    response = requests.get(url, headers=headers, allow_redirects=False)

    location = response.headers["Location"]
    id_token = extract_id_token(location)

    return id_token


def extract_id_token(location):
    match = re.search(r'id_token=([^&]+)', location)
    
    if match:
        id_token = match.group(1)
        return id_token
    else:
        raise Exception("id_token not found")


def prepare_authorize_request(idscrvSessionCookieName, idscrvSessionCookieToken, identityApplicationCookieName, identityApplicationCookieToken, antiForgeryCookieName, antiForgeryCookieToken):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,de-CH;q=0.8,de;q=0.7",
        "cache-control": "no-cache",
        "cookie": f"{antiForgeryCookieName}={antiForgeryCookieToken}; {idscrvSessionCookieName}={idscrvSessionCookieToken}; {identityApplicationCookieName}={identityApplicationCookieToken}",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://schalter.asvz.ch/",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
    }

    return headers


def extract_identity_application_cookie(cookies):
    for cookie in cookies:
        if cookie.name == ".AspNetCore.Identity.Application":
            return cookie.name, cookie.value
        
    raise Exception("Identity Application cookie not found")


def extract_idscrv_session_cookie(cookies):
    for cookie in cookies:
        if cookie.name == "idsrv.session":
            return cookie.name, cookie.value
        
    raise Exception("idsrv Session cookie not found")


def extract_anti_forgery_token(cookies):
    for cookie in cookies:
        if cookie.name == ".AspNetCore.Antiforgery.MkeJ4WI3ssE":
            return cookie.name, cookie.value
        
    raise Exception("AntiForgery token not found")


def prepare_login_request(requestVerificationToken, antiForgeryCookieName, antiForgeryCookieToken):
    data = {
        "AsvzId": Config.USERNAME,
        "Password": Config.PASSWORD,
        "__RequestVerificationToken": requestVerificationToken,
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,de-CH;q=0.8,de;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f"{antiForgeryCookieName}={antiForgeryCookieToken}",
        "origin": "https://auth.asvz.ch",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://auth.asvz.ch/Account/Login",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
    }

    return data, headers


def extract_request_verification_token(html):
    match = re.search(r'<input\s+name="__RequestVerificationToken"\s+type="hidden"\s+value="([^"]+)"', html)
    if match:
        token_value = match.group(1)
        return token_value
    else:
        raise Exception("RequestVerificationTokent not found")
    

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
