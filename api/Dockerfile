# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the common directory
COPY common common

# Copy the model directory
COPY model model

# Copy the application code
COPY api/app.py api/app.py

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "api/app.py"]
