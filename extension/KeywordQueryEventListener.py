from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from extension.AlmanacExtension import AlmanacExtension


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension: AlmanacExtension):
        return RenderResultListAction(extension.GetExtensionResult(event.get_argument()))
