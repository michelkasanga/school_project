from django.contrib import admin
from .models import Program, Testimonial, About,Actuality
from .forms import ProgramForm, TestimonialForm, AboutForm, ActualityForm
from django.utils.html import format_html


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    form = ProgramForm
    list_display = ['title', 'credit','level', 'duration', 'image_preview']
    search_fields = ['title']
    ordering = ['title']
    
    def image_preview(self, obj):
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    form = TestimonialForm
    list_display = ['fullname', 'role', 'content', 'image_preview']
    search_fields = ['fullname']
    ordering = ['fullname']
    
    def image_preview(self, obj):
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
    
    

@admin.register(Actuality)
class ActualityAdmin(admin.ModelAdmin):
    form = ActualityForm
    list_display = ['title', 'facilitator', 'place', 'end','category','date', 'image_preview']
    search_fields = ['title']
    ordering = ['title']
    
    
    def image_preview(self, obj):
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
      

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    form = AboutForm
    list_display = [ 'image_preview','imag', 'mission']
  
    def image_preview(self, obj):
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
    
    def imag(self, obj):
        if obj.image_2:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image_2.url)
        return "-"
    image_preview.short_description = 'image'
        
    
    