from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from role.models import Role 
from django.utils import timezone  




class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, unique=False, null=False, blank=False)
    surname = models.CharField(max_length=100, unique=False, null=False, blank=False)
    firstname = models.CharField(max_length=100, unique=False, null=False, blank=False)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name='staff_members')
    degree = models.CharField(max_length=100, unique=False, null=True, blank=True)
    faculty = models.CharField(max_length=100, unique=False, null=True, blank=True) 
    matricule = models.CharField(max_length=100, unique=True, blank=True)
    date_birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'fonctionnaire'
        verbose_name_plural = 'fonctionnaires'
        ordering = ['role', 'name']
        
    #sauvegarde automatique du matricule et creation
    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)  # Save to get an ID 
        if not self.matricule:
           self.matricule = f"{timezone.now.year}{self.id} - {self.name[:2].upper()}"
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
@receiver(post_save, sender=Staff)    
def create_user_for_staff(sender, instance, created, **kwargs):
    if created and not instance.user:
       username = instance.matricule
       password = instance.name + instance.date_birthday.strftime("%Y") + instance.surname
       user = User.objects.create_user(
              username=username,
              password=password,
              first_name=instance.name,
              last_name=instance.surname,
              is_staff=True 
       )
       instance.user = user
       instance.save()