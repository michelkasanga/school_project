from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg', blank=True)
    
    class Meta:
        db_table = 'profiles'
        verbose_name='profile'
        
    def save(self, *args, **kwargs):
        #redimensionner la photo avant de sauvegarder
        if self.avatar:
            #ouvrir l'image
            img = Image.open(self.avatar)
            
            #redimensionner si necessaire 
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                
                #sauvegarde l'image redimensionné
                buffer = BytesIO()
                img.save(buffer, format = img.format if img.format else 'JPEG')
                self.avatar.save(
                    self.avatar.name,
                    ContentFile(buffer.getvalue()),
                    save=False
                )
        super().save(*args, **kwargs)