from django.test import TestCase
from django.contrib.auth.models import User
from lms_core.models import Course, CourseMember, ROLE_OPTIONS # Asumsi ROLE_OPTIONS diimpor dari model

# --- Test Case untuk Model Course ---

class CourseModelTest(TestCase):
    """
    Test suite for the Course model.
    """

    def setUp(self):
        """
        Set up non-modified objects used by all test methods.
        """
        self.teacher = User.objects.create_user(username='teacher1', password='password123')
        self.student = User.objects.create_user(username='student1', password='password123')
        
        self.course = Course.objects.create(
            name="Django for Beginners",
            description="Learn Django from scratch.",
            price=100,
            teacher=self.teacher
        )

    def test_course_creation(self):
        """
        Test that a Course instance is created correctly with all attributes.
        """
        self.assertEqual(self.course.name, "Django for Beginners")
        self.assertEqual(self.course.description, "Learn Django from scratch.")
        self.assertEqual(self.course.price, 100)
        self.assertEqual(self.course.teacher, self.teacher)

    def test_course_str_representation(self):
        """
        Test the __str__ method of the Course model.
        """
        self.assertEqual(str(self.course), "Django for Beginners")

    def test_is_member_method(self):
        """
        Test the is_member() custom method on the Course model.
        """
        # 1. Before adding the student, is_member should be False.
        self.assertFalse(self.course.is_member(self.student))
        
        # 2. Add the student as a course member.
        CourseMember.objects.create(course=self.course, user=self.student, roles='std')
        
        # 3. After adding, is_member should be True.
        self.assertTrue(self.course.is_member(self.student))

# --- Test Case untuk Model CourseMember ---

class CourseMemberModelTest(TestCase):
    """
    Test suite for the CourseMember model.
    """

    def setUp(self):
        """
        Set up non-modified objects used by all test methods.
        """
        teacher = User.objects.create_user(username='teacher2', password='password123')
        self.student = User.objects.create_user(username='student2', password='password123')
        
        self.course = Course.objects.create(
            name="Advanced Python",
            description="Deep dive into Python.",
            price=150,
            teacher=teacher
        )
        
        self.course_member = CourseMember.objects.create(
            course=self.course,
            user=self.student,
            roles='std'
        )

    def test_course_member_creation(self):
        """
        Test that a CourseMember instance is created with correct relationships.
        """
        self.assertEqual(self.course_member.course, self.course)
        self.assertEqual(self.course_member.user, self.student)
        self.assertEqual(self.course_member.roles, 'std')

    def test_course_member_str_representation(self):
        """
        Test the __str__ method of the CourseMember model.
        """
        # f-string harus berada dalam satu baris
        expected_str = f"{self.course.name} : {self.student.username}"
        self.assertEqual(str(self.course_member), expected_str)

    def test_course_member_role_options(self):
        """
        Test that the assigned role is a valid choice.
        
        Note: This test assumes ROLE_OPTIONS is an iterable (like a list of tuples)
        defined in your models.py file.
        """
        valid_roles = dict(ROLE_OPTIONS).keys()
        self.assertIn(self.course_member.roles, valid_roles)