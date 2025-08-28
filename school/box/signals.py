from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Box


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