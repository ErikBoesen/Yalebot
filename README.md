# Yalebot
[![Build Status](https://travis-ci.org/ErikBoesen/Yalebot.svg?branch=master)](https://travis-ci.org/ErikBoesen/Yalebot)

> A GroupMe chatbot for Yale University.

![Screenshot](screenshot.png)

To add this bot to your own server, go [here](https://yalebot.herokuapp.com)!

[Add to Discord server](https://discordapp.com/oauth2/authorize?client_id=576194237175955456&permissions=0&scope=bot)

## Design
Yalebot uses the [GroupMe Bots API](https://dev.groupme.com/tutorials/bots) for message exchange, hosting a Flask server which listens for incoming webhooks calculates on a response.

### Module structure
In order to keep code clean and maintainable, most bot systems are compartmentalized under the subdirectory `modules/`. Each contains a class that implements a method `response` taking as parameters the query (message text following command invocation) and raw message data from GroupMe. These modules inherit from the `Module` class. Class variables `DESCRIPTION` and `ARGC` should be assigned, giving a summary of component functions and the number of required arguments respectively. Each module must be instantiated in `bot.py`.

Static text responses are present in the `static_commands` dictionary in `bot.py`.

## Platform
Yalebot runs best on [Heroku](https://heroku.com).

To run Yalebot, you must provide your own API key for certain modules to function properly:

```sh
heroku config:set GROUPME_ACCESS_TOKEN=abcdef12345  # obtained from dev.groupme.com
```

After that, simply push the code via Heroku CLI and the bot will launch.

## Authorship
Yalebot was created by [Erik Boesen](https://github.com/ErikBoesen).

## License
[GPL](LICENSE)
