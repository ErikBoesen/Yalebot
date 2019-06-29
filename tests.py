import unittest
import bot


class ProcessMessage(unittest.TestCase):
    def test_empty(self):
        message = bot.Message(text="This message shouldn't trigger a response.")
        self.assertEqual(bot.process_message(message), [])


if __name__ == "__main__":
    unittest.main()
