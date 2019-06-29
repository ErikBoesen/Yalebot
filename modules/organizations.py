from .base import Module
from yaleorgdirectory import YaleOrgDirectory
import os


class Organizations(Module):
    DESCRIPTION = "Get information on organizations on Yale's campus. Optionally specify a comma-separated list of tags."
    api = YaleOrgDirectory(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        if not query:
            if not organizations:
                return "No organizations found."
            organizations = self.api.organizations(tags=query)
            return self.bullet_list([(organization.name, organization.website) for organization in organizations])
        else:
            organization = self.api.organization(query)
            if not organization:
                return f"No organization '{query}' found."
            return self.bullet_list((("Name", organization.name),
                                     ("Website", organization.website),
                                     ("Address", organization.address),
                                     ("Room #", organization.room),
                                     ("Telephone #", organization.telephone)))
