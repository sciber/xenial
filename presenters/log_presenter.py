"""
Log presenter
=============
Contains LogScreen class presenting data 'log_screen.kv' view.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label


class LogItem(Label):
    """ Represents logslist item UI objects with inherited argument `text`. """

    pass


class LogScreen(Screen):
    """
    Presents data to the Log screen 'log_screen.kv' view.
    """

    def __init__(self, **kwargs):
        super(LogScreen, self).__init__(**kwargs)
        self.log_container = None
        self.logslist_widget = self.ids.logslist_widget

    def add_log_item(self, text):
        """ Adds item with given text to the logslist. """

        log_item_widget = LogItem(text=text)
        self.logslist_widget.add_widget(log_item_widget)
