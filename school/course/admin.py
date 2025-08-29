from django.contrib import admin
from .models import Course
from .forms import CourseForm

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    list_per_page = 10
    search_fields = ['name']
