
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from .models import *


def get_current_user(sender, instance, **kwargs):
    # Fonction pour obtenir l'utilisateur actuellement connecté
    # Cette fonction doit être adaptée en fonction de la manière dont vous gérez les utilisateurs dans votre application
    # Par exemple, si vous utilisez Django's authentication system, vous pouvez accéder à l'utilisateur via request.user
    # Cependant, dans un signal, vous n'avez pas accès à la requête directement.
    # Vous pourriez envisager d'utiliser un middleware ou une autre approche pour stocker l'utilisateur actuel.
    if not instance.collector:
        User = get_user_model()
        last_user = User.objects.order_by('-collector').first()# Exemple simple, à adapter selon votre logique
        if last_user and hasattr(last_user, 'staff'):
            instance.collector = last_user.staff


    @receiver(post_save,sender=Fees)
    def ajout_option(sender, instance, created, **kwargs):
        if created and instance.options.count() == 0:
            option_default, _ = Options.objects.get_or_create(option = "Aucun")
            instance.options.add(option_default)
            
    
    
from django.db.models import Sum, Count

# Signal pour mettre à jour la table Total à chaque paiement dans la caisse
@receiver(post_save)
def update_total_on_box_save(sender, instance, **kwargs):
    from .models import Box, Total
    if not isinstance(instance, Box):
        return
    Total.update_totals_for_fees_and_month(instance.fees, instance.month)



