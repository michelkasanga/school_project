from django import forms
from .models import Students
from classes.models import Classes
from options.models import Options
from section.models import Section

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name','surname', 'fisrt_name','classe','section', 'option', 'date_birthday', 'place_birthday' ]
        labels = ['Nom','Post-Nom', 'Prenom','classe','section', 'option', 'date de naissance', 'Lieu de naissance' ]
        widgets = {
            'classe' : forms.RadioSelect(),
            'section': forms.RadioSelect(),
            'option' : forms.RadioSelect()
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