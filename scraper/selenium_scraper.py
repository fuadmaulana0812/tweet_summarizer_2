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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TwitterSelenium:
    """
    A class to interact with Twitter using Selenium for tasks such as login, scraping tweets, and posting tweets.

    Attributes:
        start_datetime (datetime): The start date and time for filtering tweets.
        end_datetime (datetime): The end date and time for filtering tweets.
        username (str): The Twitter username for login.
        password (str): The Twitter password for login.
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    def __init__(self, start_datetime, end_datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.username = settings.TWITTER_USERNAME
        self.password = settings.TWITTER_PASSWORD
        self.driver = None

    def setup_driver(self):
        """
        Initializes the Selenium WebDriver with the required options.
        """
        logging.info("🚀 Initializing web driver...")
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
        logging.info("✅ Web driver initialized!")

    def login(self):
        """
        Logs into Twitter using the provided username and password.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        logging.info("🔑 Attempting to log in to Twitter...")
        self.driver.get("https://twitter.com/login")
        time.sleep(5)
        try:
            username_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
            username_field.send_keys(self.username)
            username_field.send_keys(Keys.RETURN)
            time.sleep(5)

            # Check if Twitter asks for email
            try:
                email_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "text")))
                email_field.send_keys(settings.TWITTER_EMAIL)  # Use email from settings
                email_field.send_keys(Keys.RETURN)
                time.sleep(5)
            except:
                logging.info("✅ Email step not required.")

            password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
            logging.info("✅ Logged in successfully!")
            return True
        except Exception as e:
            logging.error(f"❌ Login failed: {e}")
            self.driver.quit()
            return False

    async def scrape_tweets(self, users):
        """
        Scrapes tweets from the specified users within the date range.

        Args:
            users (list or str): A list of Twitter usernames or a single username.

        Returns:
            dict: A dictionary containing tweets for each user.
        """
        if isinstance(users, str):  # If only one user is given, convert it to a list
            users = [users]

        logging.info("🔍 Starting tweet scraping...")
        all_tweets = {}
        time_loc = timezone(timedelta(hours=-5))
        seen_urls = set() # Track seen URLs to avoid duplicates

        for user in users:
            logging.info(f"🔍 Scraping tweets for @{user}...")
            self.driver.get(f"https://twitter.com/{user}")
            time.sleep(10)
            
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

                    if user not in tweet_link or tweet_link in seen_urls:
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
                    logging.error(f"❌ Error parsing tweet from @{user}: {e}")
            all_tweets[user] = user_tweets

        logging.info("✅ Tweet scraping completed!")
        return all_tweets
    
    async def post_tweet(self, tweet_text):
        """
        Posts a tweet using Selenium.

        Args:
            tweet_text (str): The text of the tweet to post.

        Returns:
            bool: True if the tweet is posted successfully, False otherwise.
        """
        if not self.driver:
            logging.error("❌ Web driver not initialized. Call `setup_driver()` first.")
            return False

        logging.info("✍️ Posting tweet...")
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

            logging.info("✅ Tweet posted successfully!")
            return True

        except Exception as e:
            logging.error(f"❌ Error posting tweet: {e}")
            return False

    def run(self, users):
        """
        Runs the Selenium scraper to log in and scrape tweets.

        Args:
            users (list): A list of Twitter usernames to scrape tweets from.

        Returns:
            dict: A dictionary containing tweets for each user.
        """
        self.setup_driver()
        if not self.login():
            return {}
        tweets = self.scrape_tweets(users)
        self.driver.quit()
        return tweets
