# Docker Deployment

This folder contains all Docker-related files for the Nordic Charge Pricing App.

## Files

- `Dockerfile` - Container definition for the Streamlit app
- `docker-compose.yml` - Service orchestration configuration
- `dockerignore` - Files to exclude from Docker build context

## Quick Deployment

From the project root, run:

```bash
./deploy.sh
```

## Manual Docker Commands

### Build and run with docker-compose:
```bash
# From project root
docker-compose -f docker/docker-compose.yml up --build -d
```

### Build manually:
```bash
# From project root
docker build -f docker/Dockerfile -t nordic-pricing .
docker run -d -p 8501:8501 --name nordic-pricing-app nordic-pricing
```

### View logs:
```bash
docker-compose -f docker/docker-compose.yml logs
```

### Stop containers:
```bash
docker-compose -f docker/docker-compose.yml down
```

## Development Workflow

1. Make changes to your app
2. Push to GitHub: `git push personal main`
3. SSH to server: `ssh root@YOUR_SERVER_IP`
4. Deploy: `cd Streamlit-Pricing && ./deploy.sh`
