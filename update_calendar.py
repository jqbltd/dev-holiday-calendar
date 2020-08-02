import json
import os.path
import pickle

from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
START_YEAR_TEMPLATE = "{}-01-01T00:00:00Z"


def get_config():
    with open('config.json', 'rb') as f:
        return json.load(f)


def get_credentials():
    credentials = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            credentials = pickle.load(f)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_console()
        
        with open('token.pickle', 'wb') as f:
            pickle.dump(credentials, f)
    
    return credentials


def get_calendar_events(calendar_events, calendar_id):
    last_year = datetime.now().year - 1
    start_time = START_YEAR_TEMPLATE.format(last_year)
    
    events = []
    page_token = None
    while True:
        page_events = calendar_events.list(
            calendarId=calendar_id, pageToken=page_token, timeMin=start_time
        ).execute()
        events += page_events['items']
        page_token = page_events.get('nextPageToken')
        if not page_token:
            break
    return events


def clear_calendar_events(calendar_events, config):
    events = get_calendar_events(calendar_events, config['calendar_ids']['dev'])
    for event in events:
        calendar_events.delete(
            calendarId=config['calendar_ids']['dev'], eventId=event['id']
        ).execute()


def is_event_of_a_dev_user(event_summary, config):
    try:
        name = event_summary.split(' - ')[1]
    except IndexError:
        return False
    
    return name in config['names']


def copy_calendar_events(calendar_events, config):
    events = get_calendar_events(calendar_events, config['calendar_ids']['holiday'])
    for event in events:
        try:
            should_copy_event = is_event_of_a_dev_user(event['summary'], config)
        except KeyError:
            continue
        
        if should_copy_event:
            event_body = {
                'summary': event['summary'],
                'start': {
                    'date': event['start']['date'],
                },
                'end': {
                    'date': event['end']['date'],
                },
            }
            calendar_events.insert(
                calendarId=config['calendar_ids']['dev'], body=event_body
            ).execute()


def main():
    credentials = get_credentials()
    service = build('calendar', 'v3', credentials=credentials)
    
    config = get_config()
    
    clear_calendar_events(service.events(), config)
    copy_calendar_events(service.events(), config)


if __name__ == '__main__':
    main()
