import modules

static_commands = {
    "ping": "Pong!",
    "testing": "Join the Yalebot testing server: https://groupme.com/join_group/49940116/f2x20kxx",
    "add": "Add me to your own group here: https://yalebot.herokuapp.com",

    "sam": "❗❗❗N O 💪 F L E X 💪 Z O N E ❗❗❗",
    "test": "https://erikboesen.com/yalepuritytest",
    "shrug": r"¯\_(ツ)_/¯",
    "oh": ("", "https://i.groupme.com/766x750.jpeg.9209520c57e848369444ca498e31f90a.large"),
    "jah": ("", "https://i.groupme.com/766x750.jpeg.3eb07fe422db4b81947b634a1b309d48.large"),
    "bulldog": "Bulldog!  Bulldog!\nBow, wow, wow\nEli Yale\nBulldog!  Bulldog!\nBow, wow, wow\nOur team can never fail\n\nWhen the sons of Eli\nBreak through the line\nThat is the sign we hail\nBulldog!  Bulldog!\nBow, wow, wow\nEli Yale!",
    "flex": "👮🏽🚨🚔 PULL OVER 👮🏽🚨🚔\n\n😤Put your hands behind your back😤\n\n🗣I'm taking you into custody🗣\n\n📝And registering you as a📝\n\n🔥😩FLEX OFFENDER😩🔥",
    "ohno": ("", "https://i.groupme.com/1280x720.jpeg.f7c11a529a3b4a7195f71fa6be5ebfef.large"),
    "defuse": ("", "https://i.groupme.com/500x500.jpeg.26cbc006bcbf47048ade8a896b1e3d5a.large"),
    "cah": "Cards Against Humanity was recently removed from Yalebot and the game can now be run through Bot Against Humanity, a new separate bot which can be added at https://botagainsthumanitygroupme.herokuapp.com."
}

# "Explicit is better than implicit."
commands = {
    "about": modules.About(),
    "countdown": modules.Countdown(),
    "verify": modules.Verify(),
    "yalenews": modules.YaleNews(),
    "record": modules.Record(),
    "groups": modules.Groups(),
    "weather": modules.Weather(),
    "organizations": modules.Organizations(),
    "roomnumber": modules.RoomNumber(),
    "people": modules.People(),
    "admit": modules.Admit(),
    "shield": modules.Shield(),
    "laundry": modules.Laundry(),
    "colleges": modules.Colleges(),
    "randomcollege": modules.RandomCollege(),

    "meme": modules.Meme(),
    "damn": modules.Damn(),
    "jpeg": modules.JPEG(),
    "deepfry": modules.DeepFry(),
    "conversationstarter": modules.ConversationStarter(),
    "funfact": modules.FunFact(),
    "lyrics": modules.Lyrics(),
    "nasa": modules.NASA(),
    "cry": modules.Cry(),
    "xkcd": modules.XKCD(),
    "doge": modules.Doge(),
    "wideletters": modules.WideLetters(),
    "jake": modules.Jake(),
    "carlos": modules.Carlos(),
    "spaces": modules.Spaces(),
    "claps": modules.Claps(),
    "chat": modules.Chat(),
    "shakespeare": modules.Shakespeare(),
    "eightball": modules.EightBall(),
    "analytics": modules.Analytics(),
    "youtube": modules.YouTube(),
    "pick": modules.Pick(),
    "chose": modules.Chose(),
    "love": modules.Love(),
    "price": modules.Price(),
    "minion": modules.Minion(),
    "house": modules.House(),
    "location": modules.Location(),
    "twitter": modules.Twitter(),
    "tea": modules.Tea(),
    "capitalize": modules.Capitalize(),
    "uwu": modules.UWU(),
    "quote": modules.Quote(),
    "dog": modules.Dog(),
    "funny": modules.Funny(),
    "kelbo": modules.Kelbo(),
    "boink": modules.Boink(),
    "ship": modules.Ship(),
    "wholesome": modules.Wholesome(),
    "battery": modules.Battery(),
    "nato": modules.NATO(),
    "heaven": modules.Heaven(),
    "power": modules.Power(),
    "tictactoe": modules.TicTacToe(),
    "zalgo": modules.Zalgo(),
    "flip": modules.Flip(),
    "mccarthy": modules.McCarthy(),
    "circle": modules.Circle(),
    "anna": modules.Anna(),
    "handshake": modules.Handshake(),
    "dining": modules.Dining(),
    "building": modules.Building(),
    "course": modules.Course(),
    "iam": modules.IAm(),
    "compliment": modules.Compliment(),
    "poem": modules.Poem(),
    "lmgtfy": modules.LMGTFY(),
    "sad": modules.Sad(),
    "morse": modules.Morse(),
    "smol": modules.Smol(),
    "anagram": modules.Anagram(),
    "isitchickentendersday": modules.IsItChickenTendersDay(),
    "pdl": modules.PDL(),
    "coursename": modules.CourseName(),
}
commands["courses"] = commands["course"]
system_commands = {
    "welcome": modules.Welcome(),
    "mourn": modules.Mourn(),
    "introduce": modules.Introduce(),
}
