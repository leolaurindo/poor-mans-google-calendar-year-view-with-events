# Poor man's google calendar year view with events highlighted.

## Motivation
This app creates an annual view of your google calendar events.

For some obscure reason, this feature is missing in the main app, even though people have been requesting it for at least ~7 years.

![alt text](example.png)

## Running

You need to create an OAuth 2.0 credentials.json file from the Google Calendar API using your Google Cloud account.

Install the environment and run 

`python main.py`

The year of 2024 is set as default. But you can pass an argument like this:

`python main.py --y 2023`

On running the script, it fetches your calendar (`.ics`) data into memory and plots its year view. After that, it saves the created figure in a `calendars` subdirectory. This part was made so that you may not need to run this script everytime you want to open you annual calendar view, assuming there were no changes.

A `cleanup.py` was added to make it easy to delete all but the last calendar figure created.

# Limitations

As of now, this script only fetches your main calendar, as explicitly coded in `get_year_events` function, which uses the default `calendar_id='primary'`. This will be addressed in the future.

Additionally,

- The script only supports fetching events for a single year at a time.
- It is limited to read-only access (SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']), meaning it cannot create, update, or delete calendar events.
- Event visualizations are basic and might not be ideal for large-scale or highly complex schedules, as only days with events are highlighted in the generated calendar.
- Only a static image of the calendar is generated, with no interactive features for exploring or modifying events.