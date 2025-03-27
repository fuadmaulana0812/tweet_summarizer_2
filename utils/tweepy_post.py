import tweepy
from config.settings import settings

class TwitterAPI:
    def __init__(self):
        # Twitter API credentials
        self.API_KEY = settings.TWITTER_API_KEY
        self.API_SECRET = settings.TWITTER_API_SECRET
        self.ACCESS_TOKEN = settings.TWITTER_ACCESS_TOKEN
        self.ACCESS_SECRET = settings.TWITTER_ACCESS_TOKEN_SECRET

        # Authenticate with Twitter API
        auth = tweepy.OAuthHandler(self.API_KEY, self.API_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_SECRET)
        self.api = tweepy.API(auth)

    async def post_to_twitter(self, tweet_text):
        # Post a tweet
        tweet = self.api.update_status(tweet_text)

        # Print the tweet link
        tweet_url = f"https://twitter.com/{settings.TWITTER_USERNAME}/status/{tweet.id}"
        print(f"Tweet posted: {tweet_url}")

    async def post_thread(self, tweets):
        first_tweet = self.api.update_status(tweets[0])
        last_tweet_id = first_tweet.id

        for tweet in tweets[1:]:
            reply_tweet = self.api.update_status(tweet, in_reply_to_status_id=last_tweet_id)
            last_tweet_id = reply_tweet.id
        
            tweet_url = f"https://twitter.com/{settings.TWITTER_USERNAME}/status/{tweet.id}"
            print(f"Tweet posted: {tweet_url}")  # ✅ Print each tweet URL
