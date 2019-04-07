from .base import Module


class NATO(Module):
    dictionary = {"A":"Alpha", "B":"Bravo","C":"Charlie", "D":"Delta", "E":"Echo", "F":"Foxtrot", "G":"Golf","H":"Hotel", "I":"India", "J":"Juliet", "K":"Kilo", "L":"Lima", "M":"Mike", "N":"November", "O":"Oscar", "P":"Papa", "Q":"Quebec", "R":"Romeo", "S":"Sierra", "T":"Tango", "U":"Uniform", "V":"Victor", "W":"Whiskey", "X":"Xray", "Y":"Yankee", "Z":"Zulu"}

    def convert(self, char):
        if char.isupper():
            return dictionary[char]
        else:
            return dictionary[char.upper()].lower()

    def translate(self, text):
        return " ".join([self.convert(char) for char in text if char.isalpha()])

    def response(self, query, message):
        return self.translate(query)

    DESCRIPTION = translate("It good")
