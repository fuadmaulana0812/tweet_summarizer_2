from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Function to scrape tweets from Google Search
def scrape_tweets_from_google(query, num_results=10):
    search_query = f'site:twitter.com "{query}"'
    tweet_links = []

    for url in search(search_query, num_results=num_results):
        if "twitter.com" in url and "/status/" in url:
            tweet_links.append(url)

    return tweet_links

# Example: Get Elon Musk's latest tweets
tweet_urls = scrape_tweets_from_google('from:elonmusk', num_results=5)

# Print tweet links
for url in tweet_urls:
    print(url)

def get_tweet_text(tweet_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(tweet_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tweet_text = soup.find('meta', {'name': 'description'})['content']
        return tweet_text
    else:
        return "Failed to retrieve tweet."

# Example: Get text from first tweet
tweet_text = get_tweet_text(tweet_urls[0])
print(tweet_text)
