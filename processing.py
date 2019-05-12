import re
import modules


PREFIX = "!"

static_commands = {
    "ping": "Pong!",
    "testing": "Join the Yalebot testing server: https://groupme.com/join_group/49940116/f2x20kxx",
    "add": "Add me to your own group here: https://yalebot.herokuapp.com",

    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "social": "https://docs.google.com/spreadsheets/d/10m_0glWVUncKCxERsNf6uOJhfeYU96mOK0KvgNURIBk/edit?fbclid=IwAR35OaPO6czQxZv26A6DEgEH-Qef0kCSe4nXxl8wcIfDml-BfLx4ksVtp6Y#gid=0",
    "meetup": ("", "https://i.groupme.com/750x1200.jpeg.b0ca5f6e660a4356be2925222e6f8246.large"),
    "test": "https://erikboesen.com/yalepuritytest",
    "dislike": "👎😬👎\n 🦵🦵",
    "shrug": r"¯\_(ツ)_/¯",
    "oh": ("", "https://i.groupme.com/766x750.jpeg.9209520c57e848369444ca498e31f90a.large"),
    "jah": ("", "https://i.groupme.com/766x750.jpeg.3eb07fe422db4b81947b634a1b309d48.large"),
    "bulldog": "Bulldog!  Bulldog!\nBow, wow, wow\nEli Yale\nBulldog!  Bulldog!\nBow, wow, wow\nOur team can never fail\n\nWhen the sons of Eli\nBreak through the line\nThat is the sign we hail\nBulldog!  Bulldog!\nBow, wow, wow\nEli Yale!",
    "popcorn": "https://www.youtube.com/watch?v=9nwOm4AAXwc",
    "yyle": "https://www.youtube.com/watch?v=SsZDxL-YMYc",
    "discord": "If you must: https://discord.gg/5EScef4",
    "bang": ("", "https://i.groupme.com/720x1440.png.c76127a21867451093edd11bbb09d75d.large"),
    "chike": ("", "https://i.groupme.com/1021x1400.jpeg.70192657c76745ab809357d0512d4951.large"),
    "pressed": ("", "https://i.groupme.com/540x719.jpeg.2229bdb9f15247a7a112ac0be95e065a.large"),
    "flex": "👮🏽🚨🚔 PULL OVER 👮🏽🚨🚔\n\n😤Put your hands behind your back😤\n\n🗣I'm taking you into custody🗣\n\n📝And registering you as a📝\n\n🔥😩FLEX OFFENDER😩🔥",
    "amma": ("", "https://i.groupme.com/714x456.jpeg.66fb9e9dacab4cd9b860b084eceff282.large"),
    "ohno": ("", "https://i.groupme.com/1280x720.jpeg.f7c11a529a3b4a7195f71fa6be5ebfef.large"),
    "defuse": ("", "https://i.groupme.com/500x500.jpeg.26cbc006bcbf47048ade8a896b1e3d5a.large"),
}

commands = {
    "about": modules.About(),
    "countdown": modules.Countdown(),
    "verify": modules.Verify(),
    "yalenews": modules.YaleNews(),
    "record": modules.Record(),
    "groups": modules.Groups(),
    "weather": modules.Weather(),

    "conversationstarter": modules.ConversationStarter(),
    "funfact": modules.FunFact(),
    "lyrics": modules.Lyrics(),
    "nasa": modules.NASA(),
    "sad": modules.Sad(),
    "xkcd": modules.XKCD(),
    "elizabeth": modules.Elizabeth(),
    "dania": modules.Dania(),
    "jake": modules.Jake(),
    "carlos": modules.Carlos(),
    "crista": modules.Crista(),
    "maria": modules.Maria(),
    "annie": modules.Annie(),
    "chat": modules.Chat(),
    "kelly": modules.Kelly(),
    "eightball": modules.EightBall(),
    "analytics": modules.Analytics(),
    "youtube": modules.YouTube(),
    "pick": modules.Pick(),
    "chose": modules.Chose(),
    "meme": modules.Meme(),
    "love": modules.Love(),
    "price": modules.Price(),
    "minion": modules.Minion(),
    "house": modules.House(),
    "location": modules.Location(),
    "twitter": modules.Twitter(),
    "tea": modules.Tea(),
    "amber": modules.Amber(),
    "uwu": modules.UWU(),
    "quote": modules.Quote(),
    "dog": modules.Dog(),
    "funny": modules.Funny(),
    "kelbo": modules.Kelbo(),
    "boink": modules.Boink(),
    "conversationstarter": modules.ConversationStarter(),
    "funfact": modules.FunFact(),
    "ship": modules.Ship(),
    "hema": modules.Hema(),
    "victor": modules.Victor(),
    "truman": modules.Truman(),
    "nato": modules.NATO(),
    "tiya": modules.Tiya(),
    "crist": modules.Crist(),
    "power": modules.Power(),
    "cah": modules.CardsAgainstHumanity(),
    "colleges": modules.Colleges(),
    "tictactoe": modules.TicTacToe(),
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "mccarthy": modules.McCarthy(),
    "circle": modules.Circle(),
}
system_responses = {
    "welcome": modules.Welcome(),
    "mourn": modules.Mourn(),
}

F_PATTERN = re.compile("can i get an? (.+) in the chat", flags=re.IGNORECASE | re.MULTILINE)


def process_message(message):
    responses = []
    text = message["text"]
    name = message["name"]
    forename = name.split(" ", 1)[0]
    print("Message received: %s" % message)
    f_matches = F_PATTERN.search(text)
    if f_matches is not None and len(f_matches.groups()):
        responses.append(f_matches.groups()[0] + " ❤")
    if message["sender_type"] != "bot":
        if text.startswith(PREFIX):
            instructions = text[len(PREFIX):].strip().split(None, 1)
            command = instructions.pop(0).lower()
            query = instructions[0] if len(instructions) > 0 else ""
            # Prevent response if prefix is repeated
            if PREFIX in command:
                pass
            # Check if there's a static response for this command
            elif command in static_commands:
                responses.append(static_commands[command])
            # If not, query appropriate module for a response
            elif command in commands:
                # Make sure there are enough arguments
                if len(list(filter(None, query.split("\n")))) < commands[command].ARGC:
                    responses.append(commands[command].ARGUMENT_WARNING)
                else:
                    response = commands[command].response(query, message)
                    if response is not None:
                        responses.append(response)
            elif command == "help":
                if query:
                    query = query.strip(PREFIX)
                    if query in static_commands:
                        responses.append(PREFIX + query + ": static response.")
                    elif query in commands:
                        responses.append(PREFIX + query + ": " + commands[query].DESCRIPTION + f". Requires {commands[query].ARGC} argument(s).")
                    elif query in meme_commands:
                        responses.append(PREFIX + query + ": meme command; provide captions separated by newlines.")
                    else:
                        responses.append("No such command.")
                else:
                    help_string = "--- Help ---"
                    help_string += "\nStatic commands: " + ", ".join([PREFIX + title for title in static_commands])
                    help_string += "\nTools: " + ", ".join([PREFIX + title for title in commands])
                    help_string += f"\n(Run `{PREFIX}help commandname` for in-depth explanations.)"
                    responses.append(help_string)
            else:
                try:
                    closest = difflib.get_close_matches(command, list(static_commands.keys()) + list(commands.keys()), 1)[0]
                    advice = f"Perhaps you meant {PREFIX}{closest}? "
                except IndexError:
                    advice = ""
                responses.append(f"Command not found. {advice}Use !help to view a list of commands.")
        if "thank" in text.lower() and "yalebot" in text.lower():
            responses.append("You're welcome, " + forename + "! :)")
    if message["system"]:
        for option in system_responses:
            if system_responses[option].RE.match(text):
                responses.append(system_responses[option].response(text, message))
        """
        if system_responses["welcome"].RE.match(text):
            check_names = system_responses["welcome"].get_names(text)
            for check_name in check_names:
                send(commands["vet"].check_user(check_name), group_id)
        """
    return responses
