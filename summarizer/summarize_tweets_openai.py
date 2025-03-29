import logging
from datetime import datetime
from config.settings import settings
from langchain_openai import ChatOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def process_tweets(tweet_data, start_datetime, end_datetime):
    """
    Processes and summarizes tweets using OpenAI's language model.

    Args:
        tweet_data (dict): A dictionary containing tweet data. 
                           Keys are account names, and values are lists of tweets.
        start_datetime (datetime): The start datetime for the tweet range.
        end_datetime (datetime): The end datetime for the tweet range.

    Returns:
        str: A formatted string containing summarized tweets.
    """
    try:
        # ✅ Calculate the number of hours between start and end
        hours = (end_datetime - start_datetime).seconds // 3600
        logging.info(f"Processing tweets for the last {hours} hours.")

        # ✅ Header for the output
        output = f"BioDAO Updates in last {hours} hours ({start_datetime.strftime('%d %B %Y %H:%M')} – {end_datetime.strftime('%H:%M')})\n\n"

        for account, tweets in tweet_data.items():
            logging.info(f"Processing tweets for account: {account}")
            for tweet in tweets:
                tweet_text = tweet["tweet"]
                tweet_url = tweet["url"]

                # ✅ Summarize the tweet using OpenAI
                logging.info("Using OpenAI to summarize the tweet.")
                llm = ChatOpenAI(
                    api_key=settings.OPENAI_API_KEY,
                    model=settings.OPENAI_MODEL,
                    temperature=0.5,
                )
                messages = [
                    (
                        "system",
                        "You are a helpful assistant that summarizes tweets"
                    ),
                    (
                        "user",
                        f"Summarize this tweet in a concise way: {tweet_text}"
                    )
                ]

                try:
                    response = llm.invoke(messages)
                    summary = response.content
                    logging.info("Tweet summarized successfully.")
                except Exception as e:
                    logging.error(f"Error summarizing tweet: {e}")

                # ✅ Format the output
                output += f"* {account}\n{summary}\nOriginal tweet: {tweet_url}\n\n"

        logging.info("Tweet processing completed successfully.")
        return output.strip()
    
    except Exception as e:
        logging.error(f"An error occurred while processing tweets: {e}")