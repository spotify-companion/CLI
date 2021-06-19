import praw
import pandas as pd
import reddit_constants

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(client_id=reddit_constants.constants['client_id'], client_secret=reddit_constants.constants['secret_key'], user_agent=reddit_constants.constants['user_agent'])
        self.client_id = reddit_constants.constants['client_id']
        self.user_agent = reddit_constants.constants['user_agent']
        self.posts = {}
    
    def getHot(self, subreddit, limit=20):
        hot_posts = self.reddit.subreddit(subreddit).hot(limit=limit)
        titles = []
        for post in hot_posts:
            # print(post.title)
            titles.append(post.title)
        return hot_posts, titles
    

        



   