from .base import Module
from yalecourses import YaleCourses
import os


class Course(Module):
    DESCRIPTION = "Get information on a Yale course, simply by specifying its ID. Specify a subject to learn about all courses in that subject."
    ARGC = 1
    api = YaleCourses(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        if query.isalpha():
            courses = self.api.courses(query)
            if course is None:
                return "No course found with that ID."
            response = ""

            return response
        else:
            return "Single course information querying coming soon!"
