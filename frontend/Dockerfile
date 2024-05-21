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
