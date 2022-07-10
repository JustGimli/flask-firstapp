#conf
class Config(object):
    SECRET_KEY = 'key',
    DEBUG = False,
    TESTING = False,
    DATABASE = 'mainFlaskCore/user.db'
    USERNAME = 'admin',
    PASSWORD = 'default'

class testingConfig(Config):
    DEBUG = True
    TESTING = False


