from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Rat, Clientes
from .forms import RatForm
from django.core import serializers
import json

class RatView(View):
    def get(self, request):
        search_name = request.GET.get('search_name')
        rats = Rat.objects.all()
        if search_name:
            rats = rats.filter(nome__icontains=search_name)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                'rat/partials/lista_rats.html',
                {'rats': rats}
            )
            return JsonResponse({'html': html})
        form = RatForm()
        clientes = Clientes.objects.all()
        context = {
            'rats': rats,
            'form': form,
            'clientes': clientes,
            'search_name': search_name or '',
        }
        return render(request, 'rat/rat.html', context)

    def post(self, request):
        form = RatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rat:rat')
        rats = Rat.objects.all()
        clientes = Clientes.objects.all()
        context = {
            'rats': rats,
            'form': form,
            'clientes': clientes,
        }
        return render(request, 'rat/rat.html', context)

def get_rat(request, rat_id):
    try:
        rat = get_object_or_404(Rat, id=rat_id)
        rat_data = {
            'success': True,
            'rat': {
                'id': rat.id,
                'local_id': rat.local.id if rat.local else None,
                'local_nome': rat.local.nome if rat.local else '',
                'nome': rat.nome,
                'cpf': rat.cpf,
            }
        }
        return JsonResponse(rat_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def atualizar_rat(request, rat_id):
    rat = get_object_or_404(Rat, id=rat_id)
    if request.method == 'POST':
        form = RatForm(request.POST, instance=rat)
        if form.is_valid():
            form.save()
            return redirect('rat:rat')
    return redirect('rat:rat')

def excluir_rat(request, rat_id):
    rat = get_object_or_404(Rat, id=rat_id)
    if request.method == 'POST':
        rat.delete()
        return redirect('rat:rat')
    return redirect('rat:rat')

def get_cliente_data(request, cliente_id):
    try:
        cliente = get_object_or_404(Clientes, id=cliente_id)
        cliente_data = {
            'success': True,
            'cliente': {
                'nome': cliente.nome,
                'telefone': cliente.telefone,
                'celular': cliente.celular,
                'email': cliente.email,
                'endereco': cliente.endereco,
                'bairro': cliente.bairro,
                'cidade': cliente.cidade,
                'cep': cliente.cep,
                'cpf_cnpj': cliente.cpf_cnpj,
            }
        }
        return JsonResponse(cliente_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
