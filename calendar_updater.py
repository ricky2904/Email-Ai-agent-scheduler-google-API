from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, time, timedelta
import pytz

def parse_date(date_str):
    if not date_str:
        raise ValueError("Date is missing.")
    date_str = date_str.lower().replace("st", "").replace("nd", "").replace("rd", "").replace("th", "").title()
    for fmt in ("%Y-%m-%d", "%A, %B %d", "%B %d", "%A %B %d", "%B %d, %Y", "%A %d %B"):
        try:
            parsed = datetime.strptime(date_str.strip(), fmt)
            # Fill in year if missing
            if parsed.year == 1900:
                parsed = parsed.replace(year=datetime.now().year)
            return parsed
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")

def parse_time(time_str):
    if not time_str:
        raise ValueError("Time is missing.")
    time_str = time_str.strip().lower().replace(" ", "")
    for fmt in ("%I:%M%p", "%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Time format not recognized: {time_str}")

def create_event(data):
    try:
        # Validate title
        if not data.get('title'):
            data['title'] = "Untitled Event"

        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar'])
        service = build('calendar', 'v3', credentials=creds)

        # Parse date and time
        date_obj = parse_date(data['date'])
        start_time = parse_time(data['start_time'])
        end_time = parse_time(data['end_time']) if data.get('end_time') else (datetime.combine(datetime.today(), start_time) + timedelta(minutes=30)).time()

        start_dt = datetime.combine(date_obj.date(), start_time)
        end_dt = datetime.combine(date_obj.date(), end_time)

        timezone = 'America/New_York'
        tz = pytz.timezone(timezone)
        start_dt = tz.localize(start_dt).isoformat()
        end_dt = tz.localize(end_dt).isoformat()

        # Validate attendees
        raw_emails = data.get('participants', [])
        attendees = []
        for email in raw_emails:
            if isinstance(email, str) and "@" in email:
                attendees.append({'email': email})

        event = {
            'summary': data['title'],
            'location': data.get('location', ''),
            'description': 'Created by AI Email Scheduler Agent',
            'start': {'dateTime': start_dt, 'timeZone': timezone},
            'end': {'dateTime': end_dt, 'timeZone': timezone},
            'attendees': attendees,
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"✅ Event created successfully!\n📅 Link: {created_event.get('htmlLink')}")

    except Exception as e:
        print(f"❌ Failed to create event: {e}")
