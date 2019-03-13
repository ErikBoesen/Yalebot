from .base import Module
	
class ENQUOTE(Module):
    DESCRIPTION = "writes quote en quote however many times"
    ARGC = 1
    def response(self, query, message):
	if(query < 0 || query > 10):
		query = 1
        return "quote en" + " quote en"*int(query)

