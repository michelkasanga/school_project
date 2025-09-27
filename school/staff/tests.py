from django.test import TestCase
from .models import Staff, Role

class StaffTestCase(TestCase):
	def test_create_staff(self):
		from datetime import date
		role = Role.objects.create(name="Professeur")
		staff = Staff.objects.create(name="Professeur X", surname="Test", firstname="Testy", date_birthday=date(1990,1,1))
		staff.role.set([role])
		self.assertEqual(str(staff), "Professeur X")

# Create your tests here.
