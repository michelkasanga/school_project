from django import forms
from .models import Options

class OptionsForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ['name']
        labels = {
            'name': 'Nom de l\'option',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }