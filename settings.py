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
        if not value:
            if key not in self.settings_dict:
                return
            del self.settings_dict[key]
        else:
            self.settings_dict[key] = value
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings_dict, f)


app_settings = SettingsManager()
