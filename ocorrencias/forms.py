from django import forms
from .models import Ocorrencia

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ['local', 'data_hora', 'status', 'observacoes', 'imagem']
        widgets = {
            'local': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'status': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'observacoes': forms.Textarea(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500', 'rows': 3, 'placeholder': 'Observações da ocorrência'}),
            'imagem': forms.FileInput(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500', 'accept': 'image/*'}),
        } 