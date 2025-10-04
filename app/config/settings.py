import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LOG_DIR = os.getenv("LOG_DIR", "./logs")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    CRON_SCHEDULE_MODE = os.getenv("CRON_SCHEDULE_MODE", "random")
    SLACK_NOTIFY_EVERY_MINUTE = os.getenv("SLACK_NOTIFY_EVERY_MINUTE", "False").lower() == "true"

    LOG_MAX_BYTES = 10 * 1024 * 1024
    LOG_BACKUP_COUNT = 5

    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.LOG_DIR, exist_ok=True)
