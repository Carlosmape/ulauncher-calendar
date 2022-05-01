from typing import Any
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

import subprocess


class Calendar():
    @staticmethod
    def get(query: str) -> str:
        process = subprocess.Popen('cal ' + query,
            shell=True,
            stdout=subprocess.PIPE)
        exitcode = process.wait()
        if exitcode == 0:
            if process.stdout and process.stdout.readable():
                return process.stdout.read().decode() 
        return "Error executing cal command..."


class AlmanacExtension(Extension):

    def __init__(self):
        super(AlmanacExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or str()
        if not len(query.strip()):
            query = '--three'
        str_cal = Calendar.get(query)
        l_cal = str_cal.split("\n", 1)

        results = RenderResultListAction([
            ExtensionResultItem(icon='images/icon.png',
                name=l_cal[0],
                description=" " + l_cal[1].replace(" ", "  "),
                on_enter=CopyToClipboardAction(str_cal))
            ])
        return results


if __name__ == '__main__':
    AlmanacExtension().run()
