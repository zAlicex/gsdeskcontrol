from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Estoque, Produto, Licencas
from .forms import EstoqueForm, ProdutoForm, LicencaForm
from django.db.models import Q
import json
from clientes.models import ClienteProduto
from django.apps import apps
from django.core import serializers


def estoque(request):
    if request.method == 'POST':
        # Verifica se é uma edição ou novo registro
        estoque_id = request.POST.get('id')
        if estoque_id:
            # Edição
            estoque_item = get_object_or_404(Estoque, id=estoque_id)
            form = EstoqueForm(request.POST, instance=estoque_item)
        else:
            # Novo registro
            form = EstoqueForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('estoque:estoque')
        else:
            # Se houver erros, renderiza a página com os erros
            itens = Estoque.objects.all()
            context = {'form': form, 'itens': itens}
            return render(request, 'estoque/estoque.html', context)

    form = EstoqueForm()
    
    # Lógica de busca
    search_local = request.GET.get('search_local', '').strip()
    search_usuario = request.GET.get('search_usuario', '').strip()
    search_status = request.GET.get('search_status', '').strip()
    itens = Estoque.objects.all()

    if search_local:
        itens = itens.filter(local__nome__icontains=search_local)
    if search_usuario:
        itens = itens.filter(usuario__nome__icontains=search_usuario)
    if search_status:
        itens = itens.filter(status=search_status)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and (search_local or search_usuario or search_status):
        html = render_to_string(
            'estoque/partials/lista_estoque.html', {'itens': itens}
        )
        return JsonResponse({'html': html})

    context = {
        'form': form,
        'itens': itens,
        'search_local': search_local,
        'search_usuario': search_usuario,
        'search_status': search_status,
    }
    return render(request, 'estoque/estoque.html', context)

def get_item_details(request, item_id):
    item = get_object_or_404(Estoque, id=item_id)
    data = {
        'id': item.id,
        'nome_peca': item.nome_peca,
        'codigo': item.codigo,
        'modelo': item.modelo,
        'fornecedor': item.fornecedor,
        'data_entrada': item.data_entrada.strftime('%Y-%m-%d'),
        'descricao': item.descricao,
        'status': item.status,
        'status_display': item.get_status_display(),
    }
    return JsonResponse(data)

def edit_item(request, item_id):
    item = get_object_or_404(Estoque, id=item_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        form = EstoqueForm(data, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def delete_item(request, item_id):
    item = get_object_or_404(Estoque, id=item_id)
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def get_estoque(request, estoque_id):
    """Retorna os dados de um item do estoque para carregar no formulário"""
    try:
        estoque = get_object_or_404(Estoque, id=estoque_id)
        data = {
            'success': True,
            'estoque': {
                'id': estoque.id,
                'local_id': estoque.local.id if estoque.local else None,
                'local_nome': estoque.local.nome if estoque.local else '',
                'usuario_id': estoque.usuario.id if estoque.usuario else None,
                'usuario_nome': estoque.usuario.nome if estoque.usuario else '',
                'data_hora': estoque.data_hora.strftime('%Y-%m-%dT%H:%M') if estoque.data_hora else '',
                'status': estoque.status,
                'status_display': estoque.get_status_display(),
            }
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def atualizar_estoque(request, estoque_id):
    """Atualiza um item do estoque"""
    if request.method == 'POST':
        try:
            estoque = get_object_or_404(Estoque, id=estoque_id)
            form = EstoqueForm(request.POST, instance=estoque)
            if form.is_valid():
                form.save()
                return redirect('estoque:estoque')
            else:
                # Se houver erros, renderiza a página com os erros
                context = {
                    'form': form,
                    'itens': Estoque.objects.all(),
                    'search_local': request.GET.get('search_local', ''),
                    'search_usuario': request.GET.get('search_usuario', ''),
                    'search_status': request.GET.get('search_status', '')
                }
                return render(request, 'estoque/estoque.html', context)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return redirect('estoque:estoque')

def produto_list(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/produto_list.html', {'produtos': produtos})

def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estoque:produto_list')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/produto_form.html', {'form': form})

def licencas_list(request):
    """Lista todas as licenças"""
    licencas = Licencas.objects.all().select_related('produto')
    return render(request, 'estoque/licencas_list.html', {'licencas': licencas})

def licencas_create(request):
    """Cria uma nova licença"""
    # Verifica se veio um produto pré-selecionado
    produto_id = request.GET.get('produto')
    initial_data = {}
    
    if produto_id:
        try:
            produto = Produto.objects.get(id=produto_id)
            initial_data['produto'] = produto
        except Produto.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = LicencaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estoque:licencas_list')
    else:
        form = LicencaForm(initial=initial_data)
    
    return render(request, 'estoque/licencas_form.html', {'form': form})

def licencas_resumo(request):
    """Mostra o resumo de licenças por produto"""
    produtos = Produto.objects.all().prefetch_related('licencas')
    licencas = Licencas.objects.all()
    
    # Cálculos para estatísticas
    total_produtos = produtos.count()
    total_licencas = licencas.count()

    # Calcular licenças disponíveis por produto
    produtos_info = []
    total_licencas_disponiveis = 0
    for produto in produtos:
        total_licencas_registradas = sum(l.quantidade for l in produto.licencas.all())
        total_usos_clientes = sum(rel.quantidade for rel in ClienteProduto.objects.filter(produto=produto))
        licencas_disponiveis = total_licencas_registradas - total_usos_clientes
        if licencas_disponiveis is not None:
            total_licencas_disponiveis += licencas_disponiveis
        produtos_info.append({
            'produto': produto,
            'licencas_registradas': total_licencas_registradas,
            'usos_clientes': total_usos_clientes,
            'licencas_disponiveis': licencas_disponiveis,
        })

    context = {
        'produtos_info': produtos_info,
        'produtos': produtos,
        'licencas': licencas,
        'total_produtos': total_produtos,
        'total_licencas': total_licencas,
        'total_licencas_disponiveis': total_licencas_disponiveis,
    }
    
    return render(request, 'estoque/licencas_resumo.html', context)

def conjunt_json(request):
    """
    Endpoint JSON que retorna todas as informações do conjunt.
    """
    itens = Estoque.objects.all()
    
    data = []
    for item in itens:
        item_data = {
            'id': item.id,
            'local_id': item.local.id if item.local else None,
            'local_nome': item.local.nome if item.local else '',
            'usuario_id': item.usuario.id if item.usuario else None,
            'usuario_nome': item.usuario.nome if item.usuario else '',
            'data_hora': item.data_hora.strftime('%Y-%m-%d %H:%M') if item.data_hora else None,
            'status': item.status,
            'status_display': item.get_status_display(),
        }
        data.append(item_data)
    
    return JsonResponse({
        'success': True,
        'total_conjunt': len(data),
        'estoque': data
    }, safe=False)

def produtos_json(request):
    """
    Endpoint JSON que retorna todas as informações dos produtos.
    """
    produtos = Produto.objects.all()
    
    data = []
    for produto in produtos:
        produto_data = {
            'id': produto.id,
            'nome': produto.nome,
            'quantidade': produto.quantidade,
            'status': 'disponivel' if produto.quantidade and produto.quantidade > 0 else 'esgotado' if produto.quantidade == 0 else 'indefinido'
        }
        data.append(produto_data)
    
    return JsonResponse({
        'success': True,
        'total_produtos': len(data),
        'produtos': data
    }, safe=False)

def licencas_json(request):
    """
    Endpoint JSON que retorna todas as informações das licenças.
    """
    licencas = Licencas.objects.all().select_related('produto')
    
    data = []
    for licenca in licencas:
        licenca_data = {
            'id': licenca.id,
            'produto': {
                'id': licenca.produto.id,
                'nome': licenca.produto.nome,
            },
            'quantidade': licenca.quantidade,
            'valor': float(licenca.valor),
            'data_registro': licenca.data_registro.strftime('%Y-%m-%d %H:%M:%S'),
        }
        data.append(licenca_data)
    
    return JsonResponse({
        'success': True,
        'total_licencas': len(data),
        'licencas': data
    }, safe=False)

def all_models_json(request):
    """Endpoint que retorna todas as informações de todos os models do projeto em um único JSON."""
    # Lista de modelos do sistema Django que devem ser excluídos
    EXCLUDE_MODELS = [
        "admin.logentry",
        "auth.permission",
        "auth.group", 
        "auth.user",
        "contenttypes.contenttype",
        "sessions.session",
    ]
    
    app_labels = [app.label for app in apps.get_app_configs() if app.models_module]
    all_data = {}
    for app_label in app_labels:
        app_models = apps.get_app_config(app_label).get_models()
        for model in app_models:
            model_name = model.__name__
            model_key = f"{app_label}.{model_name.lower()}"
            
            # Pula os modelos do sistema Django
            if model_key in EXCLUDE_MODELS:
                continue
                
            queryset = model.objects.all()
            # Serializa para dicionário (não para string JSON)
            data = serializers.serialize('python', queryset)
            # Remove o wrapper do Django serializer
            data = [obj['fields'] | {'id': obj['pk']} for obj in data]
            all_data[f"{app_label}.{model_name}"] = data
    return JsonResponse(all_data, safe=False)
