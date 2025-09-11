from django import forms
from .models import Program, Testimonial, About, Actuality

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
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'credit','level',  'duration', 'condition','description', 'image']
        labels = {
            'title': 'Titre du programme',
            'credit' : 'Credit',
            'duration' : 'Durée', 
            'description': 'Description',  
           'level':'Niveau',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['description', 'mission', 'values', 'vision','image','image_2', 'team']
        labels = {
            'description': 'Description',
            'mission':'La mission'  ,
            'values':'Nos valeur' ,
            'vision':'Notre vision'   
        }
      

class ActualityForm(forms.ModelForm):
    class Meta:
        model = Actuality
        fields = ['title', 'facilitator','date','place', 'end','category','description','description', 'image']
        labels = {
            'title': 'Titre d\'Evenement',
            'facilitator' : 'Moderateur', 
            'description': 'Description', 
            'end':'heure de cloture' 
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'facilitator': forms.Select(attrs={'class': 'form-control'}),
        }