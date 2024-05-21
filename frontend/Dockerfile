# Step 1: Build the React application
FROM node:16 AS build

WORKDIR /app

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
RUN npm install

COPY . /app

# Ensure the build command is correct and outputs to the /app/dist directory
RUN npm run build && ls -al /app/dist

# Step 2: Serve the React app using a lightweight web server
FROM node:16

WORKDIR /app

# Install the serve package globally
RUN npm install -g serve

# Copy the build output from the previous stage
COPY --from=build /app/dist /app/dist

EXPOSE 3000

# Use serve to serve the static files
CMD ["serve", "-s", "dist", "-l", "3000"]







# # Step 1: Build the React application
# FROM node:16 AS build

# WORKDIR /app

# COPY package.json /app/package.json
# COPY package-lock.json /app/package-lock.json
# RUN npm install

# COPY . /app

# # Ensure the build command is correct and outputs to the /app/dist directory
# RUN npm run build && ls -al /app/dist

# # Step 2: Serve the React app using a lightweight web server
# FROM node:16

# WORKDIR /app

# # Install the serve package globally
# RUN npm install -g serve

# # Copy the build output from the previous stage
# COPY --from=build /app/dist /app/build

# EXPOSE 3000

# # Use serve to serve the static files
# CMD ["serve", "-s", "build", "-l", "3000"]










# # Step 1: Build the React application
# FROM node:16 AS build

# WORKDIR /app

# COPY package.json /app/package.json
# COPY package-lock.json /app/package-lock.json
# RUN npm install

# COPY . /app

# RUN npm run build && ls -al /app/dist

# # Step 2: Serve the React app using a lightweight web server and tunnel it with ngrok
# FROM node:16

# # Install a simple web server for serving static files
# RUN npm install -g serve

# # Install ngrok
# RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip && \
#     unzip ngrok-stable-linux-amd64.zip && \
#     mv ngrok /usr/local/bin/ngrok && \
#     rm ngrok-stable-linux-amd64.zip

# WORKDIR /app

# COPY --from=build /app/dist /app/build

# EXPOSE 80

# # Start the server and ngrok
# CMD serve -s build & ngrok http 5000 --log=stdout

# ghgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg

# # Dockerfile for Flask API
# FROM python:3.9-slim

# # Set environment variables
# ENV PYTHONUNBUFFERED=1

# # Create and set working directory
# WORKDIR /app

# # Copy requirements.txt and install dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# # Copy the Flask application code
# COPY app.py inference.py /app/

# # Expose port 5000 for the Flask API
# EXPOSE 5000

# # Run the Flask application
# CMD ["python", "app.py"]
