# Use official Python image as base
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy Python dependencies file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder into container
COPY . .

# Expose port Flask runs on
EXPOSE 5000

# Start the Flask app
CMD ["python", "app/app.py"]
