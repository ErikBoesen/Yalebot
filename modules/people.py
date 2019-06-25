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
            response += self.bullet_list((("Name", person.display_name),
                                          ("NetID", person.netid),
                                          ("Phone", person.phone_number),
                                          ("Primary organization", person.primary_organization_name),
                                          ("Primary school", person.primary_school_name),
                                          ("Residential College Name", person.residential_college_name),
                                          ("Grad year", person.student_expected_graduation_year))) + "\n"
        return response
