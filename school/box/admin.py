from django.contrib import admin
from .models import Box

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['student', 'fees', 'amount_pay', 'type_paiement', 'collector', 'paid_date', 'updated_at']
    list_filter = ['fees', 'type_paiement'] #ajout de filtres
    labels = ['Elève', 'Frais', 'Montant', 'Recepteur', 'Type de paiement']
    readonly_fields = ['collector', 'updated_at'] #champs en lecture seule
    
    def get_fields(self, request, obj = None):
        fiels = super().get_fields(request, obj)
        if 'recepteur' in fiels:
            fiels.remove('recepteur') #on ne veut pas que l'utilisateur puisse modifier le recepteur
        
        return fiels
    
    def save_model(self, request, obj, form, change):
        if not obj.collector:
            if hasattr(request.user , 'staff'):
                obj.collector = request.user.staff
        super().save_model(request, obj, form, change)
        
    
