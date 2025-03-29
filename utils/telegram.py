import requests
from config.settings import settings
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Telegram() :
    """
    A utility class for sending messages to a Telegram group using the Telegram Bot API.

    Attributes:
        bot_token (str): The Telegram bot token.
        group_id (str): The Telegram group ID where messages will be sent.
    """

    def __init__(self):
        """
        Initializes the Telegram class with the bot token and group ID from settings.
        """
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.group_id = settings.TELEGRAM_GROUP_ID

    def escape_markdown(self, text):
        """
        Escapes special MarkdownV2 characters in the given text.

        Args:
            text (str): The text to escape.

        Returns:
            str: The escaped text.
        """
        logging.info("Escaping MarkdownV2 special characters.")
        escape_chars = r"_*[]()~`>#+-=|{}.!"
        return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    async def send_telegram_message(self, message):
        """
        Sends a message to the configured Telegram group.

        Args:
            message (str): The message to send.

        Returns:
            bool: True if the message was sent successfully, False otherwise.
        """
        logging.info("Preparing to send a message to Telegram.")
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        escaped_message = self.escape_markdown(message)
        payload = {
            "chat_id": self.group_id,
            "text": escaped_message,
            "parse_mode": "MarkdownV2"
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                logging.info("✅ Sent summary to Telegram successfully.")
                return True
            else:
                logging.error(f"❌ Failed to send message: {response.text}")
                return False
        
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ An error occurred while sending the message: {e}")