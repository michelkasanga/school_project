from django.contrib import admin
from .models import Program, Testimonial, About, Service, Actuality
from .forms import ProgramForm, TestimonialForm, AboutForm, ServiceForm, ActualityForm

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramForm
    list_display = ['title', 'credit', 'duration', 'description']
    search_fields = ['title']
    ordering = ['title']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    form = TestimonialForm
    list_display = ['fullname', 'role', 'content']
    search_fields = ['fullname']
    ordering = ['fullname']

@admin.register(Actuality)
class ActualityAdmin(admin.ModelAdmin):
    form = ActualityForm
    list_display = ['title', 'facilitator','description']
    search_fields = ['title']
    ordering = ['title']

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    form = AboutForm
    list_display = ['description']
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']