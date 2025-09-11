from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField




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
    TITLE_CHOICES = [
        ('Mr.' , 'Monsieur'),
        ('Mme.' , 'Madame'),
        ('Mlle.' , 'Mademoiselle'),
        ('Me.' , 'Maitre'),
        ('Dr.' , 'Docteur'),
        ('Pr.' , 'Professeur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Nom",max_length=100, unique=False, null=False, blank=False)
    surname = models.CharField("Post Nom",max_length=100, unique=False, null=False, blank=False)
    firstname = models.CharField("Prenom",max_length=100, unique=False, null=False, blank=False)
    sexe = models.CharField(max_length=10, null= True,  choices=SEXE_CHOICE, default="masculin")
    role = models.ManyToManyField(Role, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact = PhoneNumberField("Contact📞", region='CD' ,null= True, blank= True, unique= True)
    title = models.CharField("Titre",max_length=60, choices=TITLE_CHOICES, blank=True, null=True)
    degree = models.CharField("Niveau d'etude",max_length=100, unique=False, null=True, blank=True)
    faculty = models.CharField("Domaine",max_length=100, unique=False, null=True, blank=True) 
    matricule = models.CharField(max_length=100, unique=True, blank=True, editable=False)
    date_birthday = models.DateField("Date de naissance",null=True, blank=True)
    admin = models.BooleanField('Admin', default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'fonctionnaire'
        verbose_name_plural = 'fonctionnaires'
        ordering = [ 'name']
            
    #representation textuelle      
    def __str__(self):
        return self.name
    
    #format de date
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") # Format as needed
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    

class Dean(models.Model):
    from staff.models import Staff
    from education.models import Options, Section, Course
    
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, blank=True)
    start_date = models.DateField("Date de nommination", null=False)
    end_date = models.DateField("Date de fin mandat", blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Dean'
        verbose_name = 'Doyen'
        verbose_name_plural = 'Doyens'
        
    def __str__(self):
        return f"{self.staff.name} {self.staff.firstname}"
    
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") # Format as needed
    
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def format_start_date(self):
        return self.start_date.strftime("%d-%B-%Y")
     
    def format_end_date(self):
        
        return self.end_date.strftime("%d-%B-%Y") if self.end_date else "-"

    
    