from django.test import TestCase
from lms_core.utils import calculator

class CalculatorFunctionTest(TestCase):
    """
    Test suite for the calculator utility function.
    
    This class contains a series of unit tests to verify the correct
    functionality of the `calculator` function, including basic arithmetic
    operations and handling of edge cases like division by zero and
    invalid operators.
    """

    def test_addition(self):
        """Test the addition functionality."""
        self.assertEqual(calculator(1, 2, '+'), 3)
        self.assertEqual(calculator(-1, -1, '+'), -2)
        self.assertEqual(calculator(0, 5, '+'), 5)

    def test_subtraction(self):
        """Test the subtraction functionality."""
        self.assertEqual(calculator(5, 3, '-'), 2)
        self.assertEqual(calculator(-1, -1, '-'), 0)
        self.assertEqual(calculator(0, 5, '-'), -5)

    def test_multiplication(self):
        """Test the multiplication functionality."""
        # Note: Assuming 'x' is the operator for multiplication.
        # It's often better to use '*' for consistency.
        self.assertEqual(calculator(3, 4, 'x'), 12)
        self.assertEqual(calculator(-1, 5, 'x'), -5)
        self.assertEqual(calculator(0, 5, 'x'), 0)

    def test_division(self):
        """Test the division functionality."""
        self.assertEqual(calculator(10, 2, '/'), 5)
        self.assertEqual(calculator(-10, 2, '/'), -5)
        self.assertEqual(calculator(0, 1, '/'), 0)

    def test_division_by_zero(self):
        """Test that division by zero raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            calculator(10, 0, '/')
        
        self.assertEqual(str(context.exception), "Cannot divide by zero")

    def test_invalid_operator(self):
        """Test that an invalid operator raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            calculator(10, 5, '%')
        
        self.assertEqual(str(context.exception), "Invalid operator")