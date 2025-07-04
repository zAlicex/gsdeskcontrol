from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Estoque, Produto
from .forms import EstoqueForm, ProdutoForm
from django.db.models import Q
import json

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
