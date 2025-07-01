from django import forms
from .models import Clientes

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
        } 