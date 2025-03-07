'''
Utils for common api response patterns.
'''
RESPONSE_HEADERS = {
    'Content-Type': 'application/json'
}


def success(json_success_response, status_code=200):
    '''
    Returns success json response.
    '''
    success_headers = {}.update(RESPONSE_HEADERS)
    success_response = {'success': True, 'content': json_success_response}
    return success_response, status_code, success_headers


def client_error(json_err_response, status_code=400):
    '''Returns client error json response.'''
    return error(json_err_response, status_code)


def server_error(json_err_response, status_code=500):
    '''Returns server error json response.'''
    return error(json_err_response, status_code)


def error(json_err_response, status_code):
    '''Returns error json response.'''
    error_headers = {}.update(RESPONSE_HEADERS)
    error_response = {'success': False, 'content': json_err_response}
    return error_response, status_code, error_headers
