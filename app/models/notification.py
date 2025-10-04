import sqlite3
from datetime import datetime, date
from typing import Optional
from app.config.settings import Config
import os


class NotificationDatabase:
    """SQLite database to track daily Slack notifications."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize notification database.

        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = os.path.join(Config.LOG_DIR, "notifications.db")

        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Create notifications table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                count INTEGER DEFAULT 0,
                UNIQUE(date)
            )
        ''')

        conn.commit()
        conn.close()

    def get_today_count(self) -> int:
        """
        Get notification count for today.

        Returns:
            Number of notifications sent today
        """
        today = date.today().isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT count FROM notifications WHERE date = ?', (today,))
        result = cursor.fetchone()

        conn.close()

        return result[0] if result else 0

    def increment_today_count(self) -> int:
        """
        Increment today's notification count.

        Returns:
            Updated count for today
        """
        today = date.today().isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO notifications (date, count)
            VALUES (?, 1)
            ON CONFLICT(date) DO UPDATE SET count = count + 1
        ''', (today,))

        conn.commit()

        cursor.execute('SELECT count FROM notifications WHERE date = ?', (today,))
        result = cursor.fetchone()

        conn.close()

        return result[0] if result else 0

    def can_send_notification(self, max_per_day: int = 10) -> bool:
        """
        Check if we can send another notification today.

        Args:
            max_per_day: Maximum notifications allowed per day

        Returns:
            True if we can send, False otherwise
        """
        return self.get_today_count() < max_per_day

    def reset_old_records(self, days_to_keep: int = 30) -> None:
        """
        Clean up old notification records.

        Args:
            days_to_keep: Number of days of history to keep
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM notifications
            WHERE date < date('now', '-' || ? || ' days')
        ''', (days_to_keep,))

        conn.commit()
        conn.close()
