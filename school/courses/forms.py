from django import forms
from .models import Courses

class CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['professor', 'course', 'classe', 'section', 'option']
        labels = {
            'professor': 'Professeur',
            'course': 'Cours',
            'classe': 'Classe',
            'section': 'Section',
            'option': 'Option',
        }
        widgets = {
            'professor': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'classe': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'option': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        section = cleaned_data.get('section')
        option = cleaned_data.get('option')
        
        if section and section.name.lower() in ['maternelle', 'primaire'] and option :
            raise forms.ValidationError(
                "pas d'option pour la section primaire ou maternelle"
            )    
        return cleaned_data