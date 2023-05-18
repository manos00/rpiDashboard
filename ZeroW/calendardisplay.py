#!/bin/env python3

import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getEvents():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        os.stat('token.json')
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except OSError:
        creds = False
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run 
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow()
        events_result = service.events().list(calendarId='primary', timeMin=f'{now.isoformat()}+02:00', # 'Z' indicates UTC time
                                              maxResults=3, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return
        return events

    except HttpError as error:
        print('An error occurred: %s' % error)


def prettyPrint(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    if 'T' in start:
        eventTime = start.split('T')
        eventTime = eventTime[1].split('+')[0]
    else:
        eventTime = start.split('-')
        eventTime = f'{eventTime[2]}-{eventTime[1]}-{eventTime[0][-2:]}'
    print(eventTime + ' | ' + event['summary'])


def main():
    events = getEvents()
    if not events:
        print('No events scheduled for today.')
    else:
        for event in events:
            prettyPrint(event)

if __name__ == '__main__':
    main()
