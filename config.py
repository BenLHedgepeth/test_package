class BaseConfig:
    DEBUG = False
    TESTING = False
    DATABASE = "main.db"

class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'Shhhhhh!'

    