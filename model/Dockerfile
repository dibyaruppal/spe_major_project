# Dockerfile for Training Container
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the training script and any additional necessary files
COPY train.py /app/

# Default command to keep the container running
CMD ["sleep", "infinity"]