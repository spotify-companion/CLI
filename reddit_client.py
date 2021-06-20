import praw
import pandas as pd
import reddit_constants

class RedditClient(object):
    __shared_instance = "RedditClient"

    @staticmethod
    def get_instance():
        """ To implement singleton pattern """ 
        if RedditClient.__shared_instance == "RedditClient":
            RedditClient()
        
        return RedditClient.__shared_instance

    def __init__(self):
        if RedditClient.__shared_instance != "RedditClient":
            raise Exception("Sorry this is a singleton implementation")
        else:
            RedditClient.__shared_instance =self
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

    def get_songs(self):
        songlist, titles = self.reddit_client.getHot('listentothis', 20)
        songs = []
        for i in titles:
                if ' -- ' in i:
                    i = i.split(' -- ')
                elif ' - ' in i:
                    i = i.split(' - ')
                elif ' — ' in i:
                    i = i.split(' — ')
                # print(i[len(i)-1].split(' [')[0])
                temp = {'artist': i[0], 'title': i[len(i)-1].split(' [')[0]}
                songs.append(temp)
        return songs

        



   