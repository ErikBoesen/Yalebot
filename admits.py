import requests
import os
from bs4 import BeautifulSoup
import json
import re
import base64

ADMITS_PAGE = "https://apps.admissions.yale.edu/portal/admits?cmd=faces"
LOGIN_PAGE = "https://apps.admissions.yale.edu/account/login"
USER_PATH = "https://apps.admissions.yale.edu/portal/admits"
session = requests.Session()

credentials = {
    "email": os.environ["YALE_PORTAL_EMAIL"],
    "password": os.environ["YALE_PORTAL_PASSWORD"],
}
# Log in to portal using credentials, persisting authentication through session
session.post(LOGIN_PAGE, data=credentials)

# Iterate through paginated admits list, scraping data from each page and popup content
finished = False
page_number = 0
names = []
students = []
while not finished:
    page_number += 1
    page = session.get(ADMITS_PAGE + "&page=%d" % page_number)
    bs = BeautifulSoup(page.text, "lxml")
    page_names = [name_element.string.lower() for name_element in bs.find_all("div", {"class": "facebook_name"})]
    names += page_names
    print("Page {page_number} processing, with {admit_count} admits.".format(page_number=page_number,
                                                                             admit_count=len(page_names)))
    for student_entry in bs.find_all("div", {"class": "facebook_entry"}):
        entry = session.get(USER_PATH + student_entry["data-href"])
        student_bs = BeautifulSoup(entry.text, "lxml")
        student = {}
        # Iterate through rows, skipping photo
        for row in student_bs.find_all("tr")[1:]:
            question = row.find("th")
            answer = row.find("td")
            if None not in (question, answer):
                student[question.string.strip()] = answer.string
        photo_element = student_entry.find("div", {"class": "facebook_photo"})
        photo = re.findall(r"url\(data:image/png;base64,(.*?)\)", photo_element["style"])
        # If a base64-encoded photo is found (sometimes only the default one will be linked)
        # TODO: do something with images
        """
        if len(photo) != 0:
            with open("photos/" + student["Name"] + ".png", "wb") as f:
                f.write(base64.decodebytes(photo[0].encode()))
        """
        print("Processed student: {name}.".format(name=student["Name"]))
        students.append(student)
    if len(page_names) < 4 * 12:
        # Page isn"t full, implying this is the last.
        finished = True

print("{name_count} admits processed.".format(name_count=len(names)))
with open("resources/admit_names.json", "w") as f:
    json.dump(names, f)

student_dict = {student["Name"].lower(): student for student in students}

with open("resources/admits.json", "w") as f:
    json.dump(student_dict, f)
