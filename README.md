# Coding Hours Tracker

This project tracks and logs coding hours using Google Calendar and an SQLite database. It allows you to add events to your Google Calendar, calculates the duration of coding sessions, and stores this information in a database. You can also retrieve and analyze the total and average hours worked over a specified period.

## Features

- **Database Setup**: Initializes an SQLite database to store coding hours.
- **Event Management**: Adds events to Google Calendar specifying coding duration and description.
- **Hours Tracking**: Retrieves coding events from Google Calendar, calculates total hours, and logs them in the database.
- **Hours Retrieval**: Fetches and displays total and average coding hours over a specified number of days.

## Requirements

- Python 3.x
- Google API Client Library (`google-api-python-client`)
- Google Auth Library (`google-auth`, `google-auth-oauthlib`)
- SQLite3
- `dateutil` for date parsing

## Setup

1. **Install Dependencies**

   Install the required Python libraries using pip:

   ```bash
   pip install google-api-python-client google-auth google-auth-oauthlib python-dateutil
   ```

2. **Google Calendar API Setup**

   - Enable the Google Calendar API at [Google Developers Console](https://console.developers.google.com/).
   - Download `credentials.json` and place it in the project directory.
   - Run the script to generate `token.json` by following the OAuth flow.

3. **Initialize the Database**

   Run the `initialize_db.py` script to create the SQLite database and table:

   ```bash
   python initialize_db.py
   ```

4. **Usage**

   - **Add Event**: To add a coding event to your calendar, use:

     ```bash
     python manage_hours.py add <duration> <description>
     ```

     Replace `<duration>` with the number of hours and `<description>` with the event description.

   - **Commit Hours**: To commit today's coding hours to the database, use:

     ```bash
     python manage_hours.py commit
     ```

   - **Retrieve Hours**: To get coding hours over a specified number of days, use:

     ```bash
     python manage_hours.py getHours <number_of_days>
     ```

     Replace `<number_of_days>` with the number of days to analyze.

## Files

- **`initialize_db.py`**: Script to set up the SQLite database and create the `hours` table.
- **`manage_hours.py`**: Script to interact with Google Calendar, commit hours to the database, and retrieve coding hours.

## Notes

- Make sure to replace `YOUR_CALENDAR_ID` and `YOUR_TIMEZONE` in `manage_hours.py` with your actual Google Calendar ID and timezone.
- Ensure `credentials.json` and `token.json` are in the same directory as the scripts for proper authentication.
