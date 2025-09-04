from django.contrib import admin
from .models import *
from .forms import *


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    form = SectionForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):   
    form = OptionsForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    list_per_page = 10
    search_fields = ['name']

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    form = ClassesForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    
    

@admin.register(Tutors)
class TutorsAdmin(admin.ModelAdmin):
    form = TutorsForm
    list_display = ['staff', 'classe', 'section', 'option']
    list_filter = ['classe', 'section', 'option'] #ajout de filtres
    search_fields = ['staff__name', 'classe__name'] #champs de recherche


   
@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    form = CoursesForm
    list_display = ['professor', 'get_course', 'get_classes', 'section', 'option']
    list_per_page = 10
    search_fields = ['name']
    #filter_horizontal = ('course', 'classe')
    
    def get_course(self, obj):
        return ", ".join([course.name for course in obj.course.all()])
    get_course.short_description = 'Course'
    
    def get_classes(self, obj):
        return ", ".join([classes.name for classes in obj.classe.all()])
    get_classes.short_description = 'Classes'
    