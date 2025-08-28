from django import forms
from .models import Role

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        labels = {
            'name': 'Nom du rôle',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }