import requests

LOGIN_ENDPOINT = 'http://localhost:8000/api/v1/auth/get-token/'

def loginAPI(username, password):
    response = requests.post(LOGIN_ENDPOINT, data={'username':username, 'password': password})
    print(response.json())
    json_response = response.json()
    # 200 means OK / Successful Login
    if response.status_code == 200:
        return True, json_response['token']
    # For this specific endpoint error keys is/are 'non_field_errors':
    return False, json_response['non_field_errors']
    