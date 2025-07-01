from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Ronda
from .forms import RondaForm
from django.db.models import Q
import json

def rondas(request):
    if request.method == 'POST':
        ronda_id = request.POST.get('id')
        if ronda_id:
            ronda_item = get_object_or_404(Ronda, id=ronda_id)
            form = RondaForm(request.POST, instance=ronda_item)
        else:
            form = RondaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rondas:rondas')
        else:
            itens = Ronda.objects.all()
            context = {'form': form, 'itens': itens}
            return render(request, 'rondas/rondas.html', context)

    form = RondaForm()
    search_local = request.GET.get('search_local', '').strip()
    search_status = request.GET.get('search_status', '').strip()
    itens = Ronda.objects.all()
    if search_local:
        itens = itens.filter(local__nome__icontains=search_local)
    if search_status:
        itens = itens.filter(status=search_status)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and (search_local or search_status):
        html = render_to_string(
            'rondas/partials/lista_rondas.html', {'itens': itens}
        )
        return JsonResponse({'html': html})
    context = {
        'form': form,
        'itens': itens,
        'search_local': search_local,
        'search_status': search_status,
    }
    return render(request, 'rondas/rondas.html', context)

def get_ronda(request, ronda_id):
    try:
        ronda = get_object_or_404(Ronda, id=ronda_id)
        data = {
            'success': True,
            'ronda': {
                'id': ronda.id,
                'local_id': ronda.local.id if ronda.local else None,
                'data_hora': ronda.data_hora.strftime('%Y-%m-%dT%H:%M') if ronda.data_hora else '',
                'status': ronda.status,
                'observacoes': ronda.observacoes,
                'status_display': ronda.get_status_display(),
            }
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def atualizar_ronda(request, ronda_id):
    if request.method == 'POST':
        try:
            ronda = get_object_or_404(Ronda, id=ronda_id)
            form = RondaForm(request.POST, instance=ronda)
            if form.is_valid():
                form.save()
                return redirect('rondas:rondas')
            else:
                context = {
                    'form': form,
                    'itens': Ronda.objects.all(),
                    'search_local': request.GET.get('search_local', ''),
                    'search_status': request.GET.get('search_status', '')
                }
                return render(request, 'rondas/rondas.html', context)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return redirect('rondas:rondas')
