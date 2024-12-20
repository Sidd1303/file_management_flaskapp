# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install flask boto3

# Expose Flask's default port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

