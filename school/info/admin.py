from django.contrib import admin
from .models import Program, Testimonial, About, Service, Actuality
from .forms import ProgramForm, TestimonialForm, AboutForm, ServiceForm, ActualityForm

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramForm
    list_display = ['title', 'credit', 'duration', 'description', 'image']
    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    form = TestimonialForm
    list_display = ['name', 'role', 'content', 'image']

    
@admin.register(Actuality)
class ActualityAdmin(admin.ModelAdmin):
    form = ActualityForm
    list_display = ['title', 'content', 'facilitator', 'image']    
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceForm
    list_display = ['name',  'description', 'image']

@admin.register(About)

class AboutAdmin(admin.ModelAdmin):
    form = AboutForm
    list_display = ['content', 'image']

    def has_add_permission(self, request):
       if About.objects.exists():
           return False
       return True
