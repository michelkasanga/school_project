from django.db import models
from staff.models import Staff
from students.models import Students
from fees.models import Fees

class Box(models.Model):
    TYPE_PAIEMENT_CHOICES = [
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement'),
        ('carte', 'Carte bancaire'),
    ]
    student = models.ForeignKey(Students, on_delete= models.CASCADE, null=False, blank=False )
    fees = models.ForeignKey(Fees, on_delete= models.CASCADE, null=False, blank=False )
    amount_pay = models.DecimalField(max_digits=10, decimal_places=2)
    type_paiement = models.CharField(max_length=20, choices=TYPE_PAIEMENT_CHOICES, default='espece')
    collector = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, editable=False)
    paid_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='box'
        verbose_name = "Caisse"
        verbose_name_plural="caisse"
        
    def __str__(self):
            return self.student, self.fees
        
        
    
    


