import unittest
import bot


class MessageProcessing(unittest.TestCase):
    def _message(self, text, response):
        if type(response) != list:
            response = [response]
        message = bot.Message(text=text)
        self.assertEqual(bot.process_message(message), response)

    def test_empty(self):
        self._message("This shouldn't trigger anything.", [])

    def test_static(self):
        for key in bot.static_commands:
            self._message(bot.PREFIX + key, bot.static_commands[key])


if __name__ == "__main__":
    unittest.main()
