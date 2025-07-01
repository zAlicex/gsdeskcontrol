from django import forms
from .models import Rat

class RatForm(forms.ModelForm):
    class Meta:
        model = Rat
        fields = ['local', 'nome', 'cpf'] 