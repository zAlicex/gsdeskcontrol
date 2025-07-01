from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Clientes
from .forms import ClientesForm
import json

@login_required
def clientes_view(request):
    """
    Renderiza a página de clientes e lida com a criação de novos clientes.
    """
    if request.method == 'POST':
        # Lidar com o salvamento de novos clientes
        cliente_id = request.POST.get('id')
        
        if cliente_id:
            # Atualizar cliente existente
            cliente = get_object_or_404(Clientes, id=cliente_id)
            form = ClientesForm(request.POST, instance=cliente)
            action = 'atualizado'
        else:
            # Criar novo cliente
            form = ClientesForm(request.POST)
            action = 'criado'
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {action} com sucesso!')
        else:
            messages.error(request, 'Erro ao salvar cliente. Verifique os dados.')
        
        return redirect('clientes:clientes')
    
    # Busca
    search_name = request.GET.get('search_name', '')
    
    # Query base
    clientes = Clientes.objects.all().order_by('-id')
    
    # Aplicar filtros de busca
    if search_name:
        clientes = clientes.filter(
            Q(nome__icontains=search_name) 
        )
    
    # Se for uma requisição AJAX, retorna apenas a lista
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'clientes/partials/lista_clientes.html', {
            'clientes': clientes
        })
    
    context = {
        'clientes': clientes,
        'search_name': search_name,
        'active_tab': 'clientes',
    }
    
    return render(request, 'clientes/clientes.html', context)

@login_required
def carregar_mais_clientes(request):
    """View para carregar mais clientes via AJAX (scroll infinito)"""
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))
    search_name = request.GET.get('search_name', '')
    
    clientes = Clientes.objects.all().order_by('-id')
    
    # Aplicar filtros
    if search_name:
        clientes = clientes.filter(
            Q(nome__icontains=search_name) 
        )
    
    # Aplicar offset e limit
    clientes_paginados = clientes[offset:offset + limit]
    
    # Renderizar apenas os itens da lista
    html = render(request, 'clientes/partials/lista_clientes_items.html', {
        'clientes': clientes_paginados
    }).content.decode('utf-8')
    
    return JsonResponse({
        'html': html,
        'has_more': len(clientes_paginados) == limit,
        'total_count': clientes.count()
    })

@login_required
def salvar_cliente(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('id')
        
        if cliente_id:
            # Atualizar cliente existente
            cliente = get_object_or_404(Clientes, id=cliente_id)
            form = ClientesForm(request.POST, instance=cliente)
            action = 'atualizado'
        else:
            # Criar novo cliente
            form = ClientesForm(request.POST)
            action = 'criado'
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente {action} com sucesso!')
        else:
            messages.error(request, 'Erro ao salvar cliente. Verifique os dados.')
    
    return redirect('clientes:clientes')

@login_required
def get_cliente(request, cliente_id):
    """
    Retorna os dados de um cliente específico em formato JSON para o formulário.
    """
    try:
        cliente = get_object_or_404(Clientes, id=cliente_id)
        data = {
            'id': cliente.id,
            'nome': cliente.nome or '',
        }
        return JsonResponse({'success': True, 'cliente': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def atualizar_cliente(request, cliente_id):
    """
    Atualiza um cliente existente a partir de dados POST.
    """
    if request.method == 'POST':
        cliente = get_object_or_404(Clientes, id=cliente_id)
        form = ClientesForm(request.POST, instance=cliente)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
        else:
            messages.error(request, 'Erro ao atualizar cliente.')
    
    return redirect('clientes:clientes')

@login_required
def locais_api(request):
    """
    API que retorna todos os locais (Clientes) em JSON.
    """
    locais = Clientes.objects.all().values('id', 'nome')
    return JsonResponse(list(locais), safe=False)