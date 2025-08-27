from django.db import models
from staff.models import Staff
from students.models import Students
from fees.models import Fees

class Box(models.Model):
    student = models.ForeignKey(Students, on_delete= models.CASCADE, null=False, blank=False )
    fees = models.ForeignKey(Fees, on_delete= models.CASCADE, null=False, blank=False )
    amount_pay = models.PositiveIntegerField(null=False)
    collector = models.ForeignKey(Staff, on_delete=models.PROTECT, null=False)
    paid_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Caisse"
        verbose_name_plural="caisse"
        
    def __str__(self):
            return self.student, self.fees, self.collector
        
        
    
    


