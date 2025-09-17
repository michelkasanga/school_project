from django import forms
from django.utils import timezone
from .models import Staff, Role, Dean


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

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'surname', 'firstname','sexe', 'email', 'contact', 'title', 'role', 'degree', 'faculty', 'date_birthday', 'admin']
        labels = {
            'name': 'Nom',
            'surname': 'Post-Nom',
            'firstname': 'Prenom',
            'sexe': 'Sexe',
            'title':'Titre',
            'role': 'Rôle',
            'degree': 'Niveau d\'étude',
            'faculty': 'Domaine d\'étude',
            'date_birth': 'Date de naissance',
            'admin':'Fait parti de l\'administration'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.RadioSelect(attrs={'class': 'form-control'}),
            'role': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'admin': forms.CheckboxInput(attrs={'class': 'form-control'}),
    
        
        }
        
    def clean(self):
        cleaned_data = super().clean()
        date_birthday = cleaned_data.get('date_birthday')
        
        if date_birthday and date_birthday > timezone.now().date():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")
        
        return cleaned_data
    
class DeanForm(forms.ModelForm):
    
    class Meta:
        model = Dean
        fields = [
            'staff', 'section', 'option', 'course', 'start_date', 'end_date'
        ]
        
        labels = {
            'staff':'Titulaire d\'option', 
            'course':'Cours d\'option'
        }
        
        widgets = {
          'course': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
           
        }
