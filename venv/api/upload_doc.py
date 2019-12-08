import requests

UPLOAD_DOC_ENDPOINT = 'http://localhost:8000/api/v1/external/upload/docs/'

def uploadDocAPI(token, file, doc_type, employee_id, company_code):
    response = requests.post(
        UPLOAD_DOC_ENDPOINT,
        files={'file': file}, 
        data={'employee_id': employee_id, 'company_code': company_code, 'type': doc_type},
        headers={'Authorization': 'Token {}'.format(token)})
    print(response.json())
    json_response = response.json()
    # 201 means Successfully created
    if response.status_code == 201:
        return True, '{} - {}'.format(employee_id, file.name), 'OK'
    # For this specific endpoint error keys is/are 'non_field_errors':
    return False, '{} - {}'.format(employee_id, file.name), json_response['detail']
    