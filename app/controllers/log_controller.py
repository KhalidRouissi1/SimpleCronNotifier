import os
from fastapi import HTTPException
from typing import List
from app.config.settings import Config
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class LogController:
    """Controller for handling log-related requests."""

    def list_logs(self) -> List[str]:
        """
        List all available log files.

        Returns:
            Sorted list of log file names (most recent first)
        """
        try:
            log_files = [f for f in os.listdir(Config.LOG_DIR) if f.endswith(".log")]
            logger.info(f"Listed {len(log_files)} log files")
            return sorted(log_files, reverse=True)
        except FileNotFoundError:
            logger.error(f"Log directory not found: {Config.LOG_DIR}")
            raise HTTPException(status_code=404, detail="Log directory not found.")

    def get_log_content(self, log_file_name: str) -> str:
        """
        Get the content of a specific log file.

        Args:
            log_file_name: Name of the log file to retrieve

        Returns:
            Log file contents as plain text
        """
        log_file_path = os.path.join(Config.LOG_DIR, log_file_name)

        if not os.path.exists(log_file_path):
            logger.warning(f"Log file not found: {log_file_name}")
            raise HTTPException(status_code=404, detail="Log file not found.")

        try:
            with open(log_file_path, "r") as f:
                content = f.read()
            logger.info(f"Retrieved log file: {log_file_name}")
            return content
        except Exception as e:
            logger.error(f"Error reading log file {log_file_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Error reading log file: {e}")
