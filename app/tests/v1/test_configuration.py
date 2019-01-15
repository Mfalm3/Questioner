# Test for Configurations
import unittest

from app import create_app
from instance.config import (Config, TestingConfig,
DevelopmentConfig, ProductionConfig)

app = create_app('testing')


class TestConfigs(unittest.TestCase):
    """Test class for configurations"""

    def test_config(self):
        """Test for base configuration."""
        app.config.from_object(Config)
        self.assertEqual(app.config['DEBUG'], False)


class TestDevelopmentConfigs(unittest.TestCase):
    """Test class for development configurations"""

    def test_dev_configs(self):
        """Test for development configuration."""
        app.config.from_object(DevelopmentConfig)
        self.assertEqual(app.config['DEBUG'], True)


class TestTestingConfigs(unittest.TestCase):
    """Test class for testing configurations"""

    def test_test_configs(self):
        """Test for test configuration."""
        app.config.from_object(TestingConfig)
        self.assertEqual(app.config['DEBUG'], True)


class TestProductionConfig(unittest.TestCase):
    """Test class for production configurations"""

    def test_production_configs(self):
        """Test for production configuration."""
        app.config.from_object(ProductionConfig)
        self.assertEqual(app.config['DEBUG'], False)
        self.assertEqual(app.config['ENV'], "production")
