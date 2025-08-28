from django.db import models
from classes.models import Classes
from options.models import Options
from section.models import Section

class Fees(models.Model):
    name = models.CharField(max_length=100, unique=False, null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    classe = models.ManyToManyField(Classes)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    options = models.ManyToManyField(Options)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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