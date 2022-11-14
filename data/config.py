import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        self.token = self.config['settings']['bot_token']
        self.owner_id = self.config['settings']['owner_id']
        self.owner_username = self.config['settings']['owner_username']
        self.qiwi_number = self.config['settings']['qiwi_number']
        self.qiwi_api = self.config['settings']['qiwi_api']
        self.qiwi_card = self.config['settings']['qiwi_card']

config = Config()