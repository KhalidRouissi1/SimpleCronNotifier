import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    LOG_DIR = os.getenv("LOG_DIR", "./logs")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    CRON_SCHEDULE_MODE = os.getenv("CRON_SCHEDULE_MODE", "random")
    SLACK_NOTIFY_EVERY_MINUTE = os.getenv("SLACK_NOTIFY_EVERY_MINUTE", "False").lower() == "true"

    # Logging configuration
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories."""
        os.makedirs(cls.LOG_DIR, exist_ok=True)
