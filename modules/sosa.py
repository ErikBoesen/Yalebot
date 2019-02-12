from .base import Module

THESE_BITCHES_LOVE_SOSA = """Fuckers in school telling me, always in the barber shop
Chief Keef ain't bout this, Chief Keef ain't bout that
My boy a BD on fucking Lamron and them
He, he they say that n**** don't be putting in no work
SHUT THE FUCK UP!
Y'all n****s ain't know shit
All ya motherfuckers talk about
Chief Keef ain't no hitta Chief Keef ain't this Chief Keef a fake SHUT THE FUCK UP Ya'll don't live with that n****
Y'all know that n**** got caught with a ratchet
Shootin' at the police and shit
n**** been on probation since fuckin, I don't know when! Motherfuckers stop fuckin' playin' him like that
Them n****s savages out there
If I catch another motherfucker talking sweet about Chief Keef I'm fucking beating they ass! I'm not fucking playing no more 
You know those n****s roll with Lil' Reese and them"""

class Sosa(Module):
	DESCRIPTION = "Sends the best intro to a song ever made"
	def response(self, query, message):
		return THESE_BITCHES_LOVE_SOSA
