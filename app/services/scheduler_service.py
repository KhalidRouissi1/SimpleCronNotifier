import random
import pytz
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config.settings import Config
from app.utils.logger import setup_logger
from app.models.task import Task
from app.services.task_service import TaskService
from app.services.notification_service import NotificationService


logger = setup_logger(__name__)


class SchedulerService:
    """Service for managing scheduled task execution."""

    def __init__(self, task_service: TaskService, notification_service: NotificationService):
        """
        Initialize scheduler service.

        Args:
            task_service: Service for executing tasks
            notification_service: Service for sending notifications
        """
        self.task_service = task_service
        self.notification_service = notification_service
        self.scheduler = BackgroundScheduler()

    def _job_function(self) -> None:
        """Execute scheduled task."""
        execution_time = datetime.now(pytz.utc)
        logger.info(f"Scheduled job triggered at: {execution_time}")

        task = Task(name="scheduled_task")
        self.task_service.execute_task(task)

    def _minute_notification_job(self) -> None:
        """Send periodic Slack notifications every minute."""
        logger.info("Sending minute-by-minute Slack notification")
        self.notification_service.send_slack("Minute-by-minute heartbeat notification", success=True)

    def _random_notification_job(self) -> None:
        """Send random Slack notification."""
        logger.info("Sending random Slack notification")
        self.notification_service.send_slack("Random heartbeat notification", success=True)

    def _generate_random_times(self, num_runs: int = 10) -> list:
        """
        Generate random execution times within the next 24 hours.

        Args:
            num_runs: Number of random times to generate

        Returns:
            Sorted list of datetime objects
        """
        now = datetime.now()
        time_slots = []
        for _ in range(num_runs):
            random_seconds = random.randint(0, 24 * 3600)
            time_slots.append(now + timedelta(seconds=random_seconds))

        return sorted(time_slots)

    def _setup_fixed_schedule(self) -> None:
        """Setup fixed interval scheduling (every minute)."""
        logger.info("Scheduler mode: Fixed (every minute)")
        self.scheduler.add_job(
            self._job_function,
            CronTrigger(minute='*'),
            id='fixed_job',
            name='Fixed Scheduled Job'
        )

    def _setup_random_schedule(self, num_runs: int = 5) -> None:
        """
        Setup random scheduling.

        Args:
            num_runs: Number of random jobs to schedule
        """
        logger.info("Scheduler mode: Random")
        random_times = self._generate_random_times(num_runs=num_runs)
        for i, run_time in enumerate(random_times):
            logger.info(f"Scheduling job {i+1} at {run_time}")
            self.scheduler.add_job(
                self._job_function,
                'date',
                run_date=run_time,
                id=f'random_job_{i}',
                name=f'Random Scheduled Job {i}'
            )

    def _setup_slack_notifications(self) -> None:
        """Setup Slack notifications based on configuration."""
        if Config.SLACK_NOTIFY_EVERY_MINUTE:
            logger.info("Scheduling Slack notifications: EVERY MINUTE")
            self.scheduler.add_job(
                self._minute_notification_job,
                CronTrigger(minute='*'),
                id='minute_slack_notify',
                name='Minute Slack Notification'
            )
        else:
            logger.info("Scheduling Slack notifications: RANDOM (10 times per day)")
            random_times = self._generate_random_times(num_runs=10)
            for i, run_time in enumerate(random_times):
                logger.info(f"Scheduling Slack notification {i+1} at {run_time}")
                self.scheduler.add_job(
                    self._random_notification_job,
                    'date',
                    run_date=run_time,
                    id=f'random_slack_{i}',
                    name=f'Random Slack Notification {i}'
                )

    def start(self) -> None:
        """Start the scheduler with configured jobs."""
        # Setup main job schedule
        if Config.CRON_SCHEDULE_MODE == "fixed":
            self._setup_fixed_schedule()
        else:
            self._setup_random_schedule()

        # Setup Slack notifications
        self._setup_slack_notifications()

        # Start scheduler
        self.scheduler.start()
        logger.info("Scheduler started successfully")
