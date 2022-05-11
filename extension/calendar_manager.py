from datetime import datetime
import subprocess
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


log = logging.getLogger(__name__)

class Calendar():

    def __init__(self):
        log.info('Initializing Calendar')
        self.google = None

    def initialize_google(self, api_key: str):
        """This will initialize Google for this plugin.
        Needs developer api key"""
        
        if self.google is not None:
            log.debug('GoogleCalendar already connected')
            return

        log.debug('Initializing GoogleCalendar service')
        try:
            log.error('Using given api_key =', api_key)
            self.google = build('calendar', 'v3', developerKey = api_key)
          
        except HttpError as error:
            log.error('An error occurred: %s' % error)

    def get(self, query: str) -> str:
        process = subprocess.Popen('cal ' + query,
            shell = True,
            stdout = subprocess.PIPE)
        exitcode = process.wait()
        if exitcode == 0:
            return process.stdout.read().decode() if process.stdout else "ERROR"
        else:
            log.error("cal cmd returned with exit-code <> 0, calling it withou arguments")
            return self.get("")

    def get_google(self, max_ev: int) -> list:
        log.info('Looking for google calendar events')
        events = list()
        
        if self.google:
            log.info('Currently connected with google API')
            try:
                # Call the Calendar API
                now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
                events_result = self.google.events().list(calendarId = 'primary', timeMin = now,
                                              maxResults = min(max_ev, 10), singleEvents = True,
                                              orderBy = 'startTime').execute()
                log.debug('asked for events. received: %d' % len(events_result))
                events = events_result.get('items', [])
            except HttpError as error:
                log.error('An error occurred: %s' % error)
        else:
            log.warning('Currently NOT connected with google API')
        return events

