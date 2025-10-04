from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from typing import List

from app.config.settings import Config
from app.utils.logger import setup_logger
from app.services.notification_service import NotificationService
from app.services.task_service import TaskService
from app.services.scheduler_service import SchedulerService
from app.controllers.task_controller import TaskController
from app.controllers.log_controller import LogController


Config.ensure_directories()
logger = setup_logger()
logger.info(f"Application started. LOG_DIR: {Config.LOG_DIR}")

app = FastAPI(title="Cron Job API", version="1.0.0")

notification_service = NotificationService()
task_service = TaskService(notification_service)
scheduler_service = SchedulerService(task_service, notification_service)

task_controller = TaskController(task_service)
log_controller = LogController()

scheduler_service.start()


@app.get("/", response_class=PlainTextResponse)
async def root():
    """Root endpoint with API information."""
    return "Welcome to the Cron Job API. Use /docs for API documentation."


@app.post("/run_task/{task_name}")
async def run_task_manually(task_name: str):
    """
    Trigger a task run manually.

    Args:
        task_name: Name of the task to execute

    Returns:
        Task execution details including log file path
    """
    return task_controller.run_task(task_name)


@app.get("/logs", response_model=List[str])
async def list_logs():
    """
    List all available log files.

    Returns:
        Sorted list of log file names (most recent first)
    """
    return log_controller.list_logs()


@app.get("/logs/{log_file_name}", response_class=PlainTextResponse)
async def get_log_content(log_file_name: str):
    """
    Get the content of a specific log file.

    Args:
        log_file_name: Name of the log file to retrieve

    Returns:
        Log file contents as plain text
    """
    return log_controller.get_log_content(log_file_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
