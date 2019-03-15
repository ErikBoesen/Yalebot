from .base import Module
from glob import glob
import os

class About(Module):
    def counts(self):
        total_lines = 0
        most_lines = 0
        longest_file = None
        for filename in glob("*.py") + glob("modules/*.py"):
            with open(filename) as f:
                lines = len(f.readlines())
                total_lines += lines
                if lines > most_lines:
                    most_lines = lines
                    longest_file = filename
        return (total_lines, longest_file, most_lines)

    def response(self, query, message):
        total_lines, longest_file, most_lines = self.counts()
        return f"I am a bot maintained by Erik Bøsen, whom you should follow on Instagram @erikboesen. Use the command !help to view a list of bot capabilities. The bot's source code can be viewed and contributed to on GitHub: https://github.com/ErikBoesen/Yalebot\n\nI am currently running on {total_lines} lines of code. My largest file is {longest_file}, at {most_lines} lines.",
