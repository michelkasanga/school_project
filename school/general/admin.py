"""
Fichier d'administration Django pour la gestion des modèles généraux (actualités, services, etc.).
Toutes les classes et fonctions sont documentées selon les standards Pylint.
"""

from django.contrib import admin
from .models import *
from .forms import *
from django.utils.html import format_html


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Program.
    """
    form = ProgramForm
    list_display = ['title', 'credit','level', 'duration', 'image_preview']
    search_fields = ['title']
    ordering = ['title']
    
    def image_preview(self, obj):
        """
        Affiche un aperçu de l'image du programme.
        """
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Testimonial.
    """
    form = TestimonialForm
    list_display = ['fullname', 'role', 'content', 'image_preview']
    search_fields = ['fullname']
    ordering = ['fullname']
    
    def image_preview(self, obj):
        """
        Affiche un aperçu de l'image du témoignage.
        """
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
    
    
@admin.register(Actuality)
class ActualityAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Actuality.
    """
    form = ActualityForm
    list_display = ['title', 'facilitator', 'place', 'end','category','date', 'image_preview']
    search_fields = ['title']
    ordering = ['title']
    
    
    def image_preview(self, obj):
        """
        Affiche un aperçu de l'image de l'actualité.
        """
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
      

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle About.
    """
    form = AboutForm
    list_display = [ 'image_preview','imag', 'mission']
  
    def image_preview(self, obj):
        """
        Affiche un aperçu de l'image principale de la section À propos.
        """
        if obj.image:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'image'
    
    def imag(self, obj):
        """
        Affiche un aperçu de l'image secondaire de la section À propos.
        """
        if obj.image_2:
           return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.image_2.url)
        return "-"
    image_preview.short_description = 'image'
    
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Hero.
    """
    form = HeroForm
    list_display = ["title", "open_date", "close_date", "register_date"]
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Contact.
    """
    form = ContactForm
    list_display = ["email" ,"tel", "address"]


