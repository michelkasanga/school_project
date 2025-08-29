from django.contrib import admin
from .models import Classes, Tutors

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    
    

@admin.register(Tutors)
class TutorsAdmin(admin.ModelAdmin):
    list_display = ['staff', 'classe', 'section', 'option']
    list_filter = ['classe', 'section', 'option'] #ajout de filtres
    search_fields = ['staff__name', 'classe__name'] #champs de recherche