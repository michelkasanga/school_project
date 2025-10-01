"""
Fichier d'administration Django pour la gestion des modèles étudiants.
Toutes les classes et fonctions sont documentées selon les standards Pylint.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Students    
from .forms import StudentsForm

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Students.
    Permet la gestion des informations élèves et des informations parent/tuteur.
    """
    form =  StudentsForm
    list_display = ['name', 
            'surname',
            'first_name',
            'sexe',
            'matricule',
            'classe', 
            'section', 
            'option', 
            'date_birthday',
            'place_birthday',
            'address',
            'statut',
            'father_name', 
            'mother_name', 
            'garduan', 
            'contact_garduan', 
            'address_garduan',
            'created_at'
            ]
    fieldsets = (
        ('Informations Élève', {
            'fields': ('name', 
                       'surname',
                       'first_name',
                       'sexe',
                       'classe', 
                       'section', 
                       'option', 
                       'date_birthday',
                       'place_birthday',
                       'address',
                       'statut'),
            
            'classes': ('collapse',)  # Makes the section collapsible
        }),
        ('Informations Parent et Tuteur', {
            'fields': ('father_name', 
                       'mother_name', 
                       'garduan', 
                       'contact_garduan', 
                       'address_garduan'),
            'classes': ('collapse',)  # Makes the section collapsible
        }),
       
    )
