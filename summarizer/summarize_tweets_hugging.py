from transformers import pipeline
from datetime import datetime

# ✅ Summarization model from Hugging Face
summarizer = pipeline("summarization", model="t5-small")

async def process_tweets(tweet_data, start_datetime, end_datetime):
    # ✅ Calculate the number of hours between start and end
    hours = (end_datetime - start_datetime).seconds // 3600

    # ✅ Header
    output = f"BioDAO Updates in last {hours} hours ({start_datetime.strftime('%d %B %Y %H:%M')} – {end_datetime.strftime('%H:%M')})\n\n"

    for account, tweets in tweet_data.items():
        for tweet in tweets:
            tweet_text = tweet["tweet"]
            tweet_url = tweet["url"]

            # ✅ Summarize the tweet (if it's too long)
            if len(tweet_text) > 100:  # Adjust the length threshold if needed
                summary = summarizer(tweet_text, max_length=50, min_length=20, do_sample=False)[0]["summary_text"]
            else:
                summary = tweet_text  # Keep short tweets as is

            # ✅ Format the output
            output += f"* {account}\n{summary}\nOriginal tweet: {tweet_url}\n\n"

    return output.strip()
