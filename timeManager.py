from __future__ import print_function
import datetime
import os
import sys
import sqlite3

from dateutil import parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
YOUR_CALENDAR_ID = ''
YOUR_TIMEZONE = ''

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def commit_hours(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)
        today = datetime.date.today()
        time_start = f"{today}T00:00:00Z"
        time_end = f"{today}T23:59:59Z"
        
        events_result = service.events().list(
            calendarId=YOUR_CALENDAR_ID,
            timeMin=time_start,
            timeMax=time_end,
            singleEvents=True,
            orderBy='startTime',
            timeZone=YOUR_TIMEZONE
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No coding events found.')
            return

        total_duration = datetime.timedelta()
        print("CODING HOURS:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_time = parser.isoparse(start)
            end_time = parser.isoparse(end)
            duration = end_time - start_time

            total_duration += duration
            print(f"{event['summary']}, duration: {duration}")

        formatted_total_duration = total_duration.total_seconds() / 3600
        with sqlite3.connect('hours.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO hours VALUES (?, ?, ?);", (today, 'CODING', formatted_total_duration))
            conn.commit()

        print(f"Total coding time: {total_duration} hours")
        print("Coding hours added to database successfully")

    except HttpError as error:
        print(f'An error occurred: {error}')

def add_event(creds, duration, description):
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(hours=int(duration))
    event = {
        'summary': description,
        'start': {'dateTime': start.isoformat() + 'Z', 'timeZone': YOUR_TIMEZONE},
        'end': {'dateTime': end.isoformat() + 'Z', 'timeZone': YOUR_TIMEZONE},
    }

    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId=YOUR_CALENDAR_ID, body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def get_hours(number_of_days):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=int(number_of_days))

    with sqlite3.connect('hours.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT DATE, HOURS FROM hours WHERE DATE BETWEEN ? AND ?", (start_date, today))
        hours = cur.fetchall()

    total_hours = sum(hour[1] for hour in hours)
    average_hours = total_hours / float(number_of_days) if number_of_days > 0 else 0

    for date, hours in hours:
        print(f"{date}: {hours}")
    print(f"Total hours: {total_hours}")
    print(f"Average hours: {average_hours:.2f}")

def main():
    creds = get_credentials()

    if len(sys.argv) < 2:
        print("Usage: python manage_hours.py <command> [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) != 4:
            print("Usage: python manage_hours.py add <duration> <description>")
            sys.exit(1)
        duration, description = sys.argv[2], sys.argv[3]
        add_event(creds, duration, description)
    elif command == 'commit':
        commit_hours(creds)
    elif command == 'getHours':
        if len(sys.argv) != 3:
            print("Usage: python manage_hours.py getHours <number_of_days>")
            sys.exit(1)
        number_of_days = sys.argv[2]
        get_hours(number_of_days)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
