from django.contrib import admin
from .models import Fees
from .forms import FeesForm

@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    form = FeesForm
    list_display = ['name', 'amount', 'get_classe', 'section','get_options','formatted_created_at', 'formatted_updated_at']
    list_filter = ['classe', 'section', 'options']
    
    
    def get_classe(self, obj):
        return ", ".join([classe.name for classe in obj.classe.all()])  
    get_classe.short_description = 'Classes'
    
    def get_options(self, obj):
        return ", ".join([option.name for option in obj.options.all()]) 
    get_options.short_description = 'Options'
