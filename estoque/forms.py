from django import forms
from .models import Estoque, Produto, Licencas

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['local', 'usuario', 'data_hora', 'status']
        widgets = {
            'local': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'usuario': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
            'status': forms.Select(attrs={'class': 'w-full py-1 bg-transparent border-0 border-b-2 border-gray-300 focus:outline-none focus:ring-0 focus:border-blue-500'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'quantidade': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'min': '0', 'placeholder': 'Quantidade disponível'}),
        }

class LicencaForm(forms.ModelForm):
    class Meta:
        model = Licencas
        fields = ['produto', 'quantidade', 'valor']
        widgets = {
            'produto': forms.Select(attrs={'class': 'input input-bordered w-full'}),
            'quantidade': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'min': '1', 'placeholder': 'Quantidade de licenças'}),
            'valor': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'min': '0', 'step': '0.01', 'placeholder': 'Valor da licença'}),
        } 