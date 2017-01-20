import requests

def url_to_text(url):
    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
    if response.status_code = 200:
        return response.text
    error_codes = {400: 'Bad request',
                   401: 'Unauthorized',
                   403: 'Forbidden',
                   404: 'Not Found',
                   429: 'Too Many Requests',
                   503: 'Service Unavailable'}
    return 'URL ' + url + ' encountered an error. ' + str(response.status_code) + '"' + error_codes[response.status_code] + '"'
