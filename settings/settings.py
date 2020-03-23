"""
Application settings
===================
Contains single shared instance of SettingsManager class which reads and stores application's settings.
"""

import os
import json

SETTINGS_FILE = 'settings.json'


class SettingsManager:
    """
    Reads and stores application's settings.
    """

    def __init__(self):
        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({}, f)

        with open(SETTINGS_FILE, 'r') as f:
            self.settings_dict = json.load(f)

    def exists(self, key):
        """ Test whether there are settings corresponding to the given `key`. """

        return key in self.settings_dict

    def get(self, key):
        """ Returns value corresponding to the given key and raises exception otherwise. """

        return self.settings_dict[key]

    def set(self, key, value):
        """ Stores provided value corresponding to the given key in `setting_dict` and `settings.json` file. """

        if not value:
            if key not in self.settings_dict:
                return
            del self.settings_dict[key]
        else:
            self.settings_dict[key] = value
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings_dict, f, indent=2)


app_settings = SettingsManager()
