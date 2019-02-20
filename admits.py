import requests
from requests.auth import HTTPDigestAuth
import os

ADMITS = 'https://apps.admissions.yale.edu/portal/admits?cmd=faces'
LOGIN = 'https://apps.admissions.yale.edu/account/login'
session = requests.Session()

payload = {
    'email': os.environ['YALE_PORTAL_EMAIL'],
    'password': os.environ['YALE_PORTAL_PASSWORD'],
}
r = session.post(LOGIN, data=payload)
r = session.get(ADMITS + '&page=2')
print(r.text)
