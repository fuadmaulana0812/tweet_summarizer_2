import asyncio
import schedule
from scraper.selenium_scraper import *
from summarizer.summarize_tweets_openai import *
# from summarizer.summarize_tweets_hugging import *
from utils.telegram import Telegram
from utils.utils import read_user

async def job():
    print("🔄 Running Scheduled Task...")

    # ✅ Get current time 
    time_loc = timezone(timedelta(hours=-5))
    end_datetime = datetime.now(time_loc)
    start_datetime = end_datetime - timedelta(hours=6)
    # start_datetime = datetime(2025, 3, 22, 19, 0, 0, tzinfo=time_loc)
    # end_datetime = datetime(2025, 3, 23, 0, 0, 0, tzinfo=time_loc)
    
    # ✅ Read Twitter accounts from Excel file
    user_list = await read_user()
    print(user_list[:3])

    # ✅ Initialize Selenium Scraper
    selenium_scraper = TwitterSelenium(start_datetime, end_datetime)
    selenium_scraper.setup_driver()

    if selenium_scraper.login():
        # ✅ Scrape tweets
        print("🔍 Scraping tweets...")
        tweets_data = await selenium_scraper.scrape_tweets(user_list)
        # print(tweets_data)

        # ✅ Process tweets (Assuming `process_tweets` is an async function)
        print("🔍 Processing tweets...")
        formatted_tweets = await process_tweets(tweets_data, start_datetime, end_datetime)
        print(formatted_tweets)

        # ✅ Post a Twitter thread
        print("🔍 Posting tweets...")
        await selenium_scraper.post_tweet(formatted_tweets)

        # ✅ Post to Telegram channel
        print("🔍 Posting to Telegram...")
        telegram = Telegram()
        await telegram.send_telegram_message(formatted_tweets)

    selenium_scraper.driver.quit()  # Close browser

# asyncio.run(job())

# ✅ Schedule the job at specific times (every 6 hours)
schedule.every().day.at("05:00").do(lambda: asyncio.run(job()))
schedule.every().day.at("11:00").do(lambda: asyncio.run(job()))
schedule.every().day.at("17:00").do(lambda: asyncio.run(job()))
schedule.every().day.at("23:00").do(lambda: asyncio.run(job()))

print("🕒 Scheduler started! Running job every 6 hours...")

# ✅ Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)  # Prevent high CPU usage