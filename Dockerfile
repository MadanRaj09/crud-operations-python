# Use a minimal Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
