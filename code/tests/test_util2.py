# Level 0: Impor dan definisi kelas
from django.test import TestCase
from lms_core.utils import validate_password

class PasswordValidationTest(TestCase):
    # Level 1: Di dalam kelas (indentasi 4 spasi)
    # Docstring untuk kelas
    """
    Test suite for the validate_password utility function.
    """

    def test_valid_passwords(self):
        # Level 2: Di dalam metode/fungsi (indentasi 8 spasi)
        """Test passwords that meet all criteria."""
        self.assertTrue(validate_password("PassValid1!"))
        self.assertTrue(validate_password("StrongPassword1@"))
        self.assertTrue(validate_password("Another$Valid2"))

    def test_invalid_password_too_short(self):
        # Level 2
        """Test password that is shorter than the minimum length."""
        self.assertFalse(validate_password("Short1!"), "Password should be at least 8 characters.")

    def test_invalid_password_no_uppercase(self):
        # Level 2
        """Test password without any uppercase letters."""
        self.assertFalse(validate_password("invalidpassword1!"), "Password should contain an uppercase letter.")

    def test_invalid_password_no_lowercase(self):
        # Level 2
        """Test password without any lowercase letters."""
        self.assertFalse(validate_password("INVALIDPASSWORD1!"), "Password should contain a lowercase letter.")

    def test_invalid_password_no_digit(self):
        # Level 2
        """Test password without any numerical digits."""
        self.assertFalse(validate_password("NoDigitPassword!"), "Password should contain a digit.")

    def test_invalid_password_no_special_char(self):
        # Level 2
        """Test password without any special characters."""
        self.assertFalse(validate_password("NoSpecialChar1"), "Password should contain a special character.")