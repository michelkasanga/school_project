from django.db import models
from staff.models import Staff
from options.models import Options
from section.models import Section

class Classes(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes')
    tutor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='tutored_classes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'classes'
        verbose_name = 'classe'
        verbose_name_plural = 'classes'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")