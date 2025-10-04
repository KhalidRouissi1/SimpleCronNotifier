from fastapi import HTTPException
from app.models.task import Task
from app.services.task_service import TaskService
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class TaskController:
    """Controller for handling task-related requests."""

    def __init__(self, task_service: TaskService):
        """
        Initialize task controller.

        Args:
            task_service: Service for task execution
        """
        self.task_service = task_service

    def run_task(self, task_name: str) -> dict:
        """
        Execute a task manually.

        Args:
            task_name: Name of the task to execute

        Returns:
            Task execution result
        """
        logger.info(f"Manual task trigger requested: {task_name}")

        task = Task(name=task_name)
        executed_task = self.task_service.execute_task(task)

        return {
            "message": f"Task '{task_name}' executed",
            "status": executed_task.status,
            "log_file": executed_task.log_file_path,
            "duration": executed_task.duration,
            "error": executed_task.error_message
        }
