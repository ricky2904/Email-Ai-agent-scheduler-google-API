# 🤖 AI Email Scheduler

An intelligent email processing system that automatically extracts scheduling information from emails and creates calendar events using AI.

## ✨ Features

- **Smart Email Processing**: Uses AI to extract meeting details from email content
- **Google Calendar Integration**: Automatically creates calendar events
- **Modern Web Interface**: Beautiful React frontend with Material-UI
- **Docker Support**: Fully containerized application
- **Real-time Processing**: Process emails individually or in batch
- **Health Monitoring**: Built-in health checks and status monitoring

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Flask Backend  │    │  Google APIs    │
│   (Port 3000)   │◄──►│   (Port 5000)   │◄──►│  Gmail/Calendar │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   Ollama LLM    │
         │              │  (Port 11434)   │
         │              │   (Dockerized)  │
         │              └─────────────────┘
         │
         ▼
┌─────────────────┐
│   Nginx Proxy   │
│   (Optional)    │
└─────────────────┘
```

## 🚀 Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Google Cloud Project with Gmail and Calendar APIs enabled
- Google OAuth2 credentials file

### 1. Setup Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API and Google Calendar API
4. Create OAuth2 credentials (Desktop application)
5. Download the credentials file as `credentials.json`
6. Place it in the project root directory

### 2. Run with Docker Compose

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-agent-email-scheduler

# Place your credentials.json in the root directory

# Start the application (includes Ollama LLM service)
docker-compose up --build
```

**Note**: The first time you run this, Ollama will download the required model (phi3 by default). This may take a few minutes depending on your internet connection.

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Ollama API**: http://localhost:11434
- **API Health Check**: http://localhost:5000/api/health

## 🛠️ Development Setup

### Backend Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python app.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📋 API Endpoints

### Health Check
- `GET /api/health` - Check service status

### Email Operations
- `GET /api/emails` - Fetch unread emails
- `POST /api/process-email` - Process specific email text
- `POST /api/check-emails` - Process all unread emails

### Example API Usage

```bash
# Check health
curl http://localhost:5000/api/health

# Fetch emails
curl http://localhost:5000/api/emails

# Process custom email
curl -X POST http://localhost:5000/api/process-email \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Meeting tomorrow at 2 PM in conference room A"}'
```

## 🔧 Configuration

### Environment Variables

#### Backend
- `FLASK_ENV`: Flask environment (development/production)
- `PYTHONUNBUFFERED`: Python output buffering
- `OLLAMA_URL`: Ollama API endpoint (default: `http://ollama:11434` in Docker, `http://localhost:11434` locally)

#### Frontend
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:5000/api)

### Google API Setup

1. **Enable APIs**:
   - Gmail API
   - Google Calendar API

2. **OAuth2 Setup**:
   - Create OAuth2 credentials
   - Set authorized redirect URIs
   - Download credentials.json

3. **Scopes Required**:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/calendar.events`

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild specific service
docker-compose up --build backend

# Pull/download Ollama models (run inside Ollama container)
docker exec -it ai-email-scheduler-ollama ollama pull phi3
```

## 📁 Project Structure

```
ai-agent-email-scheduler/
├── app.py                 # Flask backend API
├── email_reader.py        # Gmail integration
├── llm_agent.py          # AI email processing
├── calendar_updater.py   # Google Calendar integration
├── memory.py             # Email memory storage
├── requirements.txt      # Python dependencies
├── Dockerfile.backend    # Backend Docker image
├── docker-compose.yml    # Multi-service orchestration
├── frontend/             # React frontend
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── App.css      # Styling
│   ├── Dockerfile       # Frontend Docker image
│   └── nginx.conf       # Nginx configuration
└── README.md
```

## 🔍 Troubleshooting

### Common Issues

1. **Gmail Authentication Error**
   - Ensure `credentials.json` is in the root directory
   - Check OAuth2 scopes are correct
   - Delete `token.json` and re-authenticate

2. **Backend Connection Error**
   - Check if backend is running on port 5000
   - Verify Docker containers are healthy
   - Check logs: `docker-compose logs backend`

3. **Frontend API Error**
   - Verify `REACT_APP_API_URL` environment variable
   - Check CORS settings in backend
   - Ensure backend is accessible from frontend

### Health Checks

```bash
# Check backend health
curl http://localhost:5000/api/health

# Check frontend
curl http://localhost:3000

# Check Docker services
docker-compose ps
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google APIs for Gmail and Calendar integration
- Ollama for local LLM capabilities
- Material-UI for React components
- Flask for Python backend framework



