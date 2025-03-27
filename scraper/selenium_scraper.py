from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timezone, timedelta
import time
from config.settings import settings
import textwrap

class TwitterSelenium:
    def __init__(self, start_datetime, end_datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.username = settings.TWITTER_USERNAME
        self.password = settings.TWITTER_PASSWORD
        self.driver = None

    def setup_driver(self):
        print("🚀 Initializing web driver...")
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")  
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        options.add_argument("--disable-gpu")  
        options.add_argument("--window-size=1920,1080")  
        options.add_argument("--start-maximized")
        options.add_argument("--remote-debugging-port=9222")  

        # ✅ Manually specify Chromium binary
        options.binary_location = "/usr/bin/chromium"  

        # ✅ Set user agent (optional but correct format)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("✅ Web driver initialized!")

    def login(self):
        self.driver.get("https://twitter.com/login")
        time.sleep(3)
        try:
            username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
            username_field.send_keys(self.username)
            username_field.send_keys(Keys.RETURN)
            time.sleep(3)

            password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
            print("✅ Logged in successfully!")
        except:
            print("❌ Login failed!")
            self.driver.quit()
            return False
        return True

    async def scrape_tweets(self, users):
        """Scrape tweets from multiple users."""
        if isinstance(users, str):  # If only one user is given, convert it to a list
            users = [users]

        all_tweets = {}
        time_loc = timezone(timedelta(hours=-5))
        seen_urls = set() # Track seen URLs to avoid duplicates

        for user in users:
            print(f"🔍 Scraping tweets for @{user}...")
            self.driver.get(f"https://twitter.com/{user}")
            time.sleep(10)
            # WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
            
            tweets = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            user_tweets = []

            for tweet in tweets:
                try:
                    tweet_text_element = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                    if not tweet_text_element:
                        print(f"⚠️ No tweet text found for @{user}, skipping...")
                        continue
                    tweet_text = tweet_text_element.text
                    timestamp_element = tweet.find_element(By.XPATH, './/time')
                    tweet_time = timestamp_element.get_attribute("datetime")
                    tweet_datetime = datetime.strptime(tweet_time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).astimezone(time_loc)
                    
                    # ✅ Extract tweet ID from the tweet link
                    tweet_link_element = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
                    tweet_link = tweet_link_element.get_attribute("href")

                    if user not in tweet_link:
                        print(f"⚠️ Skipping tweet not from @{user}: {tweet_link}")
                        continue

                    # Check if the URL is already processed
                    if tweet_link in seen_urls:
                        print(f"⚠️ Duplicate tweet found: {tweet_link}, skipping...")
                        continue

                    # Add the URL to the seen set
                    seen_urls.add(tweet_link)

                    if self.start_datetime <= tweet_datetime <= self.end_datetime:
                        user_tweets.append({
                            "user": user,
                            "date_time": tweet_datetime,
                            "tweet": tweet_text,
                            "url": tweet_link
                        })
                except Exception as e:
                    print(f"❌ Error parsing tweet from @{user}: {e}")
            all_tweets[user] = user_tweets

        return all_tweets
    
    async def post_tweet(self, tweet_text):
        """Function to post a tweet using Selenium."""
        if not self.driver:
            print("❌ Web driver not initialized. Call `setup_driver()` first.")
            return False

        print("✍️ Posting tweet...")
        try:
            self.driver.get("https://twitter.com/home")
            time.sleep(5)

            # Locate tweet box and enter text
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Post text"]'))
            )
            tweet_box.send_keys(tweet_text)
            time.sleep(2)

            # Click the tweet button
            tweet_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="tweetButtonInline"]'))
            )
            tweet_button.click()

            print("✅ Tweet posted successfully!")
            return True

        except Exception as e:
            print(f"❌ Error posting tweet: {e}")
            return False

    def post_tweet_reply(self, tweet_text, in_reply_to):
        """Post a reply tweet in a thread."""
        print(f"💬 Posting reply to {in_reply_to}...")
        self.driver.get(f"https://twitter.com/intent/tweet?in_reply_to={in_reply_to}")
        time.sleep(5)

        try:
            # Locate tweet box and enter text
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Post text"]'))
            )
            tweet_box.send_keys(tweet_text)
            time.sleep(2)

            # Click the tweet button
            tweet_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="tweetButton"]'))
            )
            tweet_button.click()

            print("✅ Reply posted successfully!")
            return True

        except Exception as e:
            print(f"❌ Error posting reply: {e}")
            return False
    
    def post_thread(self, full_text):
        """Posts a thread if the text exceeds 280 characters."""
        tweets = textwrap.wrap(full_text, width=270)  # Leave room for numbering
        first_tweet_id = None

        for index, tweet in enumerate(tweets):
            numbered_tweet = f"{tweet} ({index+1}/{len(tweets)})"
            print(numbered_tweet)

            # ✅ If it's the first tweet, post normally
            if index == 0:
                tweet_id = self.post_tweet(numbered_tweet)  # Post first tweet
                first_tweet_id = tweet_id
            else:
                self.post_tweet_reply(numbered_tweet, first_tweet_id)  # Reply to first tweet

    def run(self, users):
        self.setup_driver()
        if not self.login():
            return []
        tweets = self.scrape_tweets(users)
        self.driver.quit()
        return tweets
