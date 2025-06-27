import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    #App config
    APP_URL: str
    APP_PORT: int

    # AWS SES Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SES_REGION: str # Your SES region
    SES_SENDER_EMAIL: str # Your verified SES sender email

    #Slack setting
    SLACK_BOT_TOKEN: str
    SLACK_CLIENT_ID: str

    #DB setting
    DATABASE_URL: str

    #Password
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")

settings = Settings()