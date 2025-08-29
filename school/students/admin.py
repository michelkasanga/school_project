from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Students    

class StudentsInline(admin.StackedInline):
    model = Students
    can_delete = False
    verbose_name_plural = 'Students'
    fk_name = 'user' #on lie le profile a l'utilisateur
    fieldsets = (
        ('Informations Élève', {
            'fields': ('name', 
                       'surname',
                       'first_name',
                       'matricule',
                       'classe', 
                       'section', 
                       'option', 
                       'date_birthday',
                       'place_birthday'),
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
    
class CustomUserAdmin(UserAdmin):
    inlines = (StudentsInline,)
    list_display = ('username', 'first_name', 'last_name', 'is_staff')  
   
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)    