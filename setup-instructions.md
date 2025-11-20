# 🚀 AI Email Scheduler - Complete Setup Guide

## ✅ What We've Built

I've successfully created a complete AI Email Scheduler application with:

### Backend (Python Flask)
- **API Endpoints**: Health check, email fetching, email processing
- **Google Integration**: Gmail and Google Calendar APIs
- **AI Processing**: LLM integration for extracting scheduling information
- **Docker Support**: Complete containerization

### Frontend (React)
- **Modern UI**: Material-UI components with beautiful design
- **Real-time Processing**: Process emails individually or in batch
- **Status Monitoring**: Health checks and error handling
- **Responsive Design**: Works on desktop and mobile

### Docker Configuration
- **Multi-service Setup**: Backend, Frontend, and optional Ollama LLM
- **Health Checks**: Automatic service monitoring
- **Volume Mounting**: Persistent credentials and data
- **Network Configuration**: Service communication

## 📋 Setup Instructions

### Step 1: Install Dependencies

#### Python Dependencies
```bash
# Install Python packages
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install google-auth==2.23.4
pip install google-auth-oauthlib==1.1.0
pip install google-auth-httplib2==0.1.1
pip install google-api-python-client==2.108.0
pip install requests==2.31.0
pip install chromadb==0.4.15
pip install pytz==2023.3
pip install python-dotenv==1.0.0
```

#### Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 2: Google API Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**: Create a new project or select existing
3. **Enable APIs**:
   - Gmail API
   - Google Calendar API
4. **Create OAuth2 Credentials**:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: "Desktop application"
   - Download the JSON file
   - Rename it to `credentials.json` and place in project root

### Step 3: Test the Setup

```bash
# Run the test script
python test-setup.py
```

### Step 4: Run the Application

#### Option A: Development Mode (Recommended for testing)

**Terminal 1 - Backend:**
```bash
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

#### Option B: Docker Mode (Production)

**Install Docker Desktop first, then:**
```bash
# Build and start all services
docker compose up --build

# Or with Ollama LLM locally
docker compose --profile llm up --build
```

### Step 5: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:
```env
FLASK_ENV=development
REACT_APP_API_URL=http://localhost:5000/api
```

### Google API Scopes

The application uses these scopes:
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/calendar.events`

## 📁 Project Structure

```
ai-agent-email-scheduler/
├── app.py                 # Flask backend API
├── email_reader.py        # Gmail integration
├── llm_agent.py          # AI email processing
├── calendar_updater.py   # Google Calendar integration
├── memory.py             # Email memory storage
├── requirements.txt      # Python dependencies
├── test-setup.py         # Setup verification script
├── Dockerfile.backend    # Backend Docker image
├── docker-compose.yml    # Multi-service orchestration
├── frontend/             # React frontend
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── App.css      # Styling
│   ├── Dockerfile       # Frontend Docker image
│   ├── nginx.conf       # Nginx configuration
│   └── package.json     # Frontend dependencies
└── README.md
```

## 🚀 Features

### Backend API Endpoints

- `GET /api/health` - Check service status
- `GET /api/emails` - Fetch unread emails
- `POST /api/process-email` - Process specific email text
- `POST /api/check-emails` - Process all unread emails

### Frontend Features

- **Email List**: View all unread emails
- **Individual Processing**: Process specific emails
- **Batch Processing**: Process all emails at once
- **Custom Email**: Paste email text for processing
- **Status Monitoring**: Real-time status updates
- **Error Handling**: User-friendly error messages

## 🔍 Troubleshooting

### Common Issues

1. **"No module named 'flask'"**
   - Solution: Install Python dependencies with pip

2. **"Gmail service not connected"**
   - Solution: Check credentials.json and OAuth setup

3. **"Backend API not available"**
   - Solution: Ensure backend is running on port 5000

4. **Docker issues**
   - Solution: Install Docker Desktop and restart

### Health Checks

```bash
# Check backend
curl http://localhost:5000/api/health

# Check frontend
curl http://localhost:3000

# Check Docker services
docker compose ps
```

## 🎯 Next Steps

1. **Install Dependencies**: Follow Step 1 above
2. **Setup Google APIs**: Follow Step 2 above
3. **Test Setup**: Run `python test-setup.py`
4. **Start Application**: Choose development or Docker mode
5. **Access Frontend**: Open http://localhost:3000

## 📞 Support

If you encounter any issues:
1. Check the test script output
2. Verify all dependencies are installed
3. Ensure Google credentials are properly configured
4. Check the console logs for error messages

The application is now ready to use! 🎉



