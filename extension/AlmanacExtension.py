from typing import List
import logging
from ulauncher.api.client.EventListener import EventListener

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from extension.CalendarManager import CalendarManager

from extension.CalendarManager import CalendarManager
from extension.defines import GOOGLE_ICON, PREF_GOOGLE_CAL, GOOGLE_DISABLED, GOOGLE_ENABLED, PREF_GOOGLE_MAX_EV, SELF_ICON



log = logging.getLogger(__name__)

class AlmanacExtension(Extension):

    def __init__(self):
        super(AlmanacExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())
        self.calendar = CalendarManager()

    def cal_cmd_to_extensionresult(self, str_cal:str):
        """Converts cal cmd std output to an ExtensionResultItem"""
        l_cal = str_cal.split("\n", 1)
        return ExtensionResultItem(
            icon = SELF_ICON,
            name=l_cal[0],
            description=" " + l_cal[1].replace(" ", "  "),
            on_enter=CopyToClipboardAction(str_cal))


    def google_ev_to_extensionresult(self, ev):
        """Converts cal cmd std output to an ExtensionResultItem"""
        return ExtensionResultItem(
            icon = GOOGLE_ICON,
            name = ev['summary'],
            description = ev['start'].get('dateTime', ev['start'].get('date')),
            on_enter = HideWindowAction())


    def GetExtensionResult(self, query: str, max_ev: int) -> List[ExtensionResultItem]:
        calendar_elements: List[ExtensionResultItem] = list()

        with_args = len(query.strip())
        if not with_args:
            query = '--three'

        # Generate cal command output
        str_cal = self.calendar.cal_cmd_output(query)
        calendar_elements.append(self.cal_cmd_to_extensionresult(str_cal)) 

        # Check if Google Calendar integration
        if PREF_GOOGLE_CAL in self.preferences and self.preferences[PREF_GOOGLE_CAL] == GOOGLE_ENABLED:
            # Initialize Google Calendar stuff
            self.calendar.initialize_google_if_not()

            # Check for Google Calendar incoming events 
            events = self.calendar.get_google_events(max_ev)
            for ev in events:
                calendar_elements.append(self.google_ev_to_extensionresult(ev))

        return calendar_elements

class PreferencesUpdateEventListener(EventListener):
    """This class manages preferences event listener"""
    def on_event(self, event, extension: AlmanacExtension):
        log.debug("Changed value %s=%s", event.id, event.new_value)
        if event.id == PREF_GOOGLE_CAL and event.new_value == GOOGLE_DISABLED:
            extension.calendar.force_initialize_google()
        return None

class KeywordQueryEventListener(EventListener):
    """This class manages this extension query event listener"""
    def on_event(self, event, extension: AlmanacExtension): 
        # Prepare needed arguments
        max_ev = extension.preferences[PREF_GOOGLE_MAX_EV] if PREF_GOOGLE_MAX_EV in extension.preferences else 5
        query = event.get_argument() or str()

        # Ask extension for result items
        extension_result = extension.GetExtensionResult(query, int(max_ev))
        return RenderResultListAction(extension_result)
