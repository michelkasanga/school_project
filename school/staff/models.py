from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    name = models.CharField("Role",max_length=100, unique=False, null=False, blank=False)
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
    
#________________________________________________________



class Staff(models.Model):
    
    SEXE_CHOICE = [
        ('masculin', 'Masculin'),
        ('féminin', 'Feminin')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Nom",max_length=100, unique=False, null=False, blank=False)
    surname = models.CharField("Post Nom",max_length=100, unique=False, null=False, blank=False)
    firstname = models.CharField("Prenom",max_length=100, unique=False, null=False, blank=False)
    sexe = models.CharField(max_length=10, null= True,  choices=SEXE_CHOICE)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name='staff_members')
    degree = models.CharField("Niveau d'etude",max_length=100, unique=False, null=True, blank=True)
    faculty = models.CharField("Domaine",max_length=100, unique=False, null=True, blank=True) 
    matricule = models.CharField(max_length=100, unique=True, blank=True, editable=False)
    date_birthday = models.DateField("Date de naissance",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'fonctionnaire'
        verbose_name_plural = 'fonctionnaires'
        ordering = ['role', 'name']
            
    #representation textuelle      
    def __str__(self):
        return self.name
    
    #format de date
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") # Format as needed
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
#creation automatique de l'utilisateur lie au fonctionnaire
