from django.test import TestCase
from .models import Students
import uuid

class StudentsTestCase(TestCase):
	def test_create_student(self):
		student = Students.objects.create(
			name='Test', surname='Eleve', first_name='Testy', matricule=str(uuid.uuid4())
		)
		self.assertTrue(Students.objects.filter(matricule=student.matricule).exists())

# Create your tests here.
