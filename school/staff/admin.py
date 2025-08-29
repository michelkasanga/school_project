from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Staff

class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'fonctionnaire'
    fk_name = 'user'
    fields = ('name', 'surname', 'firstname', 'role', 'degree', 'faculty', 'matricule', 'date_birthday')
    readonly_fields = ('matricule',)
    
class CustomUserAdmin(UserAdmin):
    inlines = (StaffInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    
    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

