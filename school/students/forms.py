from django import forms
from django.utils import timezone
from .models import Students


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'name', 
            'surname', 
            'first_name', 
            'classe'
            'section', 
            'option', 
            'date_of_birth', 
            'place_of_birth',
            'adress',
            'father_name',
            'mother_name',
            'garduan',
            'contact_garduan',
            'address_garduan',
            ]
        labels = {
            'name': 'Nom',
            'surname': 'Post-Nom',
            'first_name': 'Prenom',
            'classe': 'Classe',
            'section': 'Section',
            'option': 'Option',
            'date_of_birth': 'Date de naissance',
            'place_of_birth': 'Lieu de naissance',
            'adress': 'Adresse',
            'father_name': 'Nom du père',
            'mother_name': 'Nom de la mère',
            'garduan': 'Nom du tuteur',
            'contact_garduan': 'Contact du tuteur',
            'address_garduan': 'Adresse du tuteur',
            
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'option': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'garduan': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_garduan': forms.TextInput(attrs={'class': 'form-control'}),
            'address_garduan': forms.TextInput(attrs={'class': 'form-control'}),
            }
        
    def clean(self):
        cleaned_data = super().clean()
        section = cleaned_data.get('section')
        option = cleaned_data.get('option')
        
        if section and section.name.lower() in ['maternelle', 'primaire'] and option :
            raise forms.ValidationError(
                "les élèves en section primaire ou maternelle ne peuvent pas etre attribuer à une option"
            )    
        return cleaned_data
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > timezone.now().date():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")
        return date_of_birth
    
  