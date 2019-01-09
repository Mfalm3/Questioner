"""Test for Configurations"""

import unittest

from app import create_app
from instance.config import Config, TestingConfig, DevelopmentConfig, ProductionConfig

app = create_app('testing')


class TestConfigs(unittest.TestCase):
    def test_config(self):
        app.config.from_object(Config)
        self.assertEqual(app.config['DEBUG'], False)


class TestDevelopmentConfigs(unittest.TestCase):
    def test_dev_configs(self):
        app.config.from_object(DevelopmentConfig)
        self.assertEqual(app.config['DEBUG'], True)


class TestTestingConfigs(unittest.TestCase):
    def test_test_configs(self):
        app.config.from_object(TestingConfig)
        self.assertEqual(app.config['DEBUG'], True)


class TestProductionConfig(unittest.TestCase):
    def test_production_configs(self):
        app.config.from_object(ProductionConfig)
        self.assertEqual(app.config['DEBUG'], False)
        self.assertEqual(app.config['ENV'], "production")
