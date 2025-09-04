from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Staff, Role
from .forms import StaffForm, RoleForm


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):  
    form = RoleForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 10
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ['name', 'surname', 'firstname','sexe', 'role', 'degree', 'faculty', 'matricule', 'date_birthday']
    fields = ('name', 'surname', 'firstname','sexe', 'role', 'degree', 'faculty', 'matricule', 'date_birthday')
    readonly_fields = ('matricule',)
  

