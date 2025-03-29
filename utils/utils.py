import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def read_user():
    """
    Reads the user data from the 'user.json' file and extracts the list of usernames.

    Returns:
        list: A list of usernames extracted from the 'user.json' file.
    """
    try:
        logging.info("Reading user data from 'user.json'.")
        with open("user.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    
        # Extract the list of usernames
        user_list = [user["username"] for user in data]
        logging.info(f"Successfully extracted {len(user_list)} usernames.")
        return user_list
    except FileNotFoundError:
        logging.error("❌ 'user.json' file not found.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"❌ Error decoding JSON: {e}")
        return []
    except Exception as e:
        logging.error(f"❌ An unexpected error occurred: {e}")
        return []

async def export_txt(formatted_tweets):
    """
    Exports the formatted tweets to the 'output_tweets.txt' file.

    Args:
        formatted_tweets (str): The formatted tweets to be written to the file.
    """
    try:
        logging.info("Exporting tweets to 'output_tweets.txt'.")
        with open("output_tweets.txt", "a", encoding="utf-8") as f:
            f.write("\n\n\n")
            f.write(formatted_tweets)
        logging.info("✅ Tweets exported successfully to 'output_tweets.txt'.")
    except Exception as e:
        logging.error(f"❌ An error occurred while exporting tweets: {e}")