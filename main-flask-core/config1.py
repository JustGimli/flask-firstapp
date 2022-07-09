


class Config(object):
    SECRET_KEY = 'key'
    DEBUG = False
    TESTING = False
    DATABASE = '/main-flask-core/user.db'
    USERNAME = 'admin'
    PASSWORD = 'default'


class testingConfig(Config):
    DEBUG = True
    TESTING = False