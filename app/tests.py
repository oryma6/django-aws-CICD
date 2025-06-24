from django.test import TestCase

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your tests here.
class AppTestCase(TestCase):
    
    def setUp(self):
        user = User.objects.create_user(username='test', password='password123$', email='test@example.com', first_name='Test')
        print(user.username)
        
    def test_login(self):
        auth_user = authenticate(username='test', password=u'password123$')
        self.assertNotEqual(auth_user, None)