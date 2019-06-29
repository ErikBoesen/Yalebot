# Yalebot
[![Build Status](https://travis-ci.org/ErikBoesen/Yalebot.svg?branch=master)](https://travis-ci.org/ErikBoesen/Yalebot)

> A GroupMe chatbot for Yale University.

![Screenshot](screenshot.png)

To add this bot to your own server, go [here](https://yalebot.herokuapp.com)!

**NOTE:** This bot was formerly available for Discord and Facebook Messenger, but due to lack of use that functionality has been removed.

## Some notes
I would not recommend attempting to reuse this bot's code for your own. While I've licensed it under the GPL and invite you to borrow code at will under proper attribution, this bot is extremely complex, which a very large number of extraneous features that you probably don't want. If you want to use this bot yourself, it's quite easy to [add it to your own group](https://yalebot.herokuapp.com). If you're interested in creating your own GroupMe bot from scratch, start with [this tutorial](http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/). If you need practice in Python, I recommend [Codecademy's course](https://www.codecademy.com/learn/learn-python-3).

Cards Against Humanity was removed from this bot in May 2019, in favor of moving that functionality into Bot Against Humanity, a new bot without Yale baggage that can be used by all. Add it [here](https://botagainsthumanitygroupme.herokuapp.com)! [(GitHub)](https://github.com/ErikBoesen/BotAgainstHumanity)

## Design
Yalebot uses the [GroupMe Bots API](https://dev.groupme.com/tutorials/bots) for message exchange, hosting a Flask server which listens for incoming webhooks and decides on a response.

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
