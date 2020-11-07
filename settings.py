import json
import logging

class Settings():
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.token = None
        self.run_bot = True
    
    def print_settings(self):
        token = 'Not set' if self.token is None else 'set'
        print(f'settings_file: {self.settings_file}')
        print(f'Token: {token}')

    def parse_settings(self):
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
            self.token = data.get("token")
            
            logging.info('Settings were parsed successfully')
            return True
        except Exception as e:
            logging.critical(f'Failed to parse settings: {e}')
            return False