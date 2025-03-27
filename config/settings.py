from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    """
    Settings class to manage configuration variables for the application.
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

settings = Settings()
