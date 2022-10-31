from typing import List

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

from extension.KeywordQueryEventListener import KeywordQueryEventListener
from extension.calendar_manager import Calendar


class AlmanacExtension(Extension):

    def __init__(self):
        super(AlmanacExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.calendar = Calendar()

        # Initialize Google Calendar stuff
        if "google_cal" in self.preferences and self.preferences["google_cal"]:
            self.calendar.initialize_google()

    def GetExtensionResult(self, query: str) -> List[ExtensionResultItem]:
        calendar_elements: List[ExtensionResultItem] = list()

        # Generate cal command output
        if not len(query.strip()):
            query = '--three'

        str_cal = self.calendar.get(query)
        l_cal = str_cal.split("\n", 1)
        calendar_elements.append(ExtensionResultItem(icon='images/icon.png',
                name=l_cal[0],
                description=" " + l_cal[1].replace(" ", "  "),
                on_enter=CopyToClipboardAction(str_cal))) 

        # Check for Google Calendar incoming events
        events = self.calendar.get_google()
        for ev in events:
            calendar_elements.append(ExtensionResultItem(icon='images/icon.png',
                name=ev['summary'],
                description=ev['start'].get('dateTime', ev['start'].get('date')),
                on_enter=HideWindowAction()))

        return calendar_elements


