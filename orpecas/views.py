from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Orpecas
from .forms import OrpecasForm

class OrpecasView(View):
    def get(self, request):
        search_local = request.GET.get('search_local', '')
        search_diagnostico = request.GET.get('search_diagnostico', '')

        orpecas_list = Orpecas.objects.all()

        if search_local:
            orpecas_list = orpecas_list.filter(local__nome__icontains=search_local)
        
        if search_diagnostico:
            orpecas_list = orpecas_list.filter(diagnostico__icontains=search_diagnostico)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                'orpecas/partials/lista_orpecas.html',
                {'orpecas_list': orpecas_list}
            )
            return JsonResponse({'html': html})

        form = OrpecasForm()
        context = {
            'orpecas_list': orpecas_list,
            'form': form,
            'search_local': search_local,
            'search_diagnostico': search_diagnostico,
        }
        return render(request, 'orpecas/orpecas.html', context)

    def post(self, request):
        form = OrpecasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orpecas:orpecas')
        
        # Se inválido, renderiza novamente com erros
        orpecas_list = Orpecas.objects.all()
        context = {'orpecas_list': orpecas_list, 'form': form}
        return render(request, 'orpecas/orpecas.html', context)

def get_orpecas(request, orpecas_id):
    orpecas = get_object_or_404(Orpecas, id=orpecas_id)
    data = {
        'success': True,
        'orpecas': {
            'id': orpecas.id,
            'local': orpecas.local.id if orpecas.local else '',
            'diagnostico': orpecas.diagnostico or '',
            'botao_panico': orpecas.botao_panico or '',
            'sensor': orpecas.sensor or '',
        }
    }
    return JsonResponse(data)

def atualizar_orpecas(request, orpecas_id):
    orpecas = get_object_or_404(Orpecas, id=orpecas_id)
    if request.method == 'POST':
        form = OrpecasForm(request.POST, instance=orpecas)
        if form.is_valid():
            form.save()
            return redirect('orpecas:orpecas')
    return redirect('orpecas:orpecas')

def excluir_orpecas(request, orpecas_id):
    orpecas = get_object_or_404(Orpecas, id=orpecas_id)
    if request.method == 'POST':
        orpecas.delete()
    return redirect('orpecas:orpecas')
