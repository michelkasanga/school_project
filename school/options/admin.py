from django.contrib import admin
from .models import Options
from .forms import OptionsForm

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):   
    form = OptionsForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
