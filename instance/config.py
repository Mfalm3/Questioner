"""Configutation for the API"""
import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    """Base Config Class"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENV = 'development'


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """Configurations for Testing"""
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")


class ProductionConfig(Config):
    """Configurations for Production"""
    ENV = 'production'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

key = Config.SECRET_KEY
