import requests

def make_api_call(data):
    url = "https://api.example.com/endpoint"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "API call failed"}
