from django import forms
from .models import Orcamento

class OrcamentoForm(forms.ModelForm):
    data_acionamento = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
    )
    
    data_chegada = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
    )
    
    class Meta:
        model = Orcamento
        fields = ['nome_local', 'nome_usuarios', 'data_acionamento', 'data_chegada', 'sla_resposta']
        widgets = {
            'nome_local': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'nome_usuarios': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'sla_resposta': forms.NumberInput(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500', 'readonly': 'readonly'}),
        } 