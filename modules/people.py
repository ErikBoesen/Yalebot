from .base import Module
from yaledirectory import YaleDirectory


class People(Module):
    DESCRIPTION = "Get information about Yale-affiliated people"
    ARGC = 1
    api = YaleDirectory()

    def response(self, query, message):
        people = self.api.search(query)
        if not people:
            return "No search results."
        response = ""
        for person in people[:1]:
            response += "Name: " + person.display_name + "\n"
            if person.netid:
                response += "NetID: " + person.netid + "\n"
            if person.phone_number:
                response += "Phone: " + person.phone_number + "\n"
            if person.primary_organization_name:
                response += "Primary organization: " + person.primary_organization_name + "\n"
            if person.primary_school_name:
                response += "Primary school: " + person.primary_school_name + "\n"
            if person.residential_college_name:
                response += "Residential College Name: " + person.residential_college_name + "\n"
            if person.student_expected_graduation_year:
                response += "Grad year: " + person.student_expected_graduation_year + "\n"
        return response
