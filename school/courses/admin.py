from django.contrib import admin
from .models import Courses
from .forms import CoursesForm

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    form = CoursesForm
    list_display = ['professor', 'get_courses', 'get_classes', 'section', 'option']
    list_filter = ['professor', 'section', 'option']
    search_fields = ['professor__name', 'section__name', 'option__name']
    ordering = ['professor']
    
    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.course.all()])
    get_courses.short_description = 'Cours'
    
    def get_classes(self, obj):
        return ", ".join([classe.name for classe in obj.classe.all()])
    get_classes.short_description = 'Classes'