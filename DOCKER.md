# MT5 Portfolio Analyzer - Docker Setup Guide

This guide explains how to run the MT5 Portfolio Analyzer using Docker and Docker Compose.

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)
- OpenAI API key (for GPT analysis features)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kobzarbro-droid/mt5-analyzer.git
cd mt5-analyzer
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Start the Application

```bash
docker-compose up -d
```

This will:
- Build the backend Docker image
- Start the backend API server on port 5000
- Start the frontend with nginx on port 8080
- Set up networking between containers

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:8080
```

The backend API is available at:

```
http://localhost:5000
```

## Service Details

### Backend Service

- **Container Name**: `mt5-analyzer-backend`
- **Port**: 5000
- **Technology**: Python 3.11, Flask
- **Health Check**: Available at `http://localhost:5000/health`

### Frontend Service

- **Container Name**: `mt5-analyzer-frontend`
- **Port**: 8080
- **Technology**: Nginx, HTML/CSS/JavaScript
- **API Proxy**: Requests to `/api/*` are proxied to backend

## Common Commands

### Start Services

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Restart Services

```bash
docker-compose restart
```

### Rebuild and Start

```bash
docker-compose up -d --build
```

### Check Service Status

```bash
docker-compose ps
```

## Development Mode

For development with live code reloading:

### Backend Development

```bash
# Stop the Docker backend
docker-compose stop backend

# Run backend locally
cd backend
python api.py
```

The frontend in Docker will automatically proxy to your local backend.

### Frontend Development

Just edit the files in `frontend/`. Nginx will serve the updated files immediately (you may need to refresh your browser).

## Troubleshooting

### Backend Container Won't Start

1. Check logs:
   ```bash
   docker-compose logs backend
   ```

2. Verify OpenAI API key is set:
   ```bash
   docker-compose exec backend env | grep OPENAI
   ```

3. Rebuild the image:
   ```bash
   docker-compose build --no-cache backend
   docker-compose up -d
   ```

### Frontend Can't Connect to Backend

1. Check if backend is healthy:
   ```bash
   curl http://localhost:5000/health
   ```

2. Check nginx configuration:
   ```bash
   docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
   ```

3. Check browser console for CORS errors

### Port Already in Use

If ports 5000 or 8080 are already in use, modify `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "5001:5000"  # Change to different port
  
  frontend:
    ports:
      - "8081:80"    # Change to different port
```

### Permission Issues

If you encounter permission issues with volumes:

```bash
sudo chown -R $USER:$USER .
```

## Data Persistence

- **Presets**: Stored in Docker volume `presets_data`
- **Logs**: Visible via `docker-compose logs`

To backup presets:

```bash
docker cp mt5-analyzer-backend:/app/presets ./presets_backup
```

To restore presets:

```bash
docker cp ./presets_backup mt5-analyzer-backend:/app/presets
```

## Production Deployment

### Security Considerations

1. **Use HTTPS**: Set up SSL/TLS certificates with Let's Encrypt
2. **Secure API Key**: Use Docker secrets or a secrets manager
3. **Update nginx.conf**: Remove CORS wildcard (`*`) and specify allowed origins
4. **Add Authentication**: Implement user authentication for production use
5. **Rate Limiting**: Configure nginx rate limiting

### Example nginx SSL Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... rest of configuration
}
```

### Docker Compose Production

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PORT=5000
      - DEBUG=false
    
  frontend:
    image: nginx:alpine
    restart: always
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
```

## Monitoring

### Health Checks

Both services have health checks configured:

```bash
# Check backend health
curl http://localhost:5000/health

# Check frontend health via Docker
docker-compose ps
```

### Resource Usage

```bash
# Check container resource usage
docker stats mt5-analyzer-backend mt5-analyzer-frontend
```

## Scaling

To run multiple backend instances behind a load balancer:

```yaml
services:
  backend:
    deploy:
      replicas: 3
    # ... rest of configuration
```

## Updating

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Update Dependencies

Edit `requirements.txt`, then:

```bash
docker-compose build --no-cache backend
docker-compose up -d
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/kobzarbro-droid/mt5-analyzer/issues
- Documentation: See README.md

## License

MIT License - See LICENSE file for details
