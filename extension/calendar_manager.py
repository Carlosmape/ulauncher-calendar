from datetime import datetime
import os
import subprocess


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']

    def __init__(self):
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
        return "Error executing cal command..."

    def initialize_google(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', Calendar.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', Calendar.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        # Ask google for incoming events
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
          
        except HttpError as error:
            print('An error occurred: %s' % error)

    
    def get_google(self) -> list:
        events = list()
        
        if self.google:
            try:
                # Call the Calendar API
                now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
                events_result = self.google.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
                events = events_result.get('items', [])
            except HttpError as error:
                events.append('An error occurred: %s' % error)
        return events

