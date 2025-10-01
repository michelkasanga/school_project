"""
Fichier d'administration Django pour la gestion des modèles financiers.
Toutes les classes et fonctions sont documentées selon les standards Pylint.
"""

from django.contrib import admin
from .models import *
from .forms import *


@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Fees.
    Permet la gestion des frais scolaires.
    """
    form = FeesForm
    list_display = ['name', 'amount', 'get_classe', 'section','get_options','formatted_created_at', 'formatted_updated_at']
    list_filter = ['classe', 'section', 'options']
    
    
    def get_classe(self, obj):
        """
        Récupère les classes associées à un frais.
        """
        return ", ".join([classe.name for classe in obj.classe.all()])  
    get_classe.short_description = 'Classes'
    
    def get_options(self, obj):
        """
        Récupère les options associées à un frais.
        """
        return ", ".join([option.name for option in obj.options.all()]) 
    get_options.short_description = 'Options'
    
    
@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Box.
    Gère les paiements des frais scolaires par les étudiants.
    """
    form = BoxForm
    list_display = ['student', 'fees', 'amount_pay','month', 'type_paiement', 'collector', 'paid_date', 'updated_at']
    
    list_filter = ['fees', 'type_paiement'] #ajout de filtres
    readonly_fields = ['collector', 'updated_at'] #champs en lecture seule
    
    def get_fields(self, request, obj = None):
        """
        Récupère les champs à afficher dans le formulaire d'administration.
        Exclut le champ 'collector' de la modification.
        """
        fiels = super().get_fields(request, obj)
        if 'collector' in fiels:
            fiels.remove('collector') #on ne veut pas que l'utilisateur puisse modifier le recepteur
        
        return fiels
    
    def save_model(self, request, obj, form, change):
        """
        Sauvegarde le modèle Box.
        Assigne le collecteur automatiquement si non spécifié.
        """
        if not obj.collector:
            if hasattr(request.user , 'staff'):
                obj.collector = request.user.staff
        super().save_model(request, obj, form, change)
        

# Admin pour la table Total
@admin.register(Total)
class TotalAdmin(admin.ModelAdmin):
    """
    Classe d'administration pour le modèle Total.
    Affiche les totaux des paiements des frais scolaires par mois.
    """
    list_display = ['fees', 'month', 'nbrStudents', 'total_pay', 'total_amount', 'reste', 'statut', 'updated_at']
    list_filter = ['fees', 'month', 'statut']
    readonly_fields = ['fees', 'month', 'nbrStudents', 'total_pay', 'total_amount', 'reste', 'statut', 'updated_at']
    search_fields = ['fees__name', 'month']

    def has_add_permission(self, request):
        """
        Restreint l'ajout de nouveaux enregistrements dans la table Total.
        """
        from django.contrib import messages
        if request.method == "GET" and request.path.endswith("/add/"):
            return
        return False