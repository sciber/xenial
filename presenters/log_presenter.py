"""
Log presenter
=============
Contains LogScreen class presenting data 'logsmenu_screen.kv' view.
"""

import os
import re

import kivy

from kivy.config import Config
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class LogsMenuButton(Button):
    def __init__(self, log_filename, **kwargs):
        super(LogsMenuButton, self).__init__(**kwargs)
        self.log_filename = log_filename


class LogsMenuItem(Label):
    """ Represents logslist item UI objects with inherited argument `text`. """

    pass


class LogsMenuScreen(Screen):
    """
    Presents data to the Log screen 'logsmenu_screen.kv' view.
    """

    def __init__(self, **kwargs):
        super(LogsMenuScreen, self).__init__(**kwargs)
        self.logsmenu_items_container = self.ids.logsmenu_items_container
        logs_dir = os.path.join(kivy.kivy_home_dir, Config.get('kivy', 'log_dir'))
        for log_filename in sorted(os.listdir(logs_dir), reverse=True):
            logsmenu_button_widget = LogsMenuButton(log_filename)
            self.logsmenu_items_container.add_widget(logsmenu_button_widget)


class LogScreen(Screen):
    log_filename = StringProperty('')

    def on_enter(self, *largs):
        if self.log_filename:
            log_path = os.path.join(kivy.kivy_home_dir, Config.get('kivy', 'log_dir'), self.log_filename)
            colorized_log_text = ''
            with open(log_path, 'r') as f:
                for line in f:
                    colorized_log_text += self._colorize_log_line(line)
            self.log_text = colorized_log_text

    def _colorize_log_line(self, line):
        if re.match(r'^\[TRACE.*?\].*', line):
            color = '#00BB22'
        elif re.match(r'^\[DEBUG.*?\].*', line):
            color = '#0022BB'
        elif re.match(r'^\[INFO.*?\].*', line):
            color = '#00BBBB'
        elif re.match(r'^\[WARNING.*?\].*', line):
            color = '#DD8800'
        elif re.match(r'^\[ERROR.*?\].*', line):
            color = '#DD2200'
        elif re.match(r'^\[CRITICAL.*?\].*', line):
            color = '#DD0000'
        else:
            color = '#222222'
        return f'[color={color}]' + line + '[/color]'
