from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Staff, Role, Dean
from .forms import StaffForm, RoleForm, DeanForm


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
    list_display = ['name', 'surname', 'firstname','sexe', 'email', 'contact', 'title','get_role', 'degree', 'faculty', 'matricule', 'date_birthday', 'admin']
    fields = ('name', 'surname', 'firstname','sexe', 'email', 'contact', 'title', 'role', 'degree', 'faculty', 'matricule', 'date_birthday', 'admin')
    readonly_fields = ('matricule',)
    
    def get_role(self, obj):
        return ", ".join([role.name for role in obj.role.all() ])
    get_role.short_description = "Role"
    
    
  
@admin.register(Dean)
class DeanAdmin(admin.ModelAdmin):
    form = DeanForm
    list_display = ['Titulaire', 'section', 'option', 'get_course', 'start_date', 'end_date' ]
    
    def get_course(self, obj):
        return ", ".join([course.name for course in obj.course.all()])
    get_course.short_description = 'Course'
    
    def Titulaire(self, obj):
        return f"{obj.staff.firstname} {obj.staff.name}"