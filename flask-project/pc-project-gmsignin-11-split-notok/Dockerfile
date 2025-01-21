# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port that Flask runs on
EXPOSE 5000

# Initialize the database and run the application using Gunicorn
CMD ["sh", "-c", "python app.py --setup && gunicorn -w 4 -b 0.0.0.0:5000 main:app"]
