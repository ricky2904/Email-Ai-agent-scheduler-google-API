import re
import json
import requests
import os
from datetime import datetime, timedelta

# Get Ollama URL from environment variable (defaults to localhost for local development)
OLLAMA_BASE_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_API_URL = f"{OLLAMA_BASE_URL}/api/generate"

# Get model name from environment variable (defaults to smaller model for better memory usage)
# Options: "phi3", "gemma2:2b", "llama3.2", "llama3" (larger, needs more RAM)
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'phi3')

def extract_schedule_from_email(email_text):
    prompt = f"""
You are a helpful AI assistant that extracts meeting and scheduling information from email content.

Email:
\"\"\"{email_text}\"\"\"

If the email contains an event, extract:
- Title
- Date  // Use format like "October 25th 2025"
- Start Time
- End Time
- Location (if any)
- Participants (if mentioned)
Return all dates in ISO format like "2025-10-23".

Respond ONLY in this JSON format:
{{
  "title": "...",
  "date": "...",
  "start_time": "...",
  "end_time": "...",
  "location": "...",
  "participants": [...]
}}

If there's no event, respond:
{{ "action": "No scheduling info found." }}
"""

    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60  # Add timeout for better error handling
    )

    result = response.json()
    print("🔍 Result:", result)

    if "error" in result:
        raise ValueError(result["error"])

    raw_output = result["response"]
    print("🔍 Raw LLM Output:", raw_output)

    # Extract first JSON block only (removes explanations, comments, etc.)
    match = re.search(r'{[\s\S]*}', raw_output)
    if match:
        json_str = match.group()

        # Remove JS-style comments if any
        json_str = re.sub(r'//.*', '', json_str)

        # Normalize and enforce scheduling when date and time exist
        try:
            data = json.loads(json_str)

            # If model explicitly says no scheduling info, return as-is
            if isinstance(data, dict) and data.get("action"):
                return json.dumps(data)

            if not isinstance(data, dict):
                raise ValueError("Parsed JSON is not an object")

            # Map alternative keys
            if "time" in data and not data.get("start_time"):
                data["start_time"] = data.get("time")

            # Minimal requirement: date and start_time -> schedule
            has_date = bool(str(data.get("date", "")).strip())
            has_start = bool(str(data.get("start_time", "")).strip())

            if has_date and has_start:
                # Default title if missing
                if not str(data.get("title", "")).strip():
                    data["title"] = "Meeting"

                # Ensure location is a string
                if data.get("location") is None:
                    data["location"] = ""

                # Ensure participants is a list
                participants = data.get("participants")
                if participants is None:
                    data["participants"] = []
                elif not isinstance(participants, list):
                    data["participants"] = [str(participants)]

                # Auto-fill end_time (+30 minutes) if missing or empty
                end_time_raw = str(data.get("end_time", "")).strip()
                if not end_time_raw or end_time_raw.lower() in ["null", "none", ""]:
                    start_raw = str(data.get("start_time", "")).strip().lower().replace(" ", "")
                    end_time_val = None
                    # Try common formats: 3:00pm, 03:00PM, 15:00, 15:00:00
                    for fmt in ("%I:%M%p", "%I%p", "%H:%M", "%H:%M:%S"):
                        try:
                            t = datetime.strptime(start_raw, fmt)
                            dt = datetime(2000, 1, 1, t.hour, t.minute) + timedelta(minutes=30)
                            end_time_val = dt.strftime("%H:%M")
                            break
                        except Exception:
                            continue
                    # Fallback: keep same start time
                    data["end_time"] = end_time_val or start_raw

                print(f"✅ Valid scheduling data found: date={data.get('date')}, start_time={data.get('start_time')}")
                return json.dumps(data)
            else:
                # If minimal fields not found, mark as no scheduling
                print(f"⚠️ Missing required fields: date={bool(has_date)}, start_time={bool(has_start)}")
                # Return the "no scheduling" format
                return json.dumps({"action": "No scheduling info found."})
        except Exception:
            # If normalization fails, return cleaned string to avoid breaking flow
            return json_str.strip()
    else:
        raise ValueError("No valid JSON found in LLM output")
