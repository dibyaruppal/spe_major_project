# Dockerfile for Flask API
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the Flask application code
COPY app.py inference.py /app/

# Expose port 5000 for the Flask API
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]