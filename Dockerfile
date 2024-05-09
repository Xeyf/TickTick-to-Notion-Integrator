# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define arguments that can be passed at build time
ARG TICKTICK_ACCESS_TOKEN
ARG NOTION_TOKEN
ARG NOTION_DATABASE_ID
ARG PROJECT_IDS
ARG SYNC_INTERVAL

# Set environment variables from build arguments
ENV TICKTICK_ACCESS_TOKEN=${TICKTICK_ACCESS_TOKEN}
ENV NOTION_TOKEN=${NOTION_TOKEN}
ENV NOTION_DATABASE_ID=${NOTION_DATABASE_ID}
ENV PROJECT_IDS=${PROJECT_IDS}
ENV SYNC_INTERVAL=${SYNC_INTERVAL}

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "./main.py"]
