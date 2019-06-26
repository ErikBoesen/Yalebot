from .base import Module
from yalecourses import YaleCourses
import os


class Course(Module):
    DESCRIPTION = "Get information on a Yale course, simply by specifying its ID. Specify a subject to learn about all courses in that subject"
    ARGC = 1
    api = YaleCourses(os.environ.get("YALE_API_KEY"))

    def response(self, query, message):
        if not any([char.isdigit() for char in query]):
            courses = self.api.courses(query)
            if not courses:
                return query + " is not a recognized subject."
            response = self.bullet_list(tuple([(course.subject_code + course.number, course.name) for course in courses]))
            response += f"\nSpecify a course's number to get further information, for example '!course {courses[0].subject_code}{courses[0].number}'"
            return response
        else:
            course = self.api.course(query)
            if not course:
                return query + " is not a recognized course."
            return self.bullet_list(((course.number, course.name),
                                     ("Meeting schedule(s)", ", ".join(course.meeting_patterns)),
                                     ("Professors", ", ".join(course.instructors)),
                                     ("School", course.school_name),
                                     ("Registration available", ("YES" if course.active else "NO")),
                                     ("Description", "\n" + course.raw_description)))
