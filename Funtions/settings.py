import json

class Settings:
    def __init__(self, filepath):
        #Initialize the Settings object by loading settings from a JSON file.
        self.filepath = filepath
        self._settings = self.load_settings()

    def load_settings(self):
        #Load settings from the JSON file.
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Settings file {self.filepath} not found. Loading default settings.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.filepath}. Loading default settings.")
            return {}

    def get(self, key, default=None):
        #Get a setting value. Return 'default' if the key is not found.
        return self._settings.get(key, default)

    def set(self, key, value):
        #Set a setting value and update the JSON file.
        self._settings[key] = value
        self.save_settings()

    def save_settings(self):
        #Save the current settings to the JSON file.
        with open(self.filepath, 'w') as file:
            json.dump(self._settings, file, indent=4)
