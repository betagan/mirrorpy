from calpy.caldav.Client import Client
from mirrorpy.plugin import Plugin


class CalDAVPlugin(Plugin):
    def __init__(self):
        pass

    def get(self):
        return "<div><i class='fa fa-calendar-o'></i> Calendar</div>"


