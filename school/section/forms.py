from django import forms
from .models import Section

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']
        labels = {
            'name': 'Nom de la section',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }