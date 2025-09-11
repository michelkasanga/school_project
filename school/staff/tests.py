from django.test import TestCase
from .models import Staff, Role

class StaffTestCase(TestCase):
	def test_create_staff(self):
		role = Role.objects.create(name="Professeur")
		staff = Staff.objects.create(name="Professeur X", surname="Test", firstname="Testy", role=role)
		self.assertEqual(str(staff), "Professeur X")

# Create your tests here.
