
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

from .models import Box, Fees, Students, Staff, MonthChoice, Total
from decimal import Decimal
from django.db.models import Sum

class BoxPaymentTestCase(TestCase):
	def setUp(self):
		import uuid
		self.student = Students.objects.create(name='Test', surname='Eleve', first_name='Testy', matricule=str(uuid.uuid4()))
		self.staff = Staff.objects.create(name='Test', surname='Staff', firstname='Testy')
		self.fees = Fees.objects.create(name='Frais Scolarité', amount=10000)

	def test_add_payment_exact_month(self):
		box = Box.objects.create(student=self.student, fees=self.fees, amount_pay=0, month=MonthChoice.SEPTEMBRE, collector=self.staff)
		box.add_payment(10000)
		self.assertEqual(Box.objects.filter(student=self.student, fees=self.fees, month=MonthChoice.SEPTEMBRE).aggregate(Sum('amount_pay'))['amount_pay__sum'], Decimal('10000'))
		total = Total.objects.get(fees=self.fees, month=MonthChoice.SEPTEMBRE)
		self.assertEqual(total.total_pay, Decimal('10000'))
		self.assertEqual(total.reste, Decimal('0'))
		self.assertTrue(total.statut)

	def test_add_payment_overflow_next_month(self):
		box = Box.objects.create(student=self.student, fees=self.fees, amount_pay=0, month=MonthChoice.SEPTEMBRE, collector=self.staff)
		box.add_payment(15000)
		# Septembre doit être plein, octobre reçoit l'excédent
		self.assertEqual(Box.objects.filter(student=self.student, fees=self.fees, month=MonthChoice.SEPTEMBRE).aggregate(Sum('amount_pay'))['amount_pay__sum'], Decimal('10000'))
		self.assertEqual(Box.objects.filter(student=self.student, fees=self.fees, month=MonthChoice.OCTOBRE).aggregate(Sum('amount_pay'))['amount_pay__sum'], Decimal('5000'))
		total_sep = Total.objects.get(fees=self.fees, month=MonthChoice.SEPTEMBRE)
		total_oct = Total.objects.get(fees=self.fees, month=MonthChoice.OCTOBRE)
		self.assertEqual(total_sep.total_pay, Decimal('10000'))
		self.assertEqual(total_sep.reste, Decimal('0'))
		self.assertTrue(total_sep.statut)
		self.assertEqual(total_oct.total_pay, Decimal('5000'))
		self.assertEqual(total_oct.reste, Decimal('5000'))
		self.assertFalse(total_oct.statut)

	def test_delete_box_updates_total(self):
		box = Box.objects.create(student=self.student, fees=self.fees, amount_pay=10000, month=MonthChoice.SEPTEMBRE, collector=self.staff)
		box2 = Box.objects.create(student=self.student, fees=self.fees, amount_pay=5000, month=MonthChoice.SEPTEMBRE, collector=self.staff)
		# Total avant suppression
		total = Total.objects.get(fees=self.fees, month=MonthChoice.SEPTEMBRE)
		self.assertEqual(total.total_pay, Decimal('15000'))
		# Suppression d'un paiement
		box2.delete()
		total.refresh_from_db()
		self.assertEqual(total.total_pay, Decimal('10000'))
		self.assertEqual(total.reste, Decimal('0'))
		self.assertTrue(total.statut)
