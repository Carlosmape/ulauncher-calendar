from ulauncher.api.client.EventListener import EventListener



class PreferencesUpdateEventListener(EventListener):

    def on_event(self, event, extension):
        if event.id == "google_cal":
            if event.new_value and event.old_value != event.new_value:
                extension.calendar.initialize_google(event.new_value)
        return None

