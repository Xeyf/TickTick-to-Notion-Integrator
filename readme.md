
# Syncing Tasks from TickTick to Notion

This application synchronizes tasks from TickTick to a Notion database. Follow this guide to set up and use the application.

## Requirements

- Docker
- A TickTick account
- A Notion account with API access

## Setup

### 1. TickTick Configuration

To access TickTick tasks via the API, follow these steps:

#### Get TickTick Access Token

1. **Create an App on TickTick Developer Portal:**
   - Go to [TickTick Developer Portal](https://developer.ticktick.com/docs#/openapi) and create a new app.
   - Set a Redirect URI (you can use `http://localhost:YOUR_PORT` where `YOUR_PORT` is a port on your local machine).

2. **Get Authorization Code:**
   - Make a GET request to the following URL to initiate the OAuth flow:
     ```
     https://ticktick.com/oauth/authorize?client_id=YOUR_CLIENT_ID&scope=tasks:read&redirect_uri=YOUR_REDIRECT_URI&response_type=code
     ```
   - Replace `YOUR_CLIENT_ID` and `YOUR_REDIRECT_URI` with your values.
   - Login and authorize your app. You will be redirected to your redirect URI with a `code` parameter in the URL.

3. **Retrieve TickTick API Token:**
   - With the code obtained from the previous step, make a POST request to obtain the access token:
     ```bash
     curl -X POST https://ticktick.com/oauth/token \
     -u CLIENT_ID:CLIENT_SECRET \
     -d grant_type=authorization_code \
     -d code=YOUR_AUTHORIZATION_CODE \
     -d redirect_uri=YOUR_REDIRECT_URI
     ```
   - Replace `CLIENT_ID`, `CLIENT_SECRET`, `YOUR_AUTHORIZATION_CODE`, and `YOUR_REDIRECT_URI` with your respective details.

#### Retrieve TickTick Project IDs

- To get project IDs from TickTick, make a GET request:
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://api.ticktick.com/open/v1/project
  ```
- Extract the `id` field from each project you want to synchronize.

### 2. Notion Configuration

To write tasks to a Notion database, follow these steps:

1. **Create an Integration:**
   - Go to [My Integrations](https://www.notion.so/my-integrations) on Notion.
   - Click the "+ New Integration" button.
   - Name your integration and grant it access to the workspace.
   - Copy the "Internal Integration Token" that appears after you save.

2. **Share Database with Integration:**
   - Find the Notion database where you want to sync your tasks.
   - Click "Share" on the top right and invite the integration using the "Invite" button.

3. **Get the Database ID:**
   - The database ID can be extracted from the URL when you are viewing the database.
   - The URL format is `https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`.
   - Copy the `database_id`.

### 3. Set Up Environment Variables

Create a `.env` file in your project directory with the following content:

```plaintext
TICKTICK_ACCESS_TOKEN=your_ticktick_access_token_here
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_notion_database_id_here
PROJECT_IDS=project_id1,project_id2,project_id3
```

Replace the placeholders with your actual information.

### 4. Docker Configuration

1. **Build the Docker Image:**


Now, build your Docker image with the `SYNC_INTERVAL` and other parameters:

```bash
docker run -p 80:80 \
  -e TICKTICK_ACCESS_TOKEN="your_ticktick_access_token_here" \
  -e NOTION_TOKEN="your_other_notion_token_here" \
  -e NOTION_DATABASE_ID="your_other_notion_database_id_here" \
  -e PROJECT_IDS="project_id1,project_id2,project_id3" \
  -e SYNC_INTERVAL="120" \
  your_docker_username/myapp:latest

```

Replace placeholders with your actual data:
- `your_ticktick_access_token_here` with your TickTick access token.
- `your_notion_token_here` with your Notion token.
- `your_notion_database_id_here` with your Notion database ID.
- `project_id1,project_id2,project_id3` with your TickTick project IDs.
- `60` with your desired sync interval in seconds.
- `your_image_name` with your preferred Docker image name.


This will start the process of syncing tasks from TickTick to your Notion database based on the configured environment variables.

### Monitoring

- Check the `sync_log.log` file in your project directory for runtime logs.
- Any errors or operational messages will be logged there to help you diagnose issues or confirm operations.


## Troubleshooting

- **Authentication Issues:** Ensure your access tokens and client credentials are correct.
- **Database Sharing:** Make sure the Notion database is shared with the integration correctly.
- **Docker Issues:** Check Docker logs and ensure the `.env` file is loaded properly.
- **Database parameters** The db needs to have a field called "Description" and a field called "Date" this is for the usage in Notion Calendar

