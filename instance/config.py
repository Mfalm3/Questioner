"""Configutation for the API"""


class Config(object):
    """Base Config Class"""
    DEBUG = False
    SECRET_KEY = 'mysecretkey'
    ENV = 'development'


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    DATABASE_URL = "dbname='qmeetups_db' host='localhost' port='5432' " \
                   "user='waithaka' password='postgres'"



class TestingConfig(Config):
    """Configurations for Testing"""
    DEBUG = True
    DATABASE_TEST_URL = "dbname='qmeetups_tests_db' host='localhost' "\
                        "port='5432' user='waithaka' password='postgres'"


class ProductionConfig(Config):
    """Configurations for Production"""
    ENV = 'production'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

key = Config.SECRET_KEY
