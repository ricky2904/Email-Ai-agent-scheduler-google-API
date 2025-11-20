# 🐳 Docker Setup Guide

This guide explains how to run the application with Docker.

## 📋 Overview

The application supports **two deployment modes**:

1. **Full Local** (Development) - Everything runs on your machine
2. **Full Docker** (Recommended) - Everything containerized (including Ollama)

## 🚀 Recommended: Full Docker Setup

This is the **recommended** setup for deployment:

### Prerequisites

1. **Docker Desktop installed** (Windows/Mac) or Docker Engine (Linux)
2. **Google Cloud credentials** (`credentials.json` file)

### Step 1: Run Docker Containers

```bash
# Build and start all services (backend, frontend, and Ollama)
docker compose up --build
```

The backend container will automatically connect to the Ollama service running in Docker using `http://ollama:11434`.

**Note**: The first time you run this, Ollama will download the required model (phi3 by default). This may take a few minutes depending on your internet connection.

### How It Works

```
┌─────────────────────────────────────┐
│  Docker Network                      │
│                                     │
│  ┌─────────────┐                   │
│  │  Ollama     │  ollama:11434      │
│  │  (Docker)   │                   │
│  └──────┬──────┘                   │
│         │                           │
│         │ Docker Network            │
│         ↓                           │
│  ┌─────────────┐                   │
│  │  Backend     │  Container        │
│  │  (Docker)   │  Port 5000        │
│  └──────┬──────┘                   │
│         │                           │
│         ↓                           │
│  ┌─────────────┐                   │
│  │  Frontend   │  Container        │
│  │  (Docker)   │  Port 3000        │
│  └─────────────┘                   │
└─────────────────────────────────────┘
```

## 🔧 Configuration

### Environment Variables

The `llm_agent.py` uses the `OLLAMA_URL` environment variable:

- **Local Development**: Uses `http://localhost:11434` (default)
- **Docker**: Uses `http://ollama:11434` (set in docker-compose.yml)

You can override it:
```bash
# In docker-compose.yml or as environment variable
OLLAMA_URL=http://your-ollama-host:11434
```

### Downloading Models

When Ollama runs in Docker, you need to download the model inside the container:

```bash
# Pull the default model (phi3)
docker exec -it ai-email-scheduler-ollama ollama pull phi3

# Or pull a different model
docker exec -it ai-email-scheduler-ollama ollama pull llama3
```

The model will be persisted in the `ollama_data` Docker volume.

### Using Different Models

To use a different model, set the `OLLAMA_MODEL` environment variable in `docker-compose.yml`:

```yaml
backend:
  environment:
    - OLLAMA_MODEL=llama3  # Change from default 'phi3'
```

## 🧪 Testing the Connection

### Test 1: Ollama Service
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test Ollama API
curl http://localhost:11434/api/generate \
  -d '{"model": "phi3", "prompt": "Hello", "stream": false}'
```

### Test 2: From Backend Container
```bash
# Enter backend container
docker exec -it ai-email-scheduler-backend bash

# Test connection to Ollama service
curl http://ollama:11434/api/tags
```

### Test 3: Backend Health
```bash
curl http://localhost:5000/api/health
```

## 🐛 Troubleshooting

### Issue: Ollama Healthcheck Fails (Container marked as unhealthy)

**Error**: If you see errors like "healthcheck failed" or "curl: command not found" or "wget: command not found"

**Solution 1**: Remove the healthcheck (simplest fix)
```yaml
# In docker-compose.yml, remove the healthcheck section from ollama service:
ollama:
  # ... other config ...
  # Remove or comment out the healthcheck section
  # healthcheck:
  #   test: ...
  
# And change backend depends_on to:
backend:
  depends_on:
    ollama:  # Remove condition: service_healthy
```

**Solution 2**: Check if Ollama container is running
```bash
docker ps | grep ollama
```

**Solution 3**: Check Ollama logs
```bash
docker logs ai-email-scheduler-ollama
```

**Solution 4**: Make sure the model is downloaded
```bash
# Check available models
docker exec -it ai-email-scheduler-ollama ollama list

# If no models, download one
docker exec -it ai-email-scheduler-ollama ollama pull phi3
```

### Issue: Backend can't reach Ollama

**Solution 1**: Verify both services are on the same network
```bash
docker network inspect ai-agent-email-scheduler_ai-scheduler-network
```

**Solution 2**: Test connection from backend container
```bash
docker exec -it ai-email-scheduler-backend curl http://ollama:11434/api/tags
```

**Solution 3**: Check environment variable
```bash
docker exec ai-email-scheduler-backend env | grep OLLAMA_URL
# Should show: OLLAMA_URL=http://ollama:11434
```

### Issue: Ollama response too slow

**Solution**: Increase timeout in `llm_agent.py`:
```python
response = requests.post(
    OLLAMA_API_URL,
    json={...},
    timeout=120  # Increase from 60 to 120 seconds
)
```

## 📝 Environment Variables Summary

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://ollama:11434` (Docker), `http://localhost:11434` (Local) | Ollama API endpoint |
| `OLLAMA_MODEL` | `phi3` | Ollama model to use |
| `FLASK_ENV` | `production` | Flask environment |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |

## 🎯 Quick Start Commands

```bash
# 1. Start all Docker services
docker compose up --build

# 2. Download the model (first time only)
docker exec -it ai-email-scheduler-ollama ollama pull phi3

# 3. Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Ollama: http://localhost:11434
```

## ✅ Verification Checklist

- [ ] Docker Desktop is running (Windows/Mac) or Docker Engine (Linux)
- [ ] All containers are running: `docker ps`
- [ ] Ollama model is downloaded (`phi3` or your chosen model)
- [ ] Ollama is accessible at `http://localhost:11434`
- [ ] Backend can reach Ollama service
- [ ] Frontend can reach backend
- [ ] Test email processing works end-to-end

---

For more details, see the main [README.md](README.md) file.

