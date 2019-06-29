from .base import Module
from yaleorgdirectory import YaleOrgDirectory
import os


class Organizations(Module):
    DESCRIPTION = "Get information on organizations on Yale's campus. Optionally specify a comma-separated list of tags."
    api = YaleOrgDirectory(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        organizations = self.api.organizations(tags=query)
        if not organizations:
            return "No organizations found."
        return self.bullet_list([(organization.name, organization.website) for organization in organizations])
