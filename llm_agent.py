import re
import json
import requests

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
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    print("🔍 Result:", result)
    
    # Safe check for missing date
    if not data.get('date'):
        print("⚠️ No date found in the parsed data.")
        return

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

        return json_str.strip()
    else:
        raise ValueError("No valid JSON found in LLM output")
