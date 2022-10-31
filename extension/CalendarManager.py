from datetime import datetime
import subprocess
import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from extension.defines import GOOGLE_CALENDAR_SCOPES, GOOGLE_TOKEN, GOOGLE_CREDENTIALS

log = logging.getLogger(__name__)


class CalendarManager():
    """This class manages the process (cal command management and Google Calendar API)"""

    def __init__(self):
        log.info('Initializing Calendar')
        self.google = None

    def force_initialize_google(self):
        """Deletes all buffered stuff and forces to initialize Google"""

        log.info('Forcing Google to reintialize')
        self.google = None
        if os.path.exists(GOOGLE_TOKEN):
            os.remove(GOOGLE_TOKEN)

        self.initialize_google_if_not()

    def initialize_google_if_not(self):
        """This will initialize Google for this plugin.
        Needs OAuth Credentials.json file"""
        
        if self.google:
            log.debug("GoogleCalendar already initialized")
            return

        try:
            log.debug('Initializing GoogleCalendar service')
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists(GOOGLE_TOKEN):
                creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN, GOOGLE_CALENDAR_SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, GOOGLE_CALENDAR_SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(GOOGLE_TOKEN, 'w') as token:
                    token.write(creds.to_json())

            self.google = build('calendar', 'v3', credentials=creds)
          
        except HttpError as error:
            log.error('An error occurred: %s' % error)
        except FileNotFoundError as error:
            log.error('%s' % error)

    def cal_cmd_output(self, query: str) -> str:
        process = subprocess.Popen('cal ' + query,
            shell = True,
            stdout = subprocess.PIPE)
        exitcode = process.wait()
        if exitcode == 0:
            return process.stdout.read().decode() if process.stdout else "ERROR"
        else:
            log.error("cal cmd returned with exit-code <> 0, calling it withou arguments")
            return self.cal_cmd_output("")

    def get_google_events(self, max_ev: int) -> list:
        log.info('Looking for google calendar events')
        now = datetime.utcnow().isoformat()
        events = list()
        
        if self.google:
            log.info('Currently connected with google API')

            try:
                # Call the Calendar API
                events_result = self.google.events().list(
                    calendarId = 'primary',
                    timeMin = now + "Z",
                    maxResults = min(max_ev, 10),
                    singleEvents = True,
                    orderBy = 'startTime').execute()

                log.debug('asked for events. received: %d' % len(events_result))
                events = events_result.get('items', [])

            except HttpError as error:
                log.error('An error occurred: %s' % error)

        return events

