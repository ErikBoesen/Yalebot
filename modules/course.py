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
            if not courses:
                return f"{query} is not a recognized subject."
            response = ""
            for course in courses:
                response += f"* {course.subject_code}{course.number}: {course.name}\n"
            response += f"\nSpecify a course's number to get further information, for example '!course {courses[0].subject_code}{courses[0].number}'"
            return response
        else:
            return "Single course information querying coming soon!"
