from django import forms
from .models import Program, Testimonial, About, Service, Actuality

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['fullname', 'role', 'content', 'image']
        labels = {
            'fullname': 'Nom complet',
            'role' : 'Role',
            'content' : 'Temoignage'
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'credit', 'duration','description', 'image']
        labels = {
            'title': 'Titre du programme',
            'credit' : 'Credit',
            'duration' : 'Durée', 
            'description': 'Description',  
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['description', 'image']
        labels = {
            'description': 'Description',  
        }
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control'})
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name','description', 'image']
        labels = {
            'name': 'Nom du service',
            'description': 'Description',  
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }


class ActualityForm(forms.ModelForm):
    class Meta:
        model = Actuality
        fields = ['title', 'facilitator','description', 'image']
        labels = {
            'title': 'Titre d\'actualité',
            'facilitator' : 'Moderateur', 
            'description': 'Description',  
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'facilitator': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }