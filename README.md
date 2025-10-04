# Simple Cron Notifier

Production-grade FastAPI application for scheduled task execution with Slack notifications, extensive logging, and automated monitoring.

## Features

- **Scheduled Task Execution**: Random or fixed interval scheduling
- **Extensive Logging**: Unique log file per task run with detailed metrics
- **Slack Notifications**: Real-time notifications with daily limits (10/day)
- **RESTful API**: View logs and trigger manual task runs
- **MVC Architecture**: Clean separation with SOLID principles
- **SQLite Tracking**: Notification limits and history
- **Docker Support**: Containerized deployment

## Architecture

```
app/
├── config/          Configuration management
├── models/          Data models (Task, NotificationDatabase)
├── controllers/     API request handlers
├── services/        Business logic
└── utils/           Logging utilities
```

## Quick Start

### Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Docker

```bash
docker-compose up -d --build
```

## Configuration

Create `.env`:

```env
SLACK_WEBHOOK_URL=your-webhook-url
LOG_DIR=./logs
CRON_SCHEDULE_MODE=random
SLACK_NOTIFY_EVERY_MINUTE=False
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome |
| POST | `/run_task/{name}` | Execute task |
| GET | `/logs` | List logs |
| GET | `/logs/{file}` | View log |
| GET | `/docs` | API documentation |

## Deployment

Server: **159.89.28.26:8001**

```bash
ssh root@159.89.28.26
curl -fsSL https://get.docker.com | sh
git clone https://github.com/KhalidRouissi1/SimpleCronNotifier.git
cd SimpleCronNotifier
nano .env
docker-compose up -d --build
```

Access: http://159.89.28.26:8001/docs

## License

MIT
