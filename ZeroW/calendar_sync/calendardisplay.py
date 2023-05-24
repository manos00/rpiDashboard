#!/bin/env python3

import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

fileDir = Path(__file__).parent.resolve()

def getEvents():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        os.stat(f'{fileDir}/token.json')
        creds = Credentials.from_authorized_user_file(f'{fileDir}/token.json', SCOPES)
    except OSError:
        creds = False
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{fileDir}/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run 
        with open(f'{fileDir}/token.json', 'w') as token:
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


def formatEvents(events):
    eventstr = '| '
    for index, event in enumerate(events):
        start = event['start'].get('dateTime', event['start'].get('date'))
        eventDate = start.split('-')  
        eventDate = f'{eventDate[2][:2]}.{eventDate[1]}.{eventDate[0][-2:]}'  
        if 'T' in start:
            eventTime = ' | ' + start.split('T')[1].split('+')[0][:-3]
        else:
            eventTime = ''
        eventstr += f"""{eventDate}{eventTime}
    {event['summary']}"""
        if index < 2:
            eventstr += '\n'
    return eventstr

def main():
    events = getEvents()
    if not events:
        print('No events scheduled for today.')
    else:
        print(formatEvents(events))

if __name__ == '__main__':
    main()
