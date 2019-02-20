import requests
from requests.auth import HTTPDigestAuth
import os
from bs4 import BeautifulSoup

ADMITS_PAGE = 'https://apps.admissions.yale.edu/portal/admits?cmd=faces'
LOGIN_PAGE = 'https://apps.admissions.yale.edu/account/login'
session = requests.Session()

credentials = {
    'email': os.environ['YALE_PORTAL_EMAIL'],
    'password': os.environ['YALE_PORTAL_PASSWORD'],
}
# Log in to portal using credentials, persisting authentication through session
session.post(LOGIN_PAGE, data=credentials)

# Iterate through paginated admits list, scraping names from each page
finished = False
page_number = 1
while not finished:
    page_number += 1
    page = session.get(ADMITS_PAGE + '&page=%d' % page_number)
    bs = BeautifulSoup(page.text, 'html5lib')
    print(bs.prettify())
    break
