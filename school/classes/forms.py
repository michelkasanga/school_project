from django import forms
from .models import Classes, Tutors

class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ['name']
        labels = {'name': 'la classe'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de la classe'
            })
        }
        
class TutorsForm(forms.ModelForm):
    class Meta:
        model = Tutors
        fields = ['staff', 'classe', 'section', 'option']
        labels = {
            'staff': 'Titulaire',
            'classe': 'Classe',
            'section': 'Section',
            'option': 'Option (si applicable)'
        }
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'option': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        section = cleaned_data.get('section')
        option = cleaned_data.get('option')
        
        if section and section.name.lower() in ['maternelle', 'primaire'] and option:
            raise forms.ValidationError(
                "Le professeur ne peut pas avoir une option  à gerer s'il est en section primaire ou maternelle"
            )
        return cleaned_data