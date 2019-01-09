"""Configutation for the API"""


class Config(object):
    """Base Config Class"""
    DEBUG = False
    SECRET_KEY = 'mysecretkey'
    ENV = 'development'


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production"""
    ENV = 'production'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

key = Config.SECRET_KEY