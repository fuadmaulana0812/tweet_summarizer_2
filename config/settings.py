from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    A class to manage configuration variables for the application.

    Attributes:
        API_KEY (str): The API key for the application.
        TWITTER_USERNAME (str): The Twitter username for login.
        TWITTER_EMAIL (str): The email associated with the Twitter account.
        TWITTER_PASSWORD (str): The password for the Twitter account.
        OPENAI_API_KEY (str): The API key for OpenAI services.
        OPENAI_MODEL (str): The OpenAI model to be used.
        TELEGRAM_BOT_TOKEN (str): The token for the Telegram bot.
        TELEGRAM_GROUP_ID (str): The Telegram group ID for notifications.

    Config:
        env_file (str): Specifies the path to the .env file for loading environment variables.
    """
    API_KEY: str

    TWITTER_USERNAME: str
    TWITTER_EMAIL: str
    TWITTER_PASSWORD: str

    OPENAI_API_KEY: str
    OPENAI_MODEL: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_GROUP_ID: str

    class Config:
        env_file = ".env"

# Instantiate the settings object
settings = Settings()
