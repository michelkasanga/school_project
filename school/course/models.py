from django.db import models
from section.models import Section

class Course(models.Model):
    name = models.CharField(max_length= 255, null=False, blank=False)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'cours'
        verbose_name_plural = 'cours'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
