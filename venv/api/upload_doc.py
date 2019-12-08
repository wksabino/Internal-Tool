import requests

UPLOAD_DOC_ENDPOINT = 'http://localhost:8000/api/v1/external/upload/docs/'

def uploadDocAPI(token, file, type, employee_id, company_code):
    response = requests.post(LOGIN_ENDPOINT, data={'file':file, 'employee_id': employee_id, 'company_code': company_code})
    print(response.json())
    json_response = response.json()
    # 200 means OK / Successful Login
    if response.status_code == 200:
        return True, json_response['token']
    # For this specific endpoint error keys is/are 'non_field_errors':
    return False, json_response['non_field_errors']
    