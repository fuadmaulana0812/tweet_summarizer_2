import requests
from config.settings import settings
import re

class Telegram() :
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.group_id = settings.TELEGRAM_GROUP_ID

    def escape_markdown(self, text):
        escape_chars = r"_*[]()~`>#+-=|{}.!"
        return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

    def format_links(self, text):
        return re.sub(r"(https?://\S+)", lambda match: match.group(0).replace("-", r"\-").replace(".", r"\."), text)

    async def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        escaped_message = self.escape_markdown(message)
        # formatted_message = self.format_links(escaped_message)
        payload = {
            "chat_id": self.group_id,
            "text": escaped_message,
            "parse_mode": "MarkdownV2"
        }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Sent summary to Telegram")
        else:
            print(f"❌ Failed to send message: {response.text}")