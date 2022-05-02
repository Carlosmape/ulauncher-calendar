from datetime import datetime
import os
import subprocess
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


log = logging.getLogger(__name__)
TOKEN = 'token.json'
CRED = 'credentials.json'

class Calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']

    def __init__(self):
        log.info('Initializing Calendar')
        self.google = None
        self.creds = None

    def get(self, query: str) -> str:
        process = subprocess.Popen('cal ' + query,
            shell=True,
            stdout=subprocess.PIPE)
        exitcode = process.wait()
        if exitcode == 0:
            if process.stdout and process.stdout.readable():
                return process.stdout.read().decode() 
        else:
            log.error("cal cmd returned with exit-code <> 0")
        return "Error executing cal command..."

    def initialize_google(self):
        """This will initialize Google OAuth for this plugin.
        Asks for user if needed"""

        log.debug('Initializing GoogleCalendar service')

        log.debug('Looking for token.json credentials')
        if os.path.exists('token.json'):
            log.debug('Found!, loading credentials form it.')
            self.creds = Credentials.from_authorized_user_file('token.json', Calendar.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            log.debug('Not found... Not Valid credentials')
            if self.creds and self.creds.expired and self.creds.refresh_token:
                log.debug('Refreshing credentials.')
                self.creds.refresh(Request())
            else:
                log.debug("Asking for google credentials")
                flow = InstalledAppFlow.from_client_secrets_file(
                CRED, Calendar.SCOPES)
                self.creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(TOKEN, 'w') as token:
                    token.write(self.creds.to_json())

        # Ask google for incoming events
        try:
            self.google = build('calendar', 'v3', credentials=self.creds)
          
        except HttpError as error:
            log.error('An error occurred: %s' % error)

    def remove_google(self):
        if os.path.exists(TOKEN):
            os.remove(TOKEN)

    
    def get_google(self, max_ev: int) -> list:
        log.info('Looking for google calendar events')
        events = list()
        
        if self.google:
            log.info('Currently connected with google API')
            try:
                # Call the Calendar API
                now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
                events_result = self.google.events().list(calendarId='primary', timeMin=now,
                                              maxResults=min(max_ev,10), singleEvents=True,
                                              orderBy='startTime').execute()
                log.debug('asked for events. received: %d' % len(events_result))
                events = events_result.get('items', [])
            except HttpError as error:
                log.error('An error occurred: %s' % error)
        return events

