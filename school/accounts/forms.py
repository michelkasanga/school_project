from django import forms
from .models import Profiles
from django.utils.html import format_html

class ProfilesForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['avatar', 'bio']
        labels={
            'avatar':'',
            'bio':'Bio'
        }
        
        widgets = {
            'avatar':forms.ClearableFileInput(attrs={
                    'class':'form-control',
                    
                    
                    }),
            'bio':forms.Textarea(attrs={
                    'class':'form-control',
                    'placehold':'identifiez-vous dans 120 lettres'
                    
                    })
        }
        
        
class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'type':'text',
            'placeholder':'Nom d\'utilisateur', 
  
        }), 
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'type':'password',
            'placeholder':'Mot de passe',
            
        }),
         label= ""
    )