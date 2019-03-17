from .base import Module

class Elizabeth(Module):
    DESCRIPTION = "𝕙𝕒𝕣𝕕 𝕨𝕠𝕣𝕜 𝕡𝕒𝕪𝕤 𝕠𝕗𝕗."
    ARGC = 1
    def response(self, query, message):
        return "".join([chr(ord(c) + (0x1d551 - 96)) if ord("a") <= ord(c) <= ord("z") else c
                        for c in query.lower()])
