"""
Fichier d'administration Django pour la gestion des comptes utilisateurs.
Toutes les classes et fonctions sont documentées selon les standards Pylint.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profiles


class ProfilesInline(admin.StackedInline):
    """Classe d'inline pour afficher et éditer le modèle Profiles dans l'admin."""
    model = Profiles
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'user'  # on lie le profile a l'utilisateur
    
class CustomUserAdmin(UserAdmin):
    """Administration personnalisée pour le modèle User."""
    inlines = (ProfilesInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'avatar_preview')
  
    def avatar_preview(self, obj):
        """Affiche un aperçu de l'avatar de l'utilisateur."""
        if obj.profiles.avatar:
            return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.profiles.avatar.url)
    avatar_preview.short_description = 'Avatar'
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
