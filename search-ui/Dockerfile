# Use an official Node runtime as a parent image
FROM node:18

# Set the working directory to /app
WORKDIR /app

# Copy package.json and yarn.lock (or package-lock.json) first
COPY package*.json ./

# Install dependencies
RUN yarn install

# Copy the rest of the app's source code
COPY . .

# Expose port 3000
EXPOSE 3000

# Start the app
CMD ["yarn", "start"]
