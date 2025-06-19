import json
from django.test import TestCase
from django.contrib.auth.models import User
from lms_core.models import Course, CourseMember, CourseContent, Comment

# Note: The import for 'apiv1' is not used directly in the test case,
# but it's kept here if needed for other reasons.
# from lms_core.api import apiv1 

class APITestCase(TestCase):
    """
    Test suite for the LMS Core API (v1).
    
    This class tests the main API endpoints for courses, enrollment,
    contents, and comments, including authentication and authorization.
    """
    base_url = '/api/v1/'

    def setUp(self):
        """
        Set up initial data and authentication tokens for all tests.
        """
        # 1. Create users
        self.teacher = User.objects.create_user(username='teacher', password='password123')
        self.student = User.objects.create_user(username='student', password='password123')

        # 2. Create a course for testing
        self.course = Course.objects.create(
            name="Django for Beginners",
            description="Learn Django from scratch.",
            price=100,
            teacher=self.teacher
        )

        # 3. Log in and get tokens for both users
        # Teacher token
        login_response = self.client.post(
            f'{self.base_url}auth/sign-in',
            data=json.dumps({'username': 'teacher', 'password': 'password123'}),
            content_type='application/json'
        )
        self.teacher_token = login_response.json()['access']
        self.teacher_auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.teacher_token}'}

        # Student token
        login_response = self.client.post(
            f'{self.base_url}auth/sign-in',
            data=json.dumps({'username': 'student', 'password': 'password123'}),
            content_type='application/json'
        )
        self.student_token = login_response.json()['access']
        self.student_auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.student_token}'}

    def test_list_courses_unauthenticated(self):
        """Test that unauthenticated users can list courses."""
        response = self.client.get(f'{self.base_url}courses')
        self.assertEqual(response.status_code, 200)
        # Assuming pagination, the result is in the 'items' key
        self.assertEqual(len(response.json()['items']), 1)

    def test_create_course_by_teacher(self):
        """Test that a teacher can create a new course."""
        response = self.client.post(
            f'{self.base_url}courses', 
            data={
                'name': 'New Course',
                'description': 'New Course Description',
                'price': 150
            }, 
            format='json', # Use format='json' for dict data without files
            **self.teacher_auth_header
        )
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(response.json()['name'], 'New Course')

    def test_update_course_by_teacher(self):
        """Test that a teacher can update an existing course."""
        response = self.client.put( # Use PUT for full updates, PATCH for partial
            f'{self.base_url}courses/{self.course.id}',
            data={
                'name': 'Updated Course Name',
                'description': 'Updated Description',
                'price': 200
            },
            content_type='application/json',
            **self.teacher_auth_header
        )
        self.assertEqual(response.status_code, 200, response.json())
        self.assertEqual(response.json()['name'], 'Updated Course Name')

    def test_enroll_course_by_student(self):
        """Test that a student can enroll in a course."""
        response = self.client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
            **self.student_auth_header
        )
        self.assertEqual(response.status_code, 200, response.json())
        # Best practice: use object instead of _id for queries
        is_member = CourseMember.objects.filter(course=self.course, user=self.student).exists()
        self.assertTrue(is_member)

    def test_create_comment_by_enrolled_student(self):
        """Test that an enrolled student can comment on course content."""
        # 1. Create content and enroll student
        content = CourseContent.objects.create(course=self.course, name="Content Title", description="Content Description")
        self.client.post(f'{self.base_url}courses/{self.course.id}/enroll', **self.student_auth_header)

        # 2. Post a comment
        response = self.client.post(
            f'{self.base_url}contents/{content.id}/comments',
            data={'comment': 'This is a test comment'},
            content_type='application/json',
            **self.student_auth_header
        )
        self.assertEqual(response.status_code, 201, response.json())
        self.assertEqual(response.json()['comment'], 'This is a test comment')

    def test_delete_own_comment_by_student(self):
        """Test that a student can delete their own comment."""
        # 1. Setup: Create content, enroll student, and create a comment
        content = CourseContent.objects.create(course=self.course, name="Content Title", description="Content Description")
        self.client.post(f'{self.base_url}courses/{self.course.id}/enroll', **self.student_auth_header)
        comment_response = self.client.post(
            f'{self.base_url}contents/{content.id}/comments',
            data={'comment': 'Comment to be deleted'},
            content_type='application/json',
            **self.student_auth_header
        )
        comment_id = comment_response.json()['id']
        self.assertTrue(Comment.objects.filter(id=comment_id).exists())

        # 2. Action: Delete the comment
        delete_response = self.client.delete(
            f'{self.base_url}comments/{comment_id}',
            **self.student_auth_header
        )
        
        # 3. Assert: Check response and that the comment is gone
        self.assertEqual(delete_response.status_code, 204) # 204 No Content is common for successful deletes
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())