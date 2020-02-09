from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label


class LogItem(Label):
    pass


class LogScreen(Screen):
    def __init__(self, **kwargs):
        super(LogScreen, self).__init__(**kwargs)
        self.log_container = None
        self.logslist_widget = self.ids.logslist_widget

    def add_log_item(self, text):
        log_item_widget = LogItem(text=text)
        self.logslist_widget.add_widget(log_item_widget)
