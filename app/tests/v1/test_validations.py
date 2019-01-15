# Test for validators
import unittest
from app import create_app
from app.api.v1.utils.validator import is_empty, no_numbers


class TestValidations(unittest.TestCase):
    """Test class for validations"""

    def setUp(self):
        """Set up config before test"""
        self.client = create_app('testing').test_client()

    def tearDown(self):
        """Tear down config after test"""
        self.client = None

    def test_is_not_empty(self):
        """Test for white space in string"""
        mystr = is_empty("  ")
        self.assertTrue(mystr)

    def test_no_digits(self):
        """Test for digits in string"""
        mystr0 = no_numbers("No digits")
        mystr1 = no_numbers("N0 d1g1ts")

        self.assertTrue(mystr0)
        self.assertFalse(mystr1)
