# ML-Ops Mid-Project

This project demonstrates a machine learning operations (MLOps) workflow using Docker, GitHub Actions, and Python. It includes batch jobs for importing CSV data and running batch processing, as well as an API for model inference.

## Project Structure

- `api/` - REST API for model inference
- `batch/` - Batch processing scripts and jobs
- `common/` - Shared code (models, preprocessing, etc.)
- `model/` - Trained model and stats
- `logs/` - Log files
- `docker-compose.yml` - Docker Compose configuration
- `.github/workflows/batch-jobs.yml` - GitHub Actions workflow for CI/CD and batch jobs

## Main Workflows

- **Import CSV**: Loads CSV data into the database using Docker Compose.
- **Scheduled Batch**: Runs batch processing jobs on a schedule or manually via GitHub Actions.
- **Api**: Exposes a REST API for model inference. The API is implemented in `api/app.py` and can be run as a Docker container. It allows you to send data and receive predictions from the trained model.

## Usage

### Running Locally

1. Clone the repository.
2. Set up your `.env` file or provide required environment variables (e.g., `MONGO_URI`).
3. Use Docker Compose to start services:
   ```sh
   docker-compose up --build
   ```

### GitHub Actions

- The workflow supports manual and scheduled runs for both import and batch jobs.
- You can trigger jobs from the Actions tab in GitHub.

- There is currently a problem with the Action implantation.

## Requirements

- Docker & Docker Compose
- Python 3.10+
