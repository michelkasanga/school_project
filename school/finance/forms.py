from django import forms
from .models import *


class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['name', 'amount', 'classe', 'section', 'options']
        labels = {
            'name': 'Nom du frais',
            'amount': 'Montant',
            'classe': 'Classe',
            'section': 'Section',
            'options': 'Options',
            
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'classe': forms.CheckboxSelectMultiple(),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'options': forms.CheckboxSelectMultiple(),
        }
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Le montant doit être un nombre positif.")
        return amount
    
        
    def clean_classe_replance(self):
        classe = self.cleaned_data.get('classe')
        if classe:
            classe = classe.replace(" ", "")
        return classe
    
    def clean(self):
        cleaned_data = super().clean()
        section = cleaned_data.get('section')
        options = cleaned_data.get('options')
        classe = cleaned_data.get('classe')
        
        if section and section.name.lower() in ['maternelle', 'primaire'] and options:
            raise forms.ValidationError(
                "Pas d'options pour la section primaire ou maternelle"
            )   
        if classe in  ["7ème", "8ème", "7eme", "8eme"]  and options:
               raise forms.ValidationError(
                "les élèves en éducation de base(7eme et 8eme) ne peuvent pas avoir d'option " ) 
        
        return cleaned_data
    
    

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['student', 'fees', 'month','amount_pay', 'type_paiement']
        labels = {
                'students':'Elève', 
                'fees':'Frais', 
                'month':'Mois',
                'amount_pay':'Montant', 
                'type_paiement':'Type de paiement',
                'collector':'Collecteur',
                'paid_date':'Date de paimment',
                'updated_at':'Modification'
                }
        widgets = {
            'student':forms.Select(attrs={'class':'form-control'}),
            'fees':forms.Select(attrs={'class':'form-control'}),
            'amount_pay':forms.NumberInput(attrs={
                'class':'form-control',
                'step':'0.01',
                'placeholder':'Montant en Franc congolais'
                }),
            'type_paiement':forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclure les élèves exempter du champ student
        from students.models import Students
        self.fields['student'].queryset = Students.get_students_for_payment()



