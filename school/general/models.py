from django.db import models
from  staff.models import Staff

"""
program = title, credit, duration, description, image
testimonial = fullname, role, content, image
actuality = title, facilitator, description, image
about = description, image
service = name, description, image
"""


class Program(models.Model):
    title = models.CharField("Titre",max_length=100)
    credit = models.DecimalField("Credit",max_digits=10,null=True, default= 0.0, decimal_places= 2)
    duration = models.CharField("Durée",max_length=60)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='program_images/', null=True, blank=True)
    
    class Meta:
        db_table = 'program'
        verbose_name = 'Programme'
        verbose_name_plural = 'Programmes'
        
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    ROLE_CHOISE = (
        ('parent', 'Parent'), 
        ('almni', 'Ancien élève'),
        ('student', 'Elève'),
        ('staff', 'cadre')
    )
    
    fullname = models.CharField("Temoin",max_length=100)
    role = models.CharField("Role",max_length=60, choices=ROLE_CHOISE)
    content = models.TextField("Temoignage",null=True)
    image = models.ImageField(upload_to='testimonial_images/', null=True)
    
    class Meta:
        db_table = 'testimonial'
        verbose_name = 'Témoignage'
        verbose_name_plural = 'Témoignages'
        
        
    def __str__(self):
        return self.fullname

class Actuality(models.Model):
    title = models.CharField("Titre",max_length=100)
    facilitator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='actuality_images/', null=True)
    
    class Meta:
        db_table = 'actuality'
        verbose_name = 'Actualité'
        verbose_name_plural = 'Actualités'
        
        
    def __str__(self):
        return self.title

class About(models.Model):
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='about_images/', null=True)
    
    class Meta:
        db_table = 'about'
        verbose_name = 'A propo'
        
        
    def __str__(self):
        return self.description     
    

class Service(models.Model):
    name = models.CharField("Service",max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='service_images/')
    
    class Meta:
        db_table = 'service'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name