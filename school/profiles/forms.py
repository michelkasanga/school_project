from django import forms
from .models import Profiles

class ProfilesForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['avatar']