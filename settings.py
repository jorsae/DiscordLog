import json
import logging

class Settings():
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.token = None
        self.database_file = 'DiscordDatabase.db'
    
    def print_settings(self):
        token = 'Not set' if self.token is None else 'set'
        print(f'settings_file: {self.settings_file}')
        print(f'Token: {token}')
        print(f'database_file: {self.database_file}')

    def parse_settings(self):
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
            self.token = data.get("token")
            self.database = data.get("database")
            
            logging.info('Settings were parsed successfully')
            return True
        except Exception as e:
            logging.critical(f'Failed to parse settings: {e}')
            return False