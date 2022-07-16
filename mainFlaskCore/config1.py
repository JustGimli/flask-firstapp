#conf
class Config(object):
    SECRET_KEY = 'key'
    DEBUG = False
    TESTING = False
    DATABASE = 'mainFlaskCore/user.db'

class testingConfig(Config):
    DEBUG = True
    TESTING = True


