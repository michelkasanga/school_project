from django.db import models
from education.models import *
from students.models import Students
from staff.models import Staff
from django.db.models.signals import post_save
from django.dispatch import receiver



class Fees(models.Model):
    name = models.CharField("Frais",max_length=100, unique=False, null=False, blank=False)
    amount = models.DecimalField("Montant",max_digits=10, decimal_places=2, null=False, blank=False)
    classe = models.ManyToManyField(Classes)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    options = models.ManyToManyField(Options, blank=True)
    created_at = models.DateTimeField("Creation",auto_now_add=True)
    updated_at = models.DateTimeField("Modification",auto_now=True)
    
    class Meta:
        db_table='fees'
        verbose_name = 'frais'
        verbose_name_plural = 'frais'
        ordering = ['updated_at']  
    
    def __str__(self):
        return self.name
    
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    
    #__________________________________________
class Box(models.Model):
    TYPE_PAIEMENT_CHOICES = [
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement'),
        ('carte', 'Carte bancaire'),
    ]
    
    MONTH_CHOICES = [
        ('septembre', 'Septembre'),('octobre', 'Octobre'),('novembre', 'Novembre'),
        ('decembre', 'Décembre'),('janvier', 'Janvier'),('fevrier', 'Fevrier'), 
        ('mars', 'Mars'),('avril', 'Avril'),('mai', 'Mai'),('juin', 'Juin')
    ]
    student = models.ForeignKey(Students, on_delete= models.CASCADE, null=False, blank=False )
    fees = models.ForeignKey(Fees, on_delete= models.CASCADE, null=False, blank=False )
    amount_pay = models.DecimalField("Montant", max_digits=10, decimal_places=2)
    month = models.CharField('Mois', max_length=60, choices= MONTH_CHOICES)
    type_paiement = models.CharField("Type de paiement",max_length=20, choices=TYPE_PAIEMENT_CHOICES, default='espece')
    collector = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, editable=False)
    paid_date = models.DateTimeField("Date de paiment",auto_now_add=True)
    updated_at = models.DateTimeField("Modification",auto_now=True)
    
    class Meta:
        db_table='box'
        verbose_name = "Caisse"
        verbose_name_plural="caisse"
   
        
        
    
    



