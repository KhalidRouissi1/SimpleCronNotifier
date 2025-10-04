from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Task model representing a scheduled or manual task."""

    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed
    log_file_path: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def duration(self) -> Optional[float]:
        """Calculate task duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def to_dict(self) -> dict:
        """Convert task to dictionary."""
        return {
            "name": self.name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "duration": self.duration,
            "log_file_path": self.log_file_path,
            "error_message": self.error_message
        }
