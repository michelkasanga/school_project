from django import forms
from .models import Program, Testimonial, About, Service, Actuality

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'credit', 'duration', 'description', 'image']
        labels = {
            'title': 'Title',
            'credit': 'Credit',
            'duration': 'Durée',
            'description': 'Description',
            'image': 'Image',
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'content',  'image']
        labels = {
            'name': 'Nom complet',
            'role': 'Role',
            'content': 'Temoignage',
            'image': 'Image',
        }
        widgets = {
            'role': forms.RadioSelect(attrs={'class': 'form-control'}),
           
        }


class ActualityForm(forms.ModelForm):
    class Meta:
        model = Actuality
        fields = ['title', 'facilitator', 'content',  'image']
        labels = {
            'title': 'Actualité',
            'facilitator': 'Animateur(trice)',
            'content': 'Breve explication',
            'image': 'Image',
        }
        widgets = {
            'facilitator': forms.Select(attrs={'class': 'form-control'}),
           
        }

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = [ 'content',  'image']
        labels = {
            'content': 'A propo de nous',
            'image': 'Image',
        }
        

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description',  'image']
        labels = {
            'name':'Le service',
            'description': 'Desciption du Service',
            'image': 'Image',
        }
