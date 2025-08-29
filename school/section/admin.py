from django.contrib import admin
from .models import Section
from .forms import SectionForm

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    form = SectionForm
    list_display = ['name', 'formatted_created_at', 'formatted_updated_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
