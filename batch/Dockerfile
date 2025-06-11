# batch/Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only what's needed
COPY common common

COPY batch/import_csv_runner.py batch/import_csv_runner.py
COPY batch/batch_runner.py batch/batch_runner.py
COPY batch/data_drift.py batch/data_drift.py
COPY batch/db.py batch/db.py
COPY batch/input_mock_data input_mock_data
COPY batch/requirements.txt batch/requirements.txt

COPY model model

# Install dependencies
RUN pip install --no-cache-dir -r batch/requirements.txt

# Run script
CMD ["python", "batch/batch_runner.py"]