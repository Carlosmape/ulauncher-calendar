from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension): 
        # Initialize Google Calendar stuff
        if "google_cal" in extension.preferences and extension.preferences["google_cal"] != "":
            extension.calendar.initialize_google(extension.preferences["google_cal"])

        # Prepare needed arguments
        max_ev = extension.preferences["max_events"] if "max_events" in extension.preferences else 5
        query = event.get_argument() or str()

        # Ask extension for result items
        extension_result = extension.GetExtensionResult(query, int(max_ev))
        return RenderResultListAction(extension_result)
