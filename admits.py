import requests
from requests.auth import HTTPDigestAuth

ADMITS = 'https://apps.admissions.yale.edu/portal/admits?cmd=faces'
LOGIN = 'https://apps.admissions.yale.edu/account/login'
with requests.Session() as session:
    payload = {
        'email': 'erik.boesen@gmail.com',
        'password': '',
    }
    r = session.post(LOGIN, data=payload)
    print(r.text)
