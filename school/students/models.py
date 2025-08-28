from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from options.models import Options
from section.models import Section
from classes.models import Classes
from django.utils import timezone  
from phonenumber_field.modelfields import PhoneNumberField


class Students(models.Model):
    name = models.CharField(max_length=60, null= False, blank=False)
    surname = models.CharField(max_length=60, null = False, blank=False)
    first_name = models.CharField(max_length=60, null = False, blank=False)
    matricule = models.CharField(max_length=100, unique=True, blank=True)
    classe = models.ForeignKey(Classes, on_delete=models.SET_NULL , null=True, )
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null = True)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True)
    date_birthday = models.DateField(null=True, blank=True)
    place_birthday = models.CharField(max_length=60, null= True, blank= True)
    address =  models.CharField(max_length=255, null= True, blank= True)
    father_name =  models.CharField(max_length=150, null= True, blank= True)
    mother_name =  models.CharField(max_length=150, null= True, blank= True)
    garduan =  models.CharField(max_length=150, null= True, blank= True)
    contact_garduan = PhoneNumberField( region='CD' ,null= True, blank= True, unique= True)
    address_garduan = models.CharField(max_length=255, null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        db_table = 'students'
        verbose_name = 'élève'
        verbose_name_plural = 'élèves'
        ordering = [ 'name']
        
    #sauvegarde automatique du matricule et creation
    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)  # Save to get an ID 
        if not self.matricule:
           self.matricule = f"{timezone.now.year}{self.id} - {self.name[:1].upper()}"
           super.save(*args, **kwargs)
        else:   
            super().save(*args, **kwargs)
            
    #representation textuelle      
    def __str__(self):
        return {self.name},{self.surname},{self.firstname}, {self.matricule}
    
    #format de date
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") # Format as needed
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
#creation automatique de l'utilisateur lie au fonctionnaire
@receiver(post_save, sender=Students)    
def create_user_for_staff(sender, instance, created, **kwargs):
    if created and not instance.user:
       username = instance.matricule
       password = instance.name + instance.date_birthday.strftime("%Y%m%d")
       user = User.objects.create_user(
              username=username,
              password=password,
              first_name=instance.name,
              last_name=instance.surname,
              is_staff=False
       )
       instance.user = user
       instance.save()
