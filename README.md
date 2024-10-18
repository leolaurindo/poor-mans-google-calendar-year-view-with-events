# Poor man's google calendar year view with events highlighted.

This app creates an annual view of your google calendar events.

For some obscure reason, this feature is missing in the main app, even though people have been requesting it for at least ~7 years.

You need to create an OAuth 2.0 credentials.json file from the Google Calendar API using your Google Cloud account.

On running the script, it fetches your calendar (`.ics`) data into memory and plots it in a year view. After that, it saves in a `calendars` subdirectory. This part was made so that you may not need to run this script everytime you want to open you annual calendar view, assuming there were no changes.

A `cleanup.py` was added to make it easy to delete all but the last calendar figure created.