from django import forms
from .models import *

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
        
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']  # Removed 'section' field
        labels = {
            'name': 'Nom du cours',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'section': forms.Select(attrs={'class': 'form-control'}),  # Removed widget for 'section'
        }


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
    
