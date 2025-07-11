from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.http import JsonResponse
from .models import Clientes, ClienteProntaResposta, ClienteTelefone
from .forms import ClientesForm
import json
from estoque.models import Produto
from django.template.loader import render_to_string
from .models import Clientes, ClienteProduto
from django.views.decorators.csrf import csrf_exempt

from estoque.models import Produto

def clientes_view(request):
    ...
    produtos = Produto.objects.all()
    return render(request, 'clientes/clientes.html', {
        'form': form,
        'clientes': clientes,
        'cliente_id': cliente_id or '',
        'produtos': produtos,  # 👈 isso aqui!
    })


@login_required
def clientes_view(request):
    cliente_id = request.GET.get('id')
    if request.method == 'POST':
        cliente_id = request.POST.get('id')
        if cliente_id:
            cliente = get_object_or_404(Clientes, id=cliente_id)
            form = ClientesForm(request.POST, instance=cliente)
        else:
            form = ClientesForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            # Processa múltiplos produtos
            produtos = request.POST.getlist('produtos')
            quantidades = request.POST.getlist('quantidades')
            # Remove produtos antigos
            cliente.produtos_relacionados.all().delete()
            # Adiciona os novos
            for prod_id, qtd in zip(produtos, quantidades):
                if prod_id and qtd:
                    ClienteProduto.objects.create(
                        cliente=cliente,
                        produto_id=prod_id,
                        quantidade=qtd
                    )
            # --- NOVO: Processa prontas respostas e telefones ---
            # Remove antigos
            cliente.prontas_respostas.all().delete()
            cliente.telefones.all().delete()
            # Prontas respostas
            prontas_respostas = request.POST.getlist('prontas_respostas_json')
            for ordem, pr in enumerate(prontas_respostas):
                if pr:
                    ClienteProntaResposta.objects.create(
                        cliente=cliente,
                        pronta_resposta=pr,
                        ordem=ordem
                    )
            # Telefones
            telefones = request.POST.getlist('telefones_json')
            for ordem, tel_json in enumerate(telefones):
                try:
                    tel = json.loads(tel_json)
                    if tel.get('telefone'):
                        ClienteTelefone.objects.create(
                            cliente=cliente,
                            telefone=tel['telefone'],
                            tipo=tel.get('tipo', ''),
                            ordem=ordem
                        )
                except Exception:
                    continue
            return redirect('clientes:locais')
    else:
        if cliente_id:
            cliente = get_object_or_404(Clientes, id=cliente_id)
            form = ClientesForm(instance=cliente)
        else:
            form = ClientesForm()
    clientes = Clientes.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'clientes/clientes.html', {
        'form': form,
        'clientes': clientes,
        'cliente_id': cliente_id or '',
        'produtos': produtos,
    })

@login_required
def adicionar_pronta_resposta(request, cliente_id):
    """Adiciona uma nova pronta resposta ao cliente"""
    if request.method == 'POST':
        cliente = get_object_or_404(Clientes, id=cliente_id)
        pronta_resposta = request.POST.get('pronta_resposta')
        
        if pronta_resposta:
            # Encontrar a próxima ordem
            ultima_ordem = ClienteProntaResposta.objects.filter(cliente=cliente).aggregate(
                Max('ordem')
            )['ordem__max'] or 0
            
            ClienteProntaResposta.objects.create(
                cliente=cliente,
                pronta_resposta=pronta_resposta,
                ordem=ultima_ordem + 1
            )
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def adicionar_telefone(request, cliente_id):
    """Adiciona um novo telefone ao cliente"""
    if request.method == 'POST':
        cliente = get_object_or_404(Clientes, id=cliente_id)
        telefone = request.POST.get('telefone')
        tipo = request.POST.get('tipo', '')
        
        if telefone:
            # Encontrar a próxima ordem
            ultima_ordem = ClienteTelefone.objects.filter(cliente=cliente).aggregate(
                Max('ordem')
            )['ordem__max'] or 0
            
            ClienteTelefone.objects.create(
                cliente=cliente,
                telefone=telefone,
                tipo=tipo,
                ordem=ultima_ordem + 1
            )
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def remover_pronta_resposta(request, cliente_id, pronta_resposta_id):
    """Remove uma pronta resposta do cliente"""
    if request.method == 'POST':
        pronta_resposta = get_object_or_404(ClienteProntaResposta, id=pronta_resposta_id, cliente_id=cliente_id)
        pronta_resposta.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@login_required
def remover_telefone(request, cliente_id, telefone_id):
    """Remove um telefone do cliente"""
    if request.method == 'POST':
        telefone = get_object_or_404(ClienteTelefone, id=telefone_id, cliente_id=cliente_id)
        telefone.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

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
    cliente = get_object_or_404(Clientes, id=cliente_id)
    produtos = [
        {
            'produto': rel.produto.nome,
            'produto_id': rel.produto.id,
            'quantidade': rel.quantidade
        }
        for rel in cliente.produtos_relacionados.all()
    ]
    
    # Buscar prontas respostas e telefones
    prontas_respostas = [
        {
            'id': pr.id,
            'pronta_resposta': pr.pronta_resposta,
            'ordem': pr.ordem
        }
        for pr in cliente.prontas_respostas.all()
    ]
    
    telefones = [
        {
            'id': tel.id,
            'telefone': tel.telefone,
            'tipo': tel.tipo,
            'ordem': tel.ordem
        }
        for tel in cliente.telefones.all()
    ]
    
    data = {
        'id': cliente.id,
        'nome': cliente.nome,
        'pronta_resposta': cliente.pronta_resposta,
        'telefone': cliente.telefone,
        'produtos': produtos,
        'prontas_respostas': prontas_respostas,
        'telefones': telefones,
    }
    return JsonResponse({'success': True, 'cliente': data})


@login_required
def locais_api(request):
    """
    API que retorna todos os locais (Clientes) em JSON.
    """
    locais = Clientes.objects.all().values('id', 'nome')
    return JsonResponse(list(locais), safe=False)

@login_required
def locais_json(request):
    """
    Endpoint JSON que retorna todas as informações dos clientes.
    """
    clientes = Clientes.objects.all()
    
    data = []
    for cliente in clientes:
        # Buscar produtos relacionados
        produtos_relacionados = []
        for rel in cliente.produtos_relacionados.all():
            produtos_relacionados.append({
                'produto_id': rel.produto.id,
                'produto_nome': rel.produto.nome,
                'quantidade': rel.quantidade
            })
        
        # Buscar prontas respostas e telefones
        prontas_respostas = [
            {
                'id': pr.id,
                'pronta_resposta': pr.pronta_resposta,
                'ordem': pr.ordem
            }
            for pr in cliente.prontas_respostas.all()
        ]
        
        telefones = [
            {
                'id': tel.id,
                'telefone': tel.telefone,
                'tipo': tel.tipo,
                'ordem': tel.ordem
            }
            for tel in cliente.telefones.all()
        ]
        
        cliente_data = {
            'id': cliente.id,
            'nome': cliente.nome,
            'pronta_resposta': cliente.pronta_resposta,
            'telefone': cliente.telefone,
            'total_produtos': cliente.total_produtos,
            'produtos_relacionados': produtos_relacionados,
            'prontas_respostas': prontas_respostas,
            'telefones': telefones,
        }
        data.append(cliente_data)
    
    return JsonResponse({
        'success': True,
        'total_locais': len(data),
        'clientes': data
    }, safe=False)

def lista_clientes_partial(request):
    from .models import Clientes
    clientes = Clientes.objects.all()
    html = render_to_string('clientes/partials/lista_clientes.html', {'clientes': clientes})
    return JsonResponse({'html': html})

@login_required
@csrf_exempt
def adicionar_pronta_telefone(request, cliente_id):
    if request.method == 'POST':
        cliente = get_object_or_404(Clientes, id=cliente_id)
        pronta_resposta = request.POST.get('pronta_resposta')
        telefone = request.POST.get('telefone')
        tipo = request.POST.get('tipo', '')

        # Adiciona pronta resposta se preenchido
        if pronta_resposta:
            ultima_ordem = ClienteProntaResposta.objects.filter(cliente=cliente).aggregate(
                Max('ordem')
            )['ordem__max'] or 0
            ClienteProntaResposta.objects.create(
                cliente=cliente,
                pronta_resposta=pronta_resposta,
                ordem=ultima_ordem + 1
            )
        # Adiciona telefone se preenchido
        if telefone:
            ultima_ordem = ClienteTelefone.objects.filter(cliente=cliente).aggregate(
                Max('ordem')
            )['ordem__max'] or 0
            ClienteTelefone.objects.create(
                cliente=cliente,
                telefone=telefone,
                tipo=tipo,
                ordem=ultima_ordem + 1
            )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método não permitido'})