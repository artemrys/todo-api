# Add other configs, for example, TestingConfig, ProductionConfig etc


class BaseConfig(object):
    DEBUG = True
    TESTING = False


class DevelopmentConfig(BaseConfig):
    MONGOALCHEMY_DATABASE = "todo"
    MONGOALCHEMY_SERVER = "localhost"
    MONGOALCHEMY_PORT = 27017
    MONGOALCHEMY_USER = None
    MONGOALCHEMY_PASSWORD = None
