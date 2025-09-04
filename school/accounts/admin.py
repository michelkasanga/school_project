from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profiles


class ProfilesInline(admin.StackedInline):
    model = Profiles
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'user' #on lie le profile a l'utilisateur
    
class CustomUserAdmin(UserAdmin):
    inlines = (ProfilesInline,)
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'avatar')
  
    def avatar(self, obj):
        if hasattr(obj, 'profile') and obj.profile.avatar:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.profile.avatar.url)
        return "-"
    avatar.short_description = 'Avatar'
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
