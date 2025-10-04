import logging
import os
import random
import time
from datetime import datetime
from app.config.settings import Config
from app.utils.logger import setup_logger
from app.services.notification_service import NotificationService
from app.models.task import Task


logger = setup_logger(__name__)


class TaskService:
    """Service layer for task execution with extensive logging."""

    def __init__(self, notification_service: NotificationService):
        """
        Initialize task service.

        Args:
            notification_service: Service for sending notifications
        """
        self.notification_service = notification_service

    def execute_task(self, task: Task) -> Task:
        """
        Execute a task with extensive logging.

        Args:
            task: Task model to execute

        Returns:
            Updated task model with execution results
        """
        task.start_time = datetime.now()
        task.status = "running"

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        task.log_file_path = os.path.join(Config.LOG_DIR, f"{task.name}_{timestamp}.log")

        task_logger = self._setup_task_logger(task.name, task.log_file_path)

        try:
            self._log_task_start(task_logger, task)
            self._execute_task_logic(task_logger, task.name)

            task.end_time = datetime.now()
            task.status = "completed"

            self._log_task_success(task_logger, task)
            self.notification_service.send_slack(
                f"Task '{task.name}' completed successfully in {task.duration:.2f}s\nLog: {task.log_file_path}",
                success=True
            )

        except Exception as e:
            task.end_time = datetime.now()
            task.status = "failed"
            task.error_message = str(e)

            self._log_task_failure(task_logger, task, e)
            self.notification_service.send_slack(
                f"Task '{task.name}' failed: {e}\nDuration: {task.duration:.2f}s\nLog: {task.log_file_path}",
                success=False
            )

        finally:
            self._cleanup_logger(task_logger)

        return task

    def _setup_task_logger(self, task_name: str, log_file_path: str) -> logging.Logger:
        """Setup task-specific logger."""
        task_logger = logging.getLogger(f"cronJob.task.{task_name}")
        task_logger.setLevel(logging.INFO)

        task_handler = logging.FileHandler(log_file_path)
        task_handler.setLevel(logging.INFO)
        task_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        task_handler.setFormatter(task_formatter)
        task_logger.addHandler(task_handler)

        return task_logger

    def _log_task_start(self, task_logger: logging.Logger, task: Task) -> None:
        """Log task start details."""
        task_logger.info("=" * 60)
        task_logger.info(f"TASK START: {task.name}")
        task_logger.info(f"Start Time: {task.start_time}")
        task_logger.info(f"Log File: {task.log_file_path}")
        task_logger.info("=" * 60)

        logger.info(f"Running task: {task.name} | Log: {task.log_file_path}")

        task_logger.info("Environment Details:")
        task_logger.info(f"  - Working Directory: {os.getcwd()}")
        task_logger.info(f"  - Log Directory: {Config.LOG_DIR}")
        task_logger.info(f"  - Cron Mode: {Config.CRON_SCHEDULE_MODE}")

    def _execute_task_logic(self, task_logger: logging.Logger, task_name: str) -> None:
        """Execute the actual task logic with detailed logging."""
        task_logger.info("-" * 60)
        task_logger.info("EXECUTING TASK LOGIC")
        task_logger.info(f"Simulating work for task '{task_name}'...")

        for i in range(1, 4):
            task_logger.info(f"  Step {i}/3: Processing...")
            time.sleep(0.1)
            task_logger.info(f"  Step {i}/3: Completed")

        if random.random() < 0.1:
            raise ValueError("Simulated task failure!")

    def _log_task_success(self, task_logger: logging.Logger, task: Task) -> None:
        """Log successful task completion."""
        task_logger.info("-" * 60)
        task_logger.info("TASK COMPLETED SUCCESSFULLY")
        task_logger.info(f"End Time: {task.end_time}")
        task_logger.info(f"Duration: {task.duration:.2f} seconds")
        task_logger.info("=" * 60)

        logger.info(f"Task '{task.name}' completed successfully in {task.duration:.2f}s")

    def _log_task_failure(self, task_logger: logging.Logger, task: Task, error: Exception) -> None:
        """Log task failure details."""
        task_logger.error("-" * 60)
        task_logger.error("TASK FAILED")
        task_logger.error(f"Error Type: {type(error).__name__}")
        task_logger.error(f"Error Message: {str(error)}")
        task_logger.error(f"End Time: {task.end_time}")
        task_logger.error(f"Duration Before Failure: {task.duration:.2f} seconds")
        task_logger.error("=" * 60)

        logger.error(f"Task '{task.name}' failed: {error} | Duration: {task.duration:.2f}s | Log: {task.log_file_path}")

    def _cleanup_logger(self, task_logger: logging.Logger) -> None:
        """Clean up task logger handlers."""
        for handler in task_logger.handlers[:]:
            handler.close()
            task_logger.removeHandler(handler)
