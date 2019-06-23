from .base import Module
from yaledirectory import YaleDirectory


class People(Module):
    DESCRIPTION = "Get information about Yale-affiliated people"
    ARGC = 1
    api = YaleDirectory(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        people = self.api.search(query)
        if not people:
            return "No search results."
        response = ""
        for person in people[:1]:
            response += "Name: " + person.display_name
            response += "NetID: " + person.netid
            if person.phone_number:
                response += "Phone: " + person.phone_number
            if person.primary_organization_name:
                response += "Primary organization: " + person.primary_organization_name
            if person.primary_school_name:
                response += "Primary school: " + person.primary_school_name
            if person.residential_college_name:
                response += "Residential College Name: " + person.residential_college_name
            if person.student_expected_graduation_year:
                response += "Grad year: " + person.student_expected_graduation_year
            response += "UPI: " + person.upi
        return response
