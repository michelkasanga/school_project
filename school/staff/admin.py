"""
Fichier d'administration Django pour la gestion des modèles du personnel.
Toutes les classes et fonctions sont documentées selon les standards Pylint.
"""

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Staff, Role, Dean
from .forms import StaffForm, RoleForm, DeanForm


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):  
    """
    Classe d'administration pour le modèle Role.
    Permet la gestion des rôles attribués au personnel.
    """
    form = RoleForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 10
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Staff.
    Permet la gestion des informations relatives au personnel.
    """
    form = StaffForm
    list_display = ['name', 'surname', 'firstname','sexe', 'email', 'contact', 'title','get_role', 'degree', 'faculty', 'matricule', 'date_birthday', 'admin']
    fields = ('name', 'surname', 'firstname','sexe', 'email', 'contact', 'title', 'role', 'degree', 'faculty', 'matricule', 'date_birthday', 'admin')
    readonly_fields = ('matricule',)
    
    def get_role(self, obj):
        """
        Récupère les rôles associés à un membre du personnel.
        """
        return ", ".join([role.name for role in obj.role.all() ])
    get_role.short_description = "Role"
    
    
  
@admin.register(Dean)
class DeanAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Dean.
    Permet la gestion des doyens et des cours associés.
    """
    form = DeanForm
    list_display = ['Titulaire', 'section', 'option', 'get_course', 'start_date', 'end_date' ]
    
    def get_course(self, obj):
        """
        Récupère les cours associés à un doyen.
        """
        return ", ".join([course.name for course in obj.course.all()])
    get_course.short_description = 'Course'
    
    def Titulaire(self, obj):
        """
        Récupère le nom complet du titulaire (doyen).
        """
        return f"{obj.staff.firstname} {obj.staff.name}"