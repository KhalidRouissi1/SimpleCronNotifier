# Automated Cron Supervisor with Slack Notifications

This project implements an AI Ops Agent designed to supervise Python task execution in a production-grade environment. It handles task scheduling, logging, and Slack notifications for completion or errors.

## Features

- **Scheduled Task Execution**: Runs a script multiple times daily at random intervals.
- **Comprehensive Logging**: Every run generates a unique log file capturing stdout, stderr, and timestamps.
- **Slack Notifications**: Sends real-time notifications to Slack on task completion (success or failure) with relevant details.
- **API for Manual Control**: A FastAPI service allows viewing logs and triggering manual task runs.
- **Containerized Deployment**: Fully Dockerized for consistent deployment across environments.
- **CI/CD with GitHub Actions**: Automates testing, Docker image building, and deployment to DigitalOcean.

## Project Structure

- `scheduler.py`: Handles cron job scheduling and random time generation for task execution.
- `runner.py`: Executes the main task, manages logging, and sends Slack notifications.
- `api.py`: FastAPI service for interacting with the system (viewing logs, triggering runs).
- `Dockerfile`: Defines the Docker image for the application.
- `docker-compose.yml`: Orchestrates the Docker containers for local development and deployment.
- `.github/workflows/deploy.yml`: GitHub Actions workflow for CI/CD.
- `docs/`: Contains detailed documentation (INSTALL.md, USAGE.md, ARCHITECTURE.md).
- `logs/`: Directory for storing task execution logs.

## Getting Started

Refer to the `docs/INSTALL.md` for deployment instructions and `docs/USAGE.md` for how to interact with the system.

## Development

### Prerequisites

- Docker
- Docker Compose
- Python 3. +

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd cronJob
    ```

2.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Access the API:**
    The FastAPI application will be available at `http://localhost:8000`.
    Access the API documentation at `http://localhost:8000/docs`.

### Running without Docker (for development/testing)

1.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Run the scheduler (example):**
    ```bash
    python scheduler.py
    ```

3.  **Run the runner (example):**
    ```bash
    python runner.py
    ```

4.  **Run the API:**
    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8000
    ```

## Configuration

- **Slack Webhook URL**: Set the `SLACK_WEBHOOK_URL` environment variable in your `docker-compose.yml` or deployment environment.

## Contributing

Contributions are welcome! Please refer to `CONTRIBUTING.md` (if available) for guidelines.
