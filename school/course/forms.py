from django import forms
from .models import Course

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