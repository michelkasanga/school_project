from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from education.models import *

from django.utils import timezone  
from phonenumber_field.modelfields import PhoneNumberField


class Students(models.Model):
    
    SEXE_CHOICE = [
        ('masculin', 'Masculin'),
        ('feminin', 'Feminin')
    ]
    STATUT_CHOICE = [
        ('scolariser', 'Scolariser 🟡 '),
        ('exempter', 'Exempter 🟢')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Nom",max_length=60, null= False, blank=False)
    surname = models.CharField("Post Nom",max_length=60, null = False, blank=False)
    first_name = models.CharField("Prenom",max_length=60, null = False, blank=False)
    sexe = models.CharField(max_length=10, null=True, choices=SEXE_CHOICE, default="masculin")
    matricule = models.CharField(max_length=100, unique=True, blank=True)
    classe = models.ForeignKey(Classes, on_delete=models.SET_NULL , null=True )
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null = True)
    option = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True, blank=True)
    date_birthday = models.DateField("Date de naissance",null=True, blank=True)
    place_birthday = models.CharField("Lieu de naissance",max_length=60, null= True, blank= True)
    address =  models.CharField("Adresse",max_length=255, null= True, blank= True)
    statut = models.CharField(max_length=10, null=True, choices=STATUT_CHOICE, default="scolariser")
    father_name =  models.CharField("Père",max_length=150, null= True, blank= True)
    mother_name =  models.CharField("Mère",max_length=150, null= True, blank= True)
    garduan =  models.CharField("Tuteur",max_length=150, null= True, blank= True)
    contact_garduan = PhoneNumberField("Contact du tuteur", region='CD' ,null= True, blank= True, unique= True)
    address_garduan = models.CharField("Adresse du Tuteur",max_length=255, null= True, blank= True)
    created_at = models.DateTimeField("Date d'inscription",auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    class Meta:
        db_table = 'students'
        verbose_name = 'élève'
        verbose_name_plural = 'élèves'
        ordering = [ 'name']
        
    #sauvegarde automatique du matricule et creation
    def save(self, *args, **kwargs):
        # Génère le matricule après la première sauvegarde si besoin, sans double insert
        if not self.id and not self.matricule:
            super().save(*args, **kwargs)  # Première sauvegarde pour avoir l'ID
            from django.utils import timezone
            self.matricule = f"{timezone.now().year}{self.id} - {self.name[:1].upper()}"
            super().save(update_fields=['matricule'])  # Mise à jour du matricule uniquement
        else:
            super().save(*args, **kwargs)
            
    #representation textuelle      
    def __str__(self):
        return f" {self.name} {self.surname} {self.first_name} "
    
    #format de date
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") # Format as needed
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    

    @classmethod
    def get_students_for_payment(cls):
        """
        Retourne les élèves qui ne sont pas exempter (statut différent de 'exempter').
        """
        return cls.objects.exclude(statut__iexact='exempter')


