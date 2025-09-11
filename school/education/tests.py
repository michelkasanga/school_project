from django.test import TestCase
from .models import Classes

class EducationTestCase(TestCase):
	def test_create_class(self):
		classe = Classes.objects.create(name="6ème A")
		self.assertEqual(str(classe), "6ème A")

# Create your tests here.
