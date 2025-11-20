# AI Email Scheduler - Startup Script
# This script starts both backend and frontend services

Write-Host "🚀 Starting AI Email Scheduler Application..." -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is running
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
try {
    $ollamaCheck = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Ollama is running on localhost:11434" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Ollama is not running. Please start Ollama first:" -ForegroundColor Yellow
    Write-Host "   ollama serve" -ForegroundColor White
    Write-Host ""
    $startOllama = Read-Host "Do you want to continue anyway? (y/n)"
    if ($startOllama -ne "y") {
        exit
    }
}

Write-Host ""
Write-Host "📦 Starting services..." -ForegroundColor Yellow
Write-Host ""

# Start Backend in new window
Write-Host "🔧 Starting Backend (Flask) on port 5000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; Write-Host '🚀 Backend Starting...' -ForegroundColor Green; python app.py" -WindowStyle Normal

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "🎨 Starting Frontend (React) on port 3000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; Write-Host '🎨 Frontend Starting...' -ForegroundColor Green; npm start" -WindowStyle Normal

Write-Host ""
Write-Host "✅ Services starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access the application:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Please wait for both services to fully start..." -ForegroundColor Yellow
Write-Host "   Backend will show 'Running on http://0.0.0.0:5000'" -ForegroundColor Gray
Write-Host "   Frontend will show 'webpack compiled successfully'" -ForegroundColor Gray
Write-Host ""

# Check after some time
Start-Sleep -Seconds 5

Write-Host "🔍 Checking service status..." -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -TimeoutSec 2
    Write-Host "✅ Backend is healthy!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend is still starting or encountered an error." -ForegroundColor Yellow
    Write-Host "   Check the backend window for details." -ForegroundColor Gray
}

Write-Host ""
Write-Host "📝 To stop the services, close the PowerShell windows or press Ctrl+C in each." -ForegroundColor Gray
Write-Host ""





