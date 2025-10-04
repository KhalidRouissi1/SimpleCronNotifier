import requests
from datetime import datetime
from app.config.settings import Config
from app.utils.logger import setup_logger
from app.models.notification import NotificationDatabase


logger = setup_logger(__name__)


class NotificationService:
    """Handles external notifications (Slack, etc.)."""

    def __init__(self):
        """Initialize notification service with database."""
        self.db = NotificationDatabase()

    def send_slack(self, message: str, success: bool = True, force: bool = False) -> None:
        """
        Send notification to Slack webhook with daily limit.

        Args:
            message: Notification message
            success: Whether this is a success or failure notification
            force: Force send ignoring daily limit
        """
        if not Config.SLACK_WEBHOOK_URL:
            logger.warning("SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
            return

        if not force and not self.db.can_send_notification(max_per_day=10):
            logger.info("Daily Slack notification limit reached (10/day). Skipping notification.")
            return

        icon = ":white_check_mark:" if success else ":x:"
        color = "#36a64f" if success else "#ff0000"

        payload = {
            "attachments": [
                {
                    "fallback": message,
                    "color": color,
                    "pretext": f"{icon} Task Notification",
                    "text": message,
                    "ts": datetime.now().timestamp()
                }
            ]
        }

        try:
            response = requests.post(Config.SLACK_WEBHOOK_URL, json=payload, timeout=10)
            response.raise_for_status()

            count = self.db.increment_today_count()
            logger.info(f"Slack notification sent ({count}/10 today): {message}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Slack notification: {e}")
