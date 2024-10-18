import argparse
import calendar
import datetime
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials are available, user must log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_year_events(service, calendar_id='primary', year=2024):
    start_date = datetime.datetime(year, 1, 1, 0, 0, 0).isoformat() + 'Z'
    end_date = datetime.datetime(year, 12, 31, 23, 59, 59).isoformat() + 'Z'
    
    events_result = service.events().list(calendarId=calendar_id, timeMin=start_date, 
                                          timeMax=end_date, singleEvents=True,
                                          orderBy='startTime').execute()
    
    return events_result.get('items', [])

def create_yearly_calendar(events, year=2024):
    event_dates = set()
    for event in events:
        start_date_str = event['start'].get('dateTime', event['start'].get('date'))
        start_date = datetime.datetime.fromisoformat(start_date_str)
        event_dates.add(start_date.date())

    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(16, 9))
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S']  # Weekday abbreviations

    for month in range(1, 13):
        ax = axes[(month-1)//4][(month-1)%4]
        ax.set_axis_off()

        cal = calendar.monthcalendar(year, month)

        table_data = [weekdays] 
        cell_colors = [['lightgrey']*7]

        for week in cal:
            week_data = []
            week_colors = []
            for day in week:
                if day == 0:
                    week_data.append('')
                    week_colors.append('white')
                else:
                    day_date = datetime.date(year, month, day)
                    week_data.append(str(day))
                    if day_date in event_dates:
                        week_colors.append('lightblue')
                    else:
                        week_colors.append('white')
            table_data.append(week_data)
            cell_colors.append(week_colors)

        table = ax.table(cellText=table_data, cellColours=cell_colors, cellLoc='center', loc='upper center')

        ax.set_title(calendar.month_name[month], fontsize=14)

        table.scale(1.3, 1.7) 
        for key, cell in table.get_celld().items():
            cell.set_fontsize(10)

    plt.suptitle(f'Event Calendar for {year}', fontsize=16)
    os.makedirs('calendars', exist_ok=True)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    file_name = f'{year}_yearly_calendar_as_of_{today}.png'
    save_path = os.path.join('calendars', file_name)
    plt.savefig(save_path)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Google Calendar Event Fetcher')
    parser.add_argument('--y', type=int, default=2024, help='Year to fetch events for (default is 2024)')
    args = parser.parse_args()

    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    
    events = get_year_events(service, year=args.y)
    if not events:
        print('No events found.')
    else:
        create_yearly_calendar(events, year=args.y)

if __name__ == '__main__':
    main()