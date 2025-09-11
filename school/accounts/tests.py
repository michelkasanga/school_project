from django.test import TestCase
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
	def test_create_user(self):
		user = User.objects.create_user(username='testuser', password='testpass')
		self.assertTrue(User.objects.filter(username='testuser').exists())

# Create your tests here.
