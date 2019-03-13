from .base import Module
	
class ENQUOTE(Module):
    DESCRIPTION = "writes quote en quote however many times"
    ARGC = 1
    def response(self, query, message):
        return "quote en" + " quote en"*int(query)

