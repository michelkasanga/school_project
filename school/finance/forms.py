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
                'student':'Elève', 
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
            'month':forms.Select(attrs={'class':'form-control'}),
            'type_paiement':forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from students.models import Students
        self.fields['student'].queryset = Students.get_students_for_payment()
        # Filtrer les frais proposés selon l'élève sélectionné
        if 'student' in self.data:
            try:
                student_id = int(self.data.get('student'))
                from students.models import Students
                student = Students.objects.get(pk=student_id)
                self.fields['fees'].queryset = Fees.objects.filter(section=student.section, classe=student.classe)
            except (ValueError, Students.DoesNotExist):
                self.fields['fees'].queryset = Fees.objects.none()
        elif self.instance.pk and self.instance.student:
            student = self.instance.student
            self.fields['fees'].queryset = Fees.objects.filter(section=student.section, classe=student.classe)
        else:
            self.fields['fees'].queryset = Fees.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        fees = cleaned_data.get('fees')
        if student and fees:
            # Vérification classe
            if not fees.classe.filter(id=student.classe_id).exists():
                raise forms.ValidationError("La classe de l'élève ne correspond pas à celle du frais.")
            # Vérification section
            if fees.section_id != student.section_id:
                raise forms.ValidationError("La section de l'élève ne correspond pas à celle du frais.")
            # Vérification option si applicable
            if fees.options.exists():
                if student.option_id and not fees.options.filter(id=student.option_id).exists():
                    raise forms.ValidationError("L'option de l'élève ne correspond pas à celle du frais.")
        return cleaned_data



