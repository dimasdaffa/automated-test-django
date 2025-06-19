from django.test import TestCase
from .utils import calculate_discount

class UtilsTest(TestCase):
    """
    Test suite for utility functions.
    
    This class contains tests for various utility functions, starting
    with calculate_discount.
    """

    def test_calculate_discount_valid(self):
        """
        Test the calculate_discount function with valid percentage values.
        """
        # Test case 1: 10% discount on 100 should result in 90.
        self.assertEqual(calculate_discount(100, 10), 90)
        
        # Test case 2: 50% discount on 200 should result in 100.
        self.assertEqual(calculate_discount(200, 50), 100)
        
        # Test case 3: 0% discount should result in no change.
        self.assertEqual(calculate_discount(150, 0), 150)
        
        # Test case 4: 100% discount should result in 0.
        self.assertEqual(calculate_discount(150, 100), 0)

    def test_calculate_discount_invalid_percentage(self):
        """
        Test that calculate_discount raises ValueError for invalid percentages.
        """
        # Test that a negative discount percentage raises an error.
        with self.assertRaises(ValueError, msg="Negative discount should not be allowed."):
            calculate_discount(100, -10)
            
        # Test that a discount percentage greater than 100 raises an error.
        with self.assertRaises(ValueError, msg="Discount greater than 100% should not be allowed."):
            calculate_discount(100, 110)