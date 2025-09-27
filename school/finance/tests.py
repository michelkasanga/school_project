
from django.test import TestCase
from .models import Fees, Box, Total
from students.models import Students
import uuid

class BoxPaymentTestCase(TestCase):
	def setUp(self):
		self.student = Students.objects.create(
			name='Test', surname='Eleve', first_name='Testy', matricule=str(uuid.uuid4())
		)
		self.fees = Fees.objects.create(name="Frais Scolarité", amount=10000)
	def test_add_payment_exact_month(self):
		Box.add_payment(self.student, self.fees, 1, 10000)
		total = Total.objects.get(student=self.student, fees=self.fees, month=1)
		self.assertEqual(total.amount, 10000)
	def test_add_payment_overflow_next_month(self):
		Box.add_payment(self.student, self.fees, 1, 15000)
		total1 = Total.objects.get(student=self.student, fees=self.fees, month=1)
		total2 = Total.objects.get(student=self.student, fees=self.fees, month=2)
		self.assertEqual(total1.amount, 10000)
		self.assertEqual(total2.amount, 5000)
	def test_delete_box_updates_total(self):
		box = Box.add_payment(self.student, self.fees, 1, 10000)
		box.delete()
		self.assertFalse(Total.objects.filter(student=self.student, fees=self.fees, month=1).exists())


