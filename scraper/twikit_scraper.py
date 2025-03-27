from twikit import Client
from datetime import datetime, timezone, timedelta
from config.settings import settings
import asyncio

USERNAME = settings.TWITTER_USERNAME
# EMAIL = settings.TWITTER_EMAIL
PASSWORD = settings.TWITTER_PASSWORD

try:
    Client.clear_cache()
except:
    pass

# Initialize client
client = Client('en-US')

async def fetch_tweet(username, start_datetime=None, end_datetime=None, time=5):
    user = await client.get_user_by_screen_name(username)
    print(f"Fetching tweets from {user.name} ({user.id})...")

    # ✅ Get current time in WIB (UTC+7)
    WIB = timezone(timedelta(hours=7))

    # ✅ Convert provided start and end times to WIB
    if end_datetime:
        end_datetime = end_datetime.astimezone(WIB)
    else:
        end_datetime = datetime.now(WIB)  # Default: now
    
    if start_datetime:
        start_datetime = start_datetime.astimezone(WIB)
    else:
        start_datetime = end_datetime - timedelta(hours=time)  # Default: 5 hours ago

    tweets = await client.get_user_tweets(user.id, 'Tweets')

    result = []
    for tweet in tweets:
        tweet_result = {}
        # ✅ Convert Twitter timestamp to datetime
        tweet_date = datetime.strptime(tweet.created_at, "%a %b %d %H:%M:%S %z %Y")

        # ✅ Convert tweet_date to WIB before comparing
        tweet_date_wib = tweet_date.astimezone(WIB)

        # ✅ Check if the tweet falls within the given range
        if (not start_datetime or tweet_date_wib >= start_datetime) and tweet_date_wib <= end_datetime:
            tweet_result["date_time"] = tweet_date_wib
            tweet_result["tweet"] = tweet.text
            tweet_result["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
            result.append(tweet_result)

    return result, start_datetime, end_datetime

async def scraper(usernames, start_datetime=None, end_datetime=None, time=5):  
    if isinstance(usernames, str):  
        usernames = [usernames]  # Convert single username to a list

    await client.login(
        auth_info_1=USERNAME,
        # auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

    tweets_data = {}
    for user in usernames:
        tweets_data[user], start_datetime, end_datetime = await fetch_tweet(user, start_datetime, end_datetime)
        await asyncio.sleep(5)
        
    return tweets_data, start_datetime, end_datetime

async def post_to_twitter(text):
    # ✅ Ensure user is logged in
    await client.login(
        auth_info_1=USERNAME,
        # auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

    # ✅ Post the tweet
    tweet = await client.create_tweet(text)
    
    # ✅ Generate tweet link
    tweet_url = f"https://twitter.com/{USERNAME}/status/{tweet.id}"
    
    print(f"Tweet posted: {tweet_url}")  # ✅ Print tweet link

async def post_twitter_thread(text):
    # ✅ Ensure user is logged in
    await client.login(
        auth_info_1=USERNAME,
        # auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

    # ✅ Split text into chunks of 280 characters
    chunks = [text[i:i+280] for i in range(0, len(text), 280)]

    previous_tweet = None
    for chunk in chunks:
        tweet = await client.create_tweet(chunk, reply_to=previous_tweet.id if previous_tweet else None)
        tweet_url = f"https://twitter.com/{USERNAME}/status/{tweet.id}"
        
        print(f"Tweet posted: {tweet_url}")  # ✅ Print each tweet URL
        previous_tweet = tweet  # Store last tweet for threading

