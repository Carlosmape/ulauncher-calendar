from ulauncher.api.client.EventListener import EventListener


class PreferencesUpdateEventListener(EventListener):

    def on_event(self, event, extension):
        if event.id == "google_cal":
            if event.new_value == "yes" and event.old_value != event.new_value:
                extension.calendar.initialize_google()
            elif event.new_value == "no" and event.old_value != event.new_value:
                extension.calendar.remove_google()
        return None

