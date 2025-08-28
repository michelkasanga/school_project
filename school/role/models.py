from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100, unique=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='role'
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        ordering = ['name']  
    
    def __str__(self):
        return self.name
    
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    

