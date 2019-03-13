from .base import Module
	
class PWEASE(Module):
	def responseMaker(message):
		newQuery = ""
		for c in message.lower():
			if c == "r":
				c = "w"
			if c == ".":
			    c = ""
			newQuery += c
			
	return newQuery + " uwu."
    DESCRIPTION = "Improve the engwish wanguage uwu"
    ARGC = 1
    def response(self, query, message):
        return self.responseMaker(query)

