from django import forms
from .models import Orpecas

class OrpecasForm(forms.ModelForm):
    class Meta:
        model = Orpecas
        fields = ['local', 'diagnostico', 'botao_panico', 'sensor']
        widgets = {
            'local': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'diagnostico': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'botao_panico': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'sensor': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
        } 