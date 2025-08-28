from django import forms
from .models import Fees

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
    
    def clean(self):
        cleaned_data = super().clean()
        section = cleaned_data.get('section')
        options = cleaned_data.get('options')
        
        if section and section.name.lower() in ['maternelle', 'primaire'] and options.exists():
            raise forms.ValidationError(
                "Pas d'options pour la section primaire ou maternelle"
            )    
        return cleaned_data