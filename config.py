import json

class Config:
    FILE_PATH = 'config.json'
    
    USERNAME = 'ASVZ Username'
    PASSWORD = 'ASVZ Password'

    @classmethod
    def load_credentials(cls):
        """Load credentials from a JSON file."""
        try:
            with open(cls.FILE_PATH, 'r') as file:
                data = json.load(file)
                cls.USERNAME = data.get('USERNAME', cls.USERNAME)
                cls.PASSWORD = data.get('PASSWORD', cls.PASSWORD)
        except FileNotFoundError:
            # If the file doesn't exist, just use the default values
            cls.save_credentials()

    @classmethod
    def save_credentials(cls):
        """Save credentials to a JSON file."""
        with open(cls.FILE_PATH, 'w') as file:
            json.dump({
                'USERNAME': cls.USERNAME,
                'PASSWORD': cls.PASSWORD
            }, file)

    @classmethod
    def update_credentials(cls, username, password):
        """Update the credentials and save them."""
        cls.USERNAME = username
        cls.PASSWORD = password
        cls.save_credentials()