# 🚀 How to Run the Application

## Quick Start (Docker - Recommended)

### Step 1: Start All Services
```powershell
docker compose up --build
```

This will start:
- ✅ Ollama LLM service (port 11434)
- ✅ Backend API (port 5000)
- ✅ Frontend UI (port 3000)

**Note**: First startup may take 2-3 minutes as Docker downloads images and builds containers.

### Step 2: Download the Model (First Time Only)

Once the containers are running, open a **new terminal** and run:

```powershell
docker exec -it ai-email-scheduler-ollama ollama pull phi3
```

This downloads the AI model (~2GB). It may take 5-10 minutes depending on your internet speed.

### Step 3: Verify Everything is Running

Check if all containers are up:
```powershell
docker ps
```

You should see 3 containers:
- `ai-email-scheduler-ollama`
- `ai-email-scheduler-backend`
- `ai-email-scheduler-frontend`

### Step 4: Access the Application

- **🌐 Frontend UI**: http://localhost:3000
- **🔧 Backend API**: http://localhost:5000
- **🤖 Ollama API**: http://localhost:11434
- **❤️ Health Check**: http://localhost:5000/api/health

## Troubleshooting

### If Backend Won't Start

**Check logs:**
```powershell
docker compose logs backend
```

**Common issues:**
1. **Missing credentials.json** - Make sure `credentials.json` is in the project root
2. **Ollama not ready** - Wait a bit longer, Ollama needs time to start
3. **Port conflicts** - Make sure ports 5000, 3000, and 11434 are not in use

### If Ollama Healthcheck Fails

If you see healthcheck errors, you can temporarily remove it:

1. Edit `docker-compose.yml`
2. Comment out the `healthcheck` section in the `ollama` service
3. Change `backend` `depends_on` from:
   ```yaml
   depends_on:
     ollama:
       condition: service_healthy
   ```
   to:
   ```yaml
   depends_on:
     ollama:
   ```

### Check Service Status

```powershell
# View all logs
docker compose logs

# View specific service logs
docker compose logs ollama
docker compose logs backend
docker compose logs frontend

# Check container status
docker compose ps
```

### Stop the Application

```powershell
# Stop all services
docker compose down

# Stop and remove volumes (cleans up Ollama data)
docker compose down -v
```

## Alternative: Local Development (Without Docker)

If you prefer to run locally:

### 1. Start Ollama Locally
```powershell
# Make sure Ollama is installed and running
ollama serve

# In another terminal, pull the model
ollama pull phi3
```

### 2. Start Backend
```powershell
python app.py
```

### 3. Start Frontend
```powershell
cd frontend
npm start
```

## Next Steps

1. Open http://localhost:3000 in your browser
2. The first time, you'll need to authenticate with Google
3. Grant permissions for Gmail and Calendar access
4. Start fetching and processing emails!




