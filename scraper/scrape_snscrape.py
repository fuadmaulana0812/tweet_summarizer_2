import snscrape.modules.twitter as sntwitter
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

username = "vita_dao"
tweets = []

# Scrape the latest 10 tweets from NASA
# for tweet in sntwitter.TwitterUserScraper(username).get_items():
for tweet in sntwitter.TwitterSearchScraper(f"from:{username} since:2025-03-09 until:2025-03-10").get_items():
    if len(tweets) >= 10:  # Limit to 10 tweets
        break
    tweets.append({"date": tweet.date, "content": tweet.content})

# Print the tweets
for tweet in tweets:
    print(tweet["date"], "-", tweet["content"])