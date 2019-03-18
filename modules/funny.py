from .base import Module
import os
import praw
import random

class Funny(Module):
    DESCRIPTION = "Get random meme from r/Memes"
    def response(self, query, message):
        reddit = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"],
                             client_secret=os.environ["REDDIT_SECRET"],
                             user_agent='yalebot')
        response = []
        for submission in reddit.subreddit('memes').hot(limit=25):
            if not submission.stickied and 'jpg' in submission.url:
                response.append(submission.url)
        return random.choice(response)
