import requests

def url_to_text(url):
    """
    >>> text = url_to_text("http://example.com")
    >>> '<!doctype html>' in text
    True
    >>> text = url_to_text("example.com")
    >>> '<!doctype html>' in text
    True
    >>> text = url_to_text("www.example.com")
    >>> '<!doctype html>' in text
    True
    """
    if (('http://' not in url) and ('https://' not in url)):
        url = 'http://' + url
    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
    if response.status_code == 200:
        return response.text
    error_codes = {400: 'Bad request',
                   401: 'Unauthorized',
                   403: 'Forbidden',
                   404: 'Not Found',
                   429: 'Too Many Requests',
                   503: 'Service Unavailable'}
    return 'URL ' + url + ' encountered an error. ' + str(response.status_code) + '"' + error_codes[response.status_code] + '"'

if __name__ == "__main__":
    import doctest
    doctest.testmod()