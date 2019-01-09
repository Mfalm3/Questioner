"""Base Test Class"""

import unittest

from app import create_app

class BaseTest(unittest.TestCase):
    """Define base test configurations across all tests"""
    def setUp(self):
        self.client = create_app('testing').test_client()
        self.mime_type = 'application/json'

    def tearDown(self):
        self.client = None
