import tweepy
from config import t_access_token, t_access_token_secret, t_api_key, t_api_secret_key

class twitterBot:
    def __init__(self, message):
        self.message = message

    def tweet(self):
        auth = tweepy.OAuthHandler(t_api_key, t_api_secret_key) 
        auth.set_access_token(t_access_token, t_access_token_secret)

        bot = tweepy.API(auth)

        bot.update_status(self.message)

        return 'Tweeted message'

if __name__ == '__main__':
    text = 'test'
    twitterBot(text).tweet()
    