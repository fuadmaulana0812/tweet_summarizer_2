import openai
from datetime import datetime
from config.settings import settings
from langchain_openai import ChatOpenAI

async def process_tweets(tweet_data, start_datetime, end_datetime):
    # ✅ Calculate the number of hours between start and end
    hours = (end_datetime - start_datetime).seconds // 3600

    # ✅ Header
    output = f"Desci Updates in last {hours} hours ({start_datetime.strftime('%d %B %Y %H:%M')} – {end_datetime.strftime('%H:%M')})\n\n"

    for account, tweets in tweet_data.items():
        for tweet in tweets:
            tweet_text = tweet["tweet"]
            tweet_url = tweet["url"]

            # ✅ Summarize the tweet (if it's too long)
            print("Using OpenAI to summarize the tweet")
            llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model="gpt-4o-mini",
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
            response = llm.invoke(messages)
            summary = response.content

            # ✅ Format the output
            output += f"* {account}\n{summary}\nOriginal tweet: {tweet_url}\n\n"

    return output.strip()

# if __name__ == "__main__":
#     # ✅ Example usage
#     tweet_data = {
#         "elonmusk": [
#             {
#                 "tweet": "🤯 Rare Diseases = $1T+ market\n\n♻️ Drug Repurposing is the training set for AI Drug Discovery\n\n💊 Medicines are within reach\n\n🚶Kiddos are taking their first steps\n\n👀 Just watch the before vs after reel\n\n🚀 Turn crypto into $CURES moonshots\n\n🚨 AUCTION CLOSES IN 24 HOURS",
#                 "url": "https://twitter.com/elonmusk/status/1444645826638456321"
#             }
#         ]
#     }
#     start_datetime = datetime(2021, 10, 4, 12, 0)
#     end_datetime = datetime(2021, 10, 4, 13, 0)
#     print(process_tweets(tweet_data, start_datetime, end_datetime))