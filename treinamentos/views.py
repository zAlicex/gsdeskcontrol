from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Treinamento
from .forms import TreinamentoForm
from django.db.models import Q
import json

def treinamentos(request):
    if request.method == 'POST':
        treinamento_id = request.POST.get('id')
        if treinamento_id:
            treinamento_item = get_object_or_404(Treinamento, id=treinamento_id)
            form = TreinamentoForm(request.POST, instance=treinamento_item)
        else:
            form = TreinamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('treinamentos:treinamentos')
        else:
            itens = Treinamento.objects.all()
            context = {'form': form, 'itens': itens}
            return render(request, 'treinamentos/treinamentos.html', context)

    form = TreinamentoForm()
    search_local = request.GET.get('search_local', '').strip()
    search_usuario = request.GET.get('search_usuario', '').strip()
    search_status = request.GET.get('search_status', '').strip()
    itens = Treinamento.objects.all()
    if search_local:
        itens = itens.filter(local__nome__icontains=search_local)
    if search_usuario:
        itens = itens.filter(usuario__nome__icontains=search_usuario)
    if search_status:
        itens = itens.filter(status=search_status)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and (search_local or search_usuario or search_status):
        html = render_to_string(
            'treinamentos/partials/lista_treinamentos.html', {'itens': itens}
        )
        return JsonResponse({'html': html})
    context = {
        'form': form,
        'itens': itens,
        'search_local': search_local,
        'search_usuario': search_usuario,
        'search_status': search_status,
    }
    return render(request, 'treinamentos/treinamentos.html', context)

def get_treinamento(request, treinamento_id):
    try:
        treinamento = get_object_or_404(Treinamento, id=treinamento_id)
        data = {
            'success': True,
            'treinamento': {
                'id': treinamento.id,
                'local_id': treinamento.local.id if treinamento.local else None,
                'usuario_id': treinamento.usuario.id if treinamento.usuario else None,
                'data_hora': treinamento.data_hora.strftime('%Y-%m-%dT%H:%M') if treinamento.data_hora else '',
                'status': treinamento.status,
                'status_display': treinamento.get_status_display(),
            }
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def atualizar_treinamento(request, treinamento_id):
    if request.method == 'POST':
        try:
            treinamento = get_object_or_404(Treinamento, id=treinamento_id)
            form = TreinamentoForm(request.POST, instance=treinamento)
            if form.is_valid():
                form.save()
                return redirect('treinamentos:treinamentos')
            else:
                context = {
                    'form': form,
                    'itens': Treinamento.objects.all(),
                    'search_local': request.GET.get('search_local', ''),
                    'search_usuario': request.GET.get('search_usuario', ''),
                    'search_status': request.GET.get('search_status', '')
                }
                return render(request, 'treinamentos/treinamentos.html', context)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return redirect('treinamentos:treinamentos')
