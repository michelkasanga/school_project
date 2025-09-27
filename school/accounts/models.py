from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.html import format_html

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, max_length= 120)
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
        
        def avatar_preview(self, obj):
            if obj.avatar:
             return format_html('<img src="{}" width="30" height="30" style="object-fit: cover; border-radius: 50%;" />', obj.avatar.url)
            return "-"
        avatar_preview.short_description = 'avatar'