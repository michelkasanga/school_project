from django.db import models
from staff.models import Staff
from django.core.exceptions import ValidationError

class Program(models.Model):
   title = models.CharField(max_length=200)
   credit = models.DecimalField(max_digits=5, decimal_places=2)
   duration = models.CharField(max_length=100)
   description = models.TextField()
   image = models.ImageField(upload_to='program_images/', null=True, blank=True)
   
   class Meta:
       db_table = 'program'
       verbose_name = 'programme'
       verbose_name_plural = 'programmes'
       ordering = ['title']

class Testimonial(models.Model):
    
    ROLE_CHOICES = [
        ('student', 'Etudiant'),
        ('parent', 'Parent'),
        ('alumni', 'Ancien élève'),
        ('staff', 'Personnel'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True)
    
    class Meta:
         db_table = 'testimonial'
         verbose_name = 'témoignage'
         verbose_name_plural = 'témoignages'
         ordering = ['name']

class Actuality(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    facilitator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='actuality_images/', null=True, blank=True)
    published_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'actuality'
        verbose_name = 'actualité'
        verbose_name_plural = 'actualités'
        ordering = ['-published_date']

class About(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to= 'about/', null=True)
    
    class Meta:
        db_table = 'about'
        
    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            raise ValidationError('un autre enregitrement existe deja')
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.content

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to= 'service/', null=True)
