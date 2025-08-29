from django import forms
from .models import Box

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['student', 'fees', 'amount_pay', 'type_paiement'],
        labels = ['Elève', 'Frais', 'Montant', 'Type de paiement']
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


