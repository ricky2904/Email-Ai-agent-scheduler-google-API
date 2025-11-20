# 🚀 How to Run the Application

## Quick Start (Automated)

### Option 1: PowerShell Script (Recommended)
```powershell
.\start-app.ps1
```
This will start both backend and frontend in separate windows.

### Option 2: Manual Start (Recommended for debugging)

#### Step 1: Start Backend
Open a **new terminal/PowerShell window** and run:
```powershell
python app.py
```
You should see:
```
🚀 Starting AI Email Scheduler Backend...
✅ Gmail service initialized successfully
 * Running on http://0.0.0.0:5000
```

#### Step 2: Start Frontend
Open **another terminal/PowerShell window** and run:
```powershell
cd frontend
npm start
```
You should see:
```
webpack compiled successfully
```

#### Step 3: Access Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## ✅ Prerequisites Check

Before starting, make sure:

1. **Ollama is running locally:**
   ```powershell
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # If not running, start it:
   ollama serve
   ```

2. **Python dependencies installed:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Frontend dependencies installed:**
   ```powershell
   cd frontend
   npm install
   ```

4. **Google credentials configured:**
   - `credentials.json` file in project root
   - Gmail and Calendar APIs enabled

## 🐳 Docker Option (Alternative)

If you prefer Docker:

1. **Make sure Docker Desktop is running**

2. **Start containers:**
   ```powershell
   docker compose up --build
   ```

3. **Download the model (first time only):**
   ```powershell
   docker exec -it ai-email-scheduler-ollama ollama pull phi3
   ```

4. **Access:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000
   - Ollama: http://localhost:11434

## 🔍 Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Verify Python dependencies: `pip install -r requirements.txt`
- Check Google credentials are in place

### Frontend won't start
- Check if port 3000 is available
- Verify Node dependencies: `cd frontend && npm install`
- Check if backend is running first

### Ollama connection error
- Make sure Ollama is running: `curl http://localhost:11434/api/tags`
- Check if llama3 model is installed: `ollama list`
- If not installed: `ollama pull llama3`

### Gmail authentication error
- Ensure `credentials.json` exists
- Delete `token.json` and re-authenticate
- Check OAuth scopes are correct

## 📊 Verify Everything Works

1. **Check Backend:**
   ```powershell
   curl http://localhost:5000/api/health
   ```
   Should return: `{"status":"healthy","gmail_connected":true}`

2. **Check Frontend:**
   Open http://localhost:3000 in browser

3. **Test Email Processing:**
   - Click "Fetch Emails" button
   - Click "Scheduled Meeting Emails" button
   - Verify emails are displayed

## 🎯 Expected Output

### Backend Terminal:
```
🚀 Starting AI Email Scheduler Backend...
✅ Gmail service initialized successfully
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Frontend Terminal:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```

---

**Need help?** Check the logs in the terminal windows for detailed error messages.

