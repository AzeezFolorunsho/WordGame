import json
import os

class Settings:
    """
    A class to manage application settings loaded from a JSON file.

    Attributes:
        filepath (str): Path to the JSON settings file.
        _settings (dict): Dictionary to store settings loaded from the file.
    """

    def __init__(self, filepath='wordle_plus_game/local_files/Settings.json'):
        self.filepath = filepath
        self._settings = self._load_settings()

    def _load_settings(self):
        """
        Loads settings from a JSON file.

        Returns:
            dict: Loaded settings or an empty dictionary if loading fails.
        """
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Settings file {self.filepath} not found. Loading default settings.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.filepath}. Loading default settings.")
            return {}

    def get(self, section, key, default=None):
        """
        Retrieves a setting value from a specific section.

        Args:
            section (str): The section of the settings.
            key (str): The setting key to retrieve.
            default: Default value to return if key is not found.

        Returns:
            The value of the setting or default if key is not found.
        """
        return self._settings.get(section, {}).get(key, default)

    def set(self, section, key, value):
        """
        Sets a setting value in a specific section and updates the JSON file.

        Args:
            section (str): The section of the settings.
            key (str): The setting key to set.
            value: The value to set for the key.
        """
        if section not in self._settings:
            self._settings[section] = {}
        self._settings[section][key] = value
        self._save_settings()

    def _save_settings(self):
        """
        Saves the current settings to the JSON file.
        """
        with open(self.filepath, 'w') as file:
            json.dump(self._settings, file, indent=4)
