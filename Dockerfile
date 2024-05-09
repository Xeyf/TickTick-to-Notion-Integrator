# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Define build-time variables
ARG TICKTICK_ACCESS_TOKEN
ARG NOTION_TOKEN
ARG NOTION_DATABASE_ID
ARG PROJECT_IDS
ARG SYNC_INTERVAL

# Set them as environment variables for runtime
ENV TICKTICK_ACCESS_TOKEN=${TICKTICK_ACCESS_TOKEN} \
    NOTION_TOKEN=${NOTION_TOKEN} \
    NOTION_DATABASE_ID=${NOTION_DATABASE_ID} \
    PROJECT_IDS=${PROJECT_IDS} \
    SYNC_INTERVAL=${SYNC_INTERVAL}

# Copy the rest of your application's code
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["python", "./main.py"]
