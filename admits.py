import requests
import os
from bs4 import BeautifulSoup
import json

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
page_number = 0
names = []
while not finished:
    page_number += 1
    page = session.get(ADMITS_PAGE + '&page=%d' % page_number)
    bs = BeautifulSoup(page.text, 'html.parser')
    page_names = [name_element.string.lower() for name_element in bs.find_all('div', {'class': 'facebook_name'})]
    if len(page_names) < 4 * 12:
        # Page isn't full, implying this is the last.
        finished = True
    names += page_names
    print('Page {page_number} processed, with {admit_count} admits.'.format(page_number=page_number,
                                                                            admit_count=len(page_names)))

print('{name_count} admit names fetched.'.format(name_count=len(names)))
with open('resources/admit_names.json', 'w+') as f:
    json.dump(names, f)
