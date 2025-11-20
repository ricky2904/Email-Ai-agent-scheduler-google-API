from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from email_reader import authenticate_gmail, get_unread_emails
from llm_agent import extract_schedule_from_email
from calendar_updater import create_event
from googleapiclient.discovery import build
import json
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables for Gmail service
gmail_service = None

# In-memory storage for emails with scheduling content
# Format: {email_id: {email_data with scheduling_info}}
scheduling_emails_cache = {}

def initialize_gmail():
    """Initialize Gmail service on startup"""
    global gmail_service
    try:
        creds = authenticate_gmail()
        gmail_service = build('gmail', 'v1', credentials=creds)
        return True
    except Exception as e:
        print(f"Failed to initialize Gmail: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "gmail_connected": gmail_service is not None
    })

@app.route('/api/debug-scheduling', methods=['GET'])
def debug_scheduling():
    """Debug endpoint to test scheduling detection"""
    global scheduling_emails_cache
    
    test_email_text = request.args.get('text', 'Meeting tomorrow at 3pm in room A')
    
    try:
        structured = extract_schedule_from_email(test_email_text)
        parsed_data = json.loads(structured)
        
        has_action = "action" in parsed_data
        has_date = bool(str(parsed_data.get("date", "")).strip()) if parsed_data.get("date") else False
        has_start_time = bool(str(parsed_data.get("start_time", "")).strip()) if parsed_data.get("start_time") else False
        
        return jsonify({
            "test_email": test_email_text,
            "structured_output": structured,
            "parsed_data": parsed_data,
            "has_action_key": has_action,
            "has_date": has_date,
            "has_start_time": has_start_time,
            "would_be_detected": not has_action and has_date and has_start_time,
            "cache_count": len(scheduling_emails_cache)
        })
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Get unread emails"""
    if not gmail_service:
        return jsonify({"error": "Gmail service not initialized"}), 500
    
    try:
        max_results = request.args.get('max_results', 5, type=int)
        emails = get_unread_emails(gmail_service, max_results)
        return jsonify({"emails": emails})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fetch-emails', methods=['GET'])
def fetch_emails():
    """Fetch up to 10 unread emails and analyze them for scheduling content"""
    global scheduling_emails_cache
    
    if not gmail_service:
        return jsonify({"error": "Gmail service not initialized"}), 500
    
    try:
        # Always check exactly 10 emails
        max_results = 10
        emails = get_unread_emails(gmail_service, max_results, process_emails=False)
        
        # Clear previous cache
        scheduling_emails_cache = {}
        
        # Analyze each email for scheduling content
        scheduling_count = 0
        for email in emails:
            try:
                print(f"\n📧 Analyzing email: {email.get('subject', 'No subject')[:50]}")
                
                # Analyze email content for scheduling information
                structured = extract_schedule_from_email(email.get('snippet', ''))
                parsed_data = json.loads(structured)
                
                print(f"📊 Parsed data keys: {list(parsed_data.keys())}")
                print(f"📊 Has 'action' key: {'action' in parsed_data}")
                
                # Check if it contains scheduling information
                # Method 1: Check if it explicitly says "No scheduling info"
                has_action_key = "action" in parsed_data
                
                # Method 2: Check if it has valid scheduling fields (date and start_time)
                # Handle None, null strings, and empty strings
                date_value = parsed_data.get("date")
                start_time_value = parsed_data.get("start_time")
                
                has_date = (
                    date_value is not None 
                    and str(date_value).strip().lower() not in ["null", "none", ""]
                    and len(str(date_value).strip()) > 0
                )
                
                has_start_time = (
                    start_time_value is not None 
                    and str(start_time_value).strip().lower() not in ["null", "none", ""]
                    and len(str(start_time_value).strip()) > 0
                )
                
                has_valid_scheduling = has_date and has_start_time
                
                print(f"📊 Has date: {has_date} ({parsed_data.get('date')})")
                print(f"📊 Has start_time: {has_start_time} ({parsed_data.get('start_time')})")
                print(f"📊 Has valid scheduling: {has_valid_scheduling}")
                
                if not has_action_key and has_valid_scheduling:
                    # This email has scheduling information - store it
                    scheduling_count += 1
                    print(f"✅ Email {email['id']} has scheduling content!")
                    scheduling_emails_cache[email['id']] = {
                        "email_id": email['id'],
                        "subject": email['subject'],
                        "from": email['from'],
                        "snippet": email['snippet'],
                        "scheduling_data": parsed_data,
                        "has_scheduling": True
                    }
                else:
                    print(f"❌ Email {email['id']} does NOT have scheduling content")
                    if has_action_key:
                        print(f"   Reason: Has 'action' key: {parsed_data.get('action')}")
                    if not has_valid_scheduling:
                        print(f"   Reason: Missing date or start_time")
                    
            except json.JSONDecodeError as e:
                # If JSON parsing fails, skip this email
                print(f"⚠️ JSON Error analyzing email {email.get('id', 'unknown')}: {e}")
                print(f"   Raw structured output: {structured[:200]}")
                continue
            except Exception as e:
                # If parsing fails, skip this email
                print(f"⚠️ Error analyzing email {email.get('id', 'unknown')}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        return jsonify({
            "success": True,
            "count": len(emails),
            "emails": emails,
            "scheduling_found": scheduling_count,
            "message": f"Fetched {len(emails)} emails. Found {scheduling_count} emails with scheduling content."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scheduling-emails', methods=['GET'])
def get_scheduling_emails():
    """Get cached emails that contain scheduling information"""
    global scheduling_emails_cache
    
    if not gmail_service:
        return jsonify({"error": "Gmail service not initialized"}), 500
    
    try:
        # Return cached scheduling emails (stored when fetch-emails was called)
        valid_scheduling_emails = list(scheduling_emails_cache.values())
        
        if len(valid_scheduling_emails) == 0:
            return jsonify({
                "success": True,
                "scheduling_count": 0,
                "scheduling_emails": [],
                "message": "No emails with scheduling content found. Please click 'Fetch Emails' first to analyze emails."
            })
        
        return jsonify({
            "success": True,
            "scheduling_count": len(valid_scheduling_emails),
            "scheduling_emails": valid_scheduling_emails,
            "message": f"Found {len(valid_scheduling_emails)} emails with scheduling information"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/schedule-event', methods=['POST'])
def schedule_event():
    """Schedule an event from scheduling data"""
    try:
        data = request.get_json()
        scheduling_data = data.get('scheduling_data')
        
        if not scheduling_data:
            return jsonify({"error": "Scheduling data is required"}), 400
        
        # Validate required fields
        required_fields = ['title', 'date', 'start_time', 'end_time']
        missing_fields = [field for field in required_fields if not scheduling_data.get(field)]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "scheduling_data": scheduling_data
            }), 400
        
        # Create calendar event
        create_event(scheduling_data)
        
        return jsonify({
            "success": True,
            "message": "Event created successfully",
            "event_data": scheduling_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-email', methods=['POST'])
def process_email():
    """Process a specific email for scheduling"""
    try:
        data = request.get_json()
        email_text = data.get('email_text')
        
        if not email_text:
            return jsonify({"error": "Email text is required"}), 400
        
        # Extract schedule information using LLM
        structured = extract_schedule_from_email(email_text)
        
        try:
            parsed_data = json.loads(structured)
            
            # Check if it's a scheduling email
            if "action" in parsed_data:
                return jsonify({
                    "success": False,
                    "message": "No scheduling information found in email",
                    "raw_output": structured
                })
            
            # Validate required fields
            required_fields = ['title', 'date', 'start_time', 'end_time']
            missing_fields = [field for field in required_fields if not parsed_data.get(field)]
            
            if missing_fields:
                return jsonify({
                    "success": False,
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                    "raw_output": structured
                })
            
            # Create calendar event
            create_event(parsed_data)
            
            return jsonify({
                "success": True,
                "message": "Event created successfully",
                "event_data": parsed_data
            })
            
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "message": "Failed to parse LLM output as JSON",
                "raw_output": structured,
                "error": str(e)
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-emails', methods=['POST'])
def check_emails():
    """Check for new emails and process them automatically"""
    if not gmail_service:
        return jsonify({"error": "Gmail service not initialized"}), 500
    
    try:
        max_results = request.args.get('max_results', 5, type=int)
        # Delegate scheduling to email_reader which already creates events
        emails = get_unread_emails(gmail_service, max_results, process_emails=True)

        return jsonify({
            "processed_count": len(emails),
            "emails": emails,
            "message": f"Checked {len(emails)} unread emails; scheduling attempted via email_reader."
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Email Scheduler Backend...")
    
    # Initialize Gmail service
    if initialize_gmail():
        print("✅ Gmail service initialized successfully")
    else:
        print("❌ Failed to initialize Gmail service")
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
