from django.contrib import admin
from .models import Role
from .forms import RoleForm

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):  
    form = RoleForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 10
    readonly_fields = ['created_at', 'updated_at']

