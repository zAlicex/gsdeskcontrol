from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Ocorrencia
from .forms import OcorrenciaForm
from clientes.models import Clientes
from django.core import serializers
import json

class OcorrenciasView(View):
    def get(self, request):
        search_local = request.GET.get('search_local')
        search_status = request.GET.get('search_status')
        ocorrencias = Ocorrencia.objects.all()
        
        if search_local:
            ocorrencias = ocorrencias.filter(local__nome__icontains=search_local)
        if search_status:
            ocorrencias = ocorrencias.filter(status=search_status)
            
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                'ocorrencias/partials/lista_ocorrencias.html',
                {'ocorrencias': ocorrencias}
            )
            return JsonResponse({'html': html})
            
        form = OcorrenciaForm()
        clientes = Clientes.objects.all()
        context = {
            'ocorrencias': ocorrencias,
            'form': form,
            'clientes': clientes,
            'search_local': search_local or '',
            'search_status': search_status or '',
        }
        return render(request, 'ocorrencias/ocorrencias.html', context)

    def post(self, request):
        form = OcorrenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ocorrencias:ocorrencias')
        ocorrencias = Ocorrencia.objects.all()
        clientes = Clientes.objects.all()
        context = {
            'ocorrencias': ocorrencias,
            'form': form,
            'clientes': clientes,
        }
        return render(request, 'ocorrencias/ocorrencias.html', context)

def get_ocorrencia(request, ocorrencia_id):
    try:
        ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
        ocorrencia_data = {
            'success': True,
            'ocorrencia': {
                'id': ocorrencia.id,
                'local': ocorrencia.local.id if ocorrencia.local else None,
                'local_nome': ocorrencia.local.nome if ocorrencia.local else '',
                'data_hora': ocorrencia.data_hora.strftime('%Y-%m-%dT%H:%M') if ocorrencia.data_hora else '',
                'status': ocorrencia.status,
                'observacoes': ocorrencia.observacoes,
            }
        }
        return JsonResponse(ocorrencia_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def atualizar_ocorrencia(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
    if request.method == 'POST':
        form = OcorrenciaForm(request.POST, instance=ocorrencia)
        if form.is_valid():
            form.save()
            return redirect('ocorrencias:ocorrencias')
    return redirect('ocorrencias:ocorrencias')

def excluir_ocorrencia(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, id=ocorrencia_id)
    if request.method == 'POST':
        ocorrencia.delete()
        return redirect('ocorrencias:ocorrencias')
    return redirect('ocorrencias:ocorrencias')
