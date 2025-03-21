# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the app directory
RUN mkdir /app
# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY spatest /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "spatest.wsgi:application"
