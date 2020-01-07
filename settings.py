import json

SETTINGS_FILE = 'settings.json'


class SettingsManager:
    def __init__(self):
        with open(SETTINGS_FILE, 'r') as f:
            self.settings_dict = json.load(f)

    def exists(self, key):
        return key in self.settings_dict

    def get(self, key):
        return self.settings_dict[key]

    def set(self, key, value):
        self.settings_dict[key] = value
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(f, self.settings_dict)


app_settings = SettingsManager()
