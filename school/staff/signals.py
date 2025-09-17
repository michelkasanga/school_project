
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Staff
from django.utils import timezone  

@receiver(post_save, sender=Staff)    
def create_user_and_matricule(sender, instance, created, **kwargs):
   if created:
    #sauvegarde automatique du matricule et creation
        if not instance.matricule:
            id_stf = str(instance.id)
            db_stf = instance.date_birthday.strftime("%y")
            nm = instance.name[:1].upper() if instance.name else 'X'
            tmz = timezone.now()
            
            instance.matricule = f"{tmz.strftime("%y")}{db_stf}{id_stf}-{nm}"
            instance.save(update_fields=["matricule"]) 
            
        if not instance.user:
            username = instance.matricule
            password = instance.name + instance.date_birthday.strftime("%Y")
            user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=instance.name,
                    last_name=instance.surname,
                    email= instance.email,
                    is_staff=True 
            )
            instance.user = user
            instance.save()
        
     