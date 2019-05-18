from .base import Module
from glob import glob
import json


class About(Module):
    DESCRIPTION = "Show basic information about Yalebot"
    string = None

    def response(self, query, message):
        # Generate response on first run, and not after that
        if self.string is None:
            total_lines = 0
            most_lines = 0
            longest_file = None
            filenames = []
            for criterion in ["Procfile", "*.py", "*.sh", "static/stylesheets/*.css",
                              "static/scripts/*", "modules/*.py",
                              "hooks/*", "templates/*"]:
                filenames.extend(glob(criterion))
            for filename in filenames:
                with open(filename) as f:
                    lines = len(f.readlines())
                    total_lines += lines
                    if lines > most_lines:
                        most_lines = lines
                        longest_file = filename
            self.string = f"👋 Hi! I'm Yalebot, a bot maintained by Erik Bøsen, whom you should follow on Instagram @erikboesen. Use the command !help to view a list of my abilities. My source code can be viewed and contributed to on GitHub: https://github.com/ErikBoesen/Yalebot\n\nI am currently running on {total_lines} lines of code and markup. My largest file is {longest_file}, at {most_lines} lines."
        return self.string
