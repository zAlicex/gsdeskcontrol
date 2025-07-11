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
        itens = itens.filter(local_nome_icontains=search_local)
    if search_usuario:
        itens = itens.filter(usuario_nome_icontains=search_usuario)
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
            model_name = model._name_
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

def clientes_json(request):
    """Endpoint JSON que retorna todas as informações dos clientes."""
    from clientes.models import Clientes, ClienteProduto
    
    clientes = Clientes.objects.all()
    cliente_produtos = ClienteProduto.objects.all().select_related('cliente', 'produto')
    
    clientes_data = []
    for cliente in clientes:
        cliente_data = {
            'id': cliente.id,
            'nome': cliente.nome,
            'pronta_resposta': cliente.pronta_resposta,
            'telefone': cliente.telefone,
        }
        clientes_data.append(cliente_data)
    
    cliente_produtos_data = []
    for cp in cliente_produtos:
        cp_data = {
            'id': cp.id,
            'cliente_id': cp.cliente.id,
            'cliente_nome': cp.cliente.nome,
            'produto_id': cp.produto.id,
            'produto_nome': cp.produto.nome,
            'quantidade': cp.quantidade,
        }
        cliente_produtos_data.append(cp_data)
    
    return JsonResponse({
        'success': True,
        'total_clientes': len(clientes_data),
        'total_cliente_produtos': len(cliente_produtos_data),
        'clientes': clientes_data,
        'cliente_produtos': cliente_produtos_data,
    }, safe=False)

def orcamentos_json(request):
    """Endpoint JSON que retorna todas as informações dos orçamentos."""
    from orcamento.models import Orcamento
    
    orcamentos = Orcamento.objects.all().select_related('nome_local', 'nome_usuarios')
    
    orcamentos_data = []
    for orcamento in orcamentos:
        orcamento_data = {
            'id': orcamento.id,
            'nome_local_id': orcamento.nome_local.id if orcamento.nome_local else None,
            'nome_local_nome': orcamento.nome_local.nome if orcamento.nome_local else '',
            'nome_usuarios_id': orcamento.nome_usuarios.id if orcamento.nome_usuarios else None,
            'nome_usuarios_nome': orcamento.nome_usuarios.nome if orcamento.nome_usuarios else '',
            'data_acionamento': orcamento.data_acionamento.strftime('%Y-%m-%d %H:%M:%S') if orcamento.data_acionamento else None,
            'data_chegada': orcamento.data_chegada.strftime('%Y-%m-%d %H:%M:%S') if orcamento.data_chegada else None,
            'sla_resposta': str(orcamento.sla_resposta) if orcamento.sla_resposta else None,
            'imagem': orcamento.imagem.url if orcamento.imagem else None,
        }
        orcamentos_data.append(orcamento_data)
    
    return JsonResponse({
        'success': True,
        'total_orcamentos': len(orcamentos_data),
        'orcamentos': orcamentos_data,
    }, safe=False)

def orpecas_json(request):
    """Endpoint JSON que retorna todas as informações dos orçamentos de peças."""
    from orpecas.models import Orpecas
    
    orpecas = Orpecas.objects.all().select_related('local')
    
    orpecas_data = []
    for orpeca in orpecas:
        orpeca_data = {
            'id': orpeca.id,
            'local_id': orpeca.local.id if orpeca.local else None,
            'local_nome': orpeca.local.nome if orpeca.local else '',
            'diagnostico': orpeca.diagnostico,
            'botao_panico': orpeca.botao_panico,
            'sensor': orpeca.sensor,
            'imagem': orpeca.imagem.url if orpeca.imagem else None,
        }
        orpecas_data.append(orpeca_data)
    
    return JsonResponse({
        'success': True,
        'total_orpecas': len(orpecas_data),
        'orpecas': orpecas_data,
    }, safe=False)

def ocorrencias_json(request):
    """Endpoint JSON que retorna todas as informações das ocorrências."""
    from ocorrencias.models import Ocorrencia
    
    ocorrencias = Ocorrencia.objects.all().select_related('local')
    
    ocorrencias_data = []
    for ocorrencia in ocorrencias:
        ocorrencia_data = {
            'id': ocorrencia.id,
            'local_id': ocorrencia.local.id if ocorrencia.local else None,
            'local_nome': ocorrencia.local.nome if ocorrencia.local else '',
            'data_hora': ocorrencia.data_hora.strftime('%Y-%m-%d %H:%M:%S') if ocorrencia.data_hora else None,
            'status': ocorrencia.status,
            'status_display': ocorrencia.get_status_display(),
            'observacoes': ocorrencia.observacoes,
            'imagem': ocorrencia.imagem.url if ocorrencia.imagem else None,
        }
        ocorrencias_data.append(ocorrencia_data)
    
    return JsonResponse({
        'success': True,
        'total_ocorrencias': len(ocorrencias_data),
        'ocorrencias': ocorrencias_data,
    }, safe=False)

def rat_json(request):
    """Endpoint JSON que retorna todas as informações dos RATs."""
    from rat.models import Rat
    
    rats = Rat.objects.all().select_related('local')
    
    rats_data = []
    for rat in rats:
        rat_data = {
            'id': rat.id,
            'local_id': rat.local.id if rat.local else None,
            'local_nome': rat.local.nome if rat.local else '',
            'nome': rat.nome,
            'cpf': rat.cpf,
            'tipo_servico': rat.tipo_servico,
            'status': rat.status,
            'status_display': rat.get_status_display(),
        }
        rats_data.append(rat_data)
    
    return JsonResponse({
        'success': True,
        'total_rats': len(rats_data),
        'rats': rats_data,
    }, safe=False)

def agenda_json(request):
    """Endpoint JSON que retorna todas as informações da agenda."""
    from agenda.models import AgendaDia, Visita
    
    agenda_dias = AgendaDia.objects.all()
    visitas = Visita.objects.all().select_related('agenda')
    
    agenda_dias_data = []
    for dia in agenda_dias:
        dia_data = {
            'id': dia.id,
            'data': dia.data.strftime('%Y-%m-%d'),
            'dia_semana': dia.dia_semana,
        }
        agenda_dias_data.append(dia_data)
    
    visitas_data = []
    for visita in visitas:
        visita_data = {
            'id': visita.id,
            'agenda_id': visita.agenda.id if visita.agenda else None,
            'agenda_data': visita.agenda.data.strftime('%Y-%m-%d') if visita.agenda else None,
            'horario': visita.horario.strftime('%H:%M') if visita.horario else None,
            'servico': visita.servico,
            'cliente': visita.cliente,
            'profissional': visita.profissional,
            'observacoes': visita.observacoes,
        }
        visitas_data.append(visita_data)
    
    return JsonResponse({
        'success': True,
        'total_agenda_dias': len(agenda_dias_data),
        'total_visitas': len(visitas_data),
        'agenda_dias': agenda_dias_data,
        'visitas': visitas_data,
    }, safe=False)

def pagpendentes_json(request):
    """Endpoint JSON que retorna todas as informações dos pagamentos pendentes."""
    from pagpendentes.models import PagPendente
    
    pag_pendentes = PagPendente.objects.all().select_related('local')
    
    pag_pendentes_data = []
    for pag in pag_pendentes:
        pag_data = {
            'id': pag.id,
            'local_id': pag.local.id if pag.local else None,
            'local_nome': pag.local.nome if pag.local else '',
            'data_hora': pag.data_hora.strftime('%Y-%m-%d %H:%M:%S') if pag.data_hora else None,
            'status': pag.status,
            'status_display': pag.get_status_display(),
        }
        pag_pendentes_data.append(pag_data)
    
    return JsonResponse({
        'success': True,
        'total_pag_pendentes': len(pag_pendentes_data),
        'pag_pendentes': pag_pendentes_data,
    }, safe=False)

def treinamentos_json(request):
    """Endpoint JSON que retorna todas as informações dos treinamentos."""
    from treinamentos.models import Treinamento
    
    treinamentos = Treinamento.objects.all().select_related('local', 'usuario')
    
    treinamentos_data = []
    for treinamento in treinamentos:
        treinamento_data = {
            'id': treinamento.id,
            'local_id': treinamento.local.id if treinamento.local else None,
            'local_nome': treinamento.local.nome if treinamento.local else '',
            'usuario_id': treinamento.usuario.id if treinamento.usuario else None,
            'usuario_nome': treinamento.usuario.nome if treinamento.usuario else '',
            'data_hora': treinamento.data_hora.strftime('%Y-%m-%d %H:%M:%S') if treinamento.data_hora else None,
            'status': treinamento.status,
            'status_display': treinamento.get_status_display(),
        }
        treinamentos_data.append(treinamento_data)
    
    return JsonResponse({
        'success': True,
        'total_treinamentos': len(treinamentos_data),
        'treinamentos': treinamentos_data,
    }, safe=False)

def rondas_json(request):
    """Endpoint JSON que retorna todas as informações das rondas."""
    from rondas.models import Ronda
    
    rondas = Ronda.objects.all().select_related('local')
    
    rondas_data = []
    for ronda in rondas:
        ronda_data = {
            'id': ronda.id,
            'local_id': ronda.local.id if ronda.local else None,
            'local_nome': ronda.local.nome if ronda.local else '',
            'data_hora': ronda.data_hora.strftime('%Y-%m-%d %H:%M:%S') if ronda.data_hora else None,
            'status': ronda.status,
            'status_display': ronda.get_status_display(),
            'observacoes': ronda.observacoes,
        }
        rondas_data.append(ronda_data)
    
    return JsonResponse({
        'success': True,
        'total_rondas': len(rondas_data),
        'rondas': rondas_data,
    }, safe=False)
