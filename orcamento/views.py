from django.shortcuts import render, redirect, get_object_or_404
from .models import Orcamento
from .forms import OrcamentoForm
from django.http import JsonResponse

def lista_orcamentos(request):
    if request.method == 'POST':
        # Verifica se é uma edição ou novo orçamento
        orcamento_id = request.POST.get('orcamento_id')
        if orcamento_id:
            # Edição
            orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
            form = OrcamentoForm(request.POST, request.FILES, instance=orcamento)
        else:
            # Novo orçamento
            form = OrcamentoForm(request.POST, request.FILES)
        
        if form.is_valid():
            orcamento = form.save()
            print(f"Orçamento salvo com sucesso: {orcamento}")  # Debug
            return redirect('orcamento:lista_orcamentos')
        else:
            print(f"Erros no formulário: {form.errors}")  # Debug
    else:
        form = OrcamentoForm()
    
    orcamentos = Orcamento.objects.all().order_by('-id')
    return render(request, 'orcamento/orcamento.html', {'orcamentos': orcamentos, 'form': form})

def novo_orcamento(request):
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, request.FILES)
        if form.is_valid():
            orcamento = form.save()
            print(f"Orçamento salvo com sucesso: {orcamento}")  # Debug
            return redirect('orcamento:lista_orcamentos')
        else:
            print(f"Erros no formulário: {form.errors}")  # Debug
            return render(request, 'orcamento/novo_orcamento.html', {'form': form})
    else:
        form = OrcamentoForm()
    return render(request, 'orcamento/novo_orcamento.html', {'form': form})

def editar_orcamento(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, request.FILES, instance=orcamento)
        if form.is_valid():
            form.save()
            return redirect('orcamento:lista_orcamentos')
    else:
        form = OrcamentoForm(instance=orcamento)
    return render(request, 'orcamento/novo_orcamento.html', {'form': form, 'orcamento': orcamento})

def get_orcamento_data(request, pk):
    """View para retornar dados do orçamento em formato JSON"""
    print(f"DEBUG: get_orcamento_data chamada com pk={pk}")
    try:
        orcamento = get_object_or_404(Orcamento, pk=pk)
        print(f"DEBUG: Orçamento encontrado: {orcamento}")
        data = {
            'success': True,
            'orcamento': {
                'id': orcamento.id,
                'nome_local': orcamento.nome_local.id if orcamento.nome_local else '',
                'nome_usuarios': orcamento.nome_usuarios.id if orcamento.nome_usuarios else '',
                'data_acionamento': orcamento.data_acionamento.strftime('%Y-%m-%dT%H:%M') if orcamento.data_acionamento else '',
                'data_chegada': orcamento.data_chegada.strftime('%Y-%m-%dT%H:%M') if orcamento.data_chegada else '',
                'sla_resposta': str(orcamento.sla_resposta) if orcamento.sla_resposta else '0.00',
            }
        }
        print(f"DEBUG: Dados retornados: {data}")
        return JsonResponse(data)
    except Exception as e:
        print(f"DEBUG: Erro na view get_orcamento_data: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def acionamentos_json(request):
    """
    Endpoint JSON que retorna todas as informações dos acionamentos (orçamentos).
    """
    orcamentos = Orcamento.objects.all().order_by('-data_acionamento')
    
    data = []
    for orcamento in orcamentos:
        orcamento_data = {
            'id': orcamento.id,
            'nome_local_id': orcamento.nome_local.id if orcamento.nome_local else None,
            'nome_local_nome': orcamento.nome_local.nome if orcamento.nome_local else '',
            'nome_usuarios_id': orcamento.nome_usuarios.id if orcamento.nome_usuarios else None,
            'nome_usuarios_nome': orcamento.nome_usuarios.nome if orcamento.nome_usuarios else '',
            'data_acionamento': orcamento.data_acionamento.strftime('%Y-%m-%d %H:%M') if orcamento.data_acionamento else None,
            'data_chegada': orcamento.data_chegada.strftime('%Y-%m-%d %H:%M') if orcamento.data_chegada else None,
            'sla_resposta': str(orcamento.sla_resposta) if orcamento.sla_resposta else '0.00',
            'imagem_url': orcamento.imagem.url if orcamento.imagem else None,
            'imagem_nome': orcamento.imagem.name if orcamento.imagem else None,
        }
        data.append(orcamento_data)
    
    return JsonResponse({
        'success': True,
        'total_acionamentos': len(data),
        'acionamentos': data
    }, safe=False)