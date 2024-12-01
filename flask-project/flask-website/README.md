# Deploying your Flask app in Docker.

#### Clone this Repository & Enter the directory
```
rm -rf flask-dashboard-1
git clone https://github.com/SumonPaul18/flask-dashboard-1.git
cd flask-dashboard-1
```

### After entering the directory you changed `.env` file as your environment variable.

1. **Use a `.env` File**:
   - Store sensitive information like API keys, database credentials, and secret keys in a `.env` file.
   - Example `.env` file:
     ```
     SECRET_KEY=your-secret-key
     GOOGLE_OAUTH_CLIENT_ID=your-client-id
     GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
     ```

### Docker Deployment

1. **Build and Run Your Docker Container**:
   - Build your Docker image:
     ```bash
     docker compose build
     ```
   - Run your Docker container:
     ```bash
     docker compose up -d
     ```
