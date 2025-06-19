from django.test import TestCase
from django.urls import reverse
from .models import Course

class CourseViewTest(TestCase):
    """
    Integration tests for views related to the Course model.
    """

    def setUp(self):
        """
        Set up initial data for the tests, creating a couple of Course objects.
        """
        Course.objects.create(
            name="Django for Beginners", 
            description="Learn Django from scratch.", 
            price=100
        )
        Course.objects.create(
            name="Advanced Django", 
            description="Deep dive into Django.", 
            price=200
        )

    def test_course_list_view(self):
        """
        Test the course list view for status code, template usage, and content.
        """
        # Get the URL for the course_list view
        url = reverse('course_list')
        
        # Make a GET request to the URL
        response = self.client.get(url)
        
        # 1. Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # 2. Check that the correct template is being used
        self.assertTemplateUsed(response, 'course_list.html')
        
        # 3. Check that the response contains the names of the created courses
        self.assertContains(response, "Django for Beginners")
        self.assertContains(response, "Advanced Django")