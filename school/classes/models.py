from django.db import models
from staff.models import Staff
from options.models import Options
from section.models import Section

class Classes(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'classe'
        verbose_name_plural = 'classes'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    

class Tutors(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classes, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null= True, blank=True)
    
    class Meta:
        verbose_name = 'Titulaire'
        verbose_name_plural = 'Titulaires'
    