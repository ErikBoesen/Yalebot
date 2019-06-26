from .base import Module
import morse_talk


class Morse(Module):
    DESCRIPTION = "Cipher or decipher morse code"
    ARGC = 1

    def is_morse(self, text: str) -> bool:
        """
        Given a string, determine if it is morse code or just regular text.
        """
        return all([c in '-. ' for c in text])

    def response(self, query, message):
        query = query.replace('_', '-')
        if self.is_morse(query):
            return morse_talk.decode(query)
        else:
            return morse_talk.encode(query)
