from .base import Module


class Love(Module):
    DESCRIPTION = "Express your feelings"
    ARGC = 1

    def response(self, query, message):
        return "💓💕💗💖💚❤️💜🧡❤️💜💗💕💓💖❤️💜💗💖💚💙💙💚💖💕❤️💚💜 oh fuck I dropped my love for " + query + " 💓💕💗💖💚❤️💜🧡❤️💜💗💕💓💖❤️💜💗💖💚💙💙💚💖💕❤️💚it keeps getting everywhere oh fuck 💓💕💗💖💚❤️💜🧡❤️💜💗💕💓💖❤️💜💗💖💚💙💙💚💖💕❤️💚I’m so clumsy oh "
