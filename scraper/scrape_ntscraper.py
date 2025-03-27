from ntscraper import Nitter
# import pandas as pd

# Initialize the scraper
scraper = Nitter("https://nitter.net")

# Scrape tweets from a specific user
tweets_data = scraper.get_tweets("NASA", mode='user', number=5)
print(tweets_data)

# Inspecting the structure of the data
print(tweets_data.keys())
print(tweets_data['tweets'][0])

# Getting profile information
# profile_info = scraper.get_profile_info(username='elonmusk')
# print(profile_info)

# Creating a dictionary to store the tweet data
data = {
    'link': [],
    'text': [],
    'user': [],
    'likes': [],
    'retweets': [],
    'comments': []
}

# Extracting data from tweets
for tweet in tweets_data['tweets']:
    data['link'].append(tweet['link'])
    data['text'].append(tweet['text'])
    data['user'].append(tweet['user']['name'])
    data['likes'].append(tweet['stats']['likes'])
    data['retweets'].append(tweet['stats']['retweets'])
    data['comments'].append(tweet['stats']['comments'])

# Creating a DataFrame and saving to CSV
# df = pd.DataFrame(data)
# df.to_csv('prez.csv', index=False)
# print("Tweets saved to prez.csv")