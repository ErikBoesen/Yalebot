from .base import Module
import os
import praw
import random


class Funny(Module):
    DESCRIPTION = "Get random meme from r/Memes"
    responses = []

    def __init__(self):
        super().__init__()
        self.reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),
                                  client_secret=os.environ.get("REDDIT_SECRET"),
                                  user_agent="yalebot")

    def response(self, query, message):
        if len(self.responses) == 0:
            for submission in self.reddit.subreddit("memes").hot(limit=25):
                if not submission.stickied and "jpg" in submission.url:
                    self.responses.append(submission.url)
            random.shuffle(self.responses)
        return self.responses.pop()
