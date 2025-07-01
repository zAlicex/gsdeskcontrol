import json
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orcamento.models import Orcamento
from clientes.models import Clientes
from django.utils import timezone
from django.http import HttpResponse
from agenda.models import Visita, AgendaDia
from orpecas.models import Orpecas
from rat.models import Rat

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'home'

        # --- KPIs ---
        thirty_days_ago = datetime.now() - timedelta(days=30)

        # Faturamento (soma de OS e Orçamentos de Peças com status relevante)
        status_faturamento = ['aprovado', 'pendente_pagamento', 'finalizado', 'PAGO']
        faturamento_os = Orcamento.objects.filter(status__in=status_faturamento).aggregate(total=Sum('valor_total_com_desconto'))['total'] or 0
        faturamento_pecas = Orpecas.objects.filter(status__in=status_faturamento).aggregate(total=Sum('valor_total_com_desconto'))['total'] or 0
        faturamento_30d = faturamento_os + faturamento_pecas

        # Novos Clientes (últimos 30 dias)
        novos_clientes_30d = Clientes.objects.filter(data_chamado__gte=thirty_days_ago).count()
        
        # Orçamentos Abertos (total)
        orcamentos_abertos = Orcamento.objects.filter(status='aberto').count()
        
        # Orçamentos Finalizados (total)
        orcamentos_finalizados = Orcamento.objects.filter(status__in=['finalizado', 'PAGO']).count()
        
        # Total de Visitas (próximos 30 dias)
        hoje = timezone.localdate()
        trinta_dias = hoje + timedelta(days=30)
        total_visitas = Visita.objects.filter(agenda__data__range=[hoje, trinta_dias]).count()

        context.update({
            'faturamento_30d': faturamento_30d,
            'novos_clientes_30d': novos_clientes_30d,
            'orcamentos_abertos': orcamentos_abertos,
            'orcamentos_finalizados': orcamentos_finalizados,
            'total_visitas': total_visitas,
        })

        # --- Top 5 Clientes por Faturamento ---
        top_clientes = Clientes.objects.annotate(
            total_gasto=Sum(
                'orcamentos__valor_total_com_desconto',
                filter=Q(orcamentos__status__in=['aprovado', 'finalizado'])
            )
        ).filter(total_gasto__isnull=False).order_by('-total_gasto')[:5]
        
        context['top_clientes'] = top_clientes

        # --- Dados para Gráficos ---
        # Faturamento mensal (últimos 6 meses)
        faturamento_mensal_data = self.get_faturamento_mensal()
        context['faturamento_chart_data'] = json.dumps(faturamento_mensal_data)

        # Status de Orçamentos
        status_orcamentos_data = self.get_status_orcamentos()
        context['status_chart_data'] = json.dumps(status_orcamentos_data)

        # Projeção de Faturamento (Próximos 3 meses)
        projecao_faturamento_data = self.get_projecao_faturamento()
        context['projecao_chart_data'] = json.dumps(projecao_faturamento_data)

        return context

    def get_faturamento_mensal(self):
        six_months_ago = datetime.now() - timedelta(days=180)
        faturamento_mensal = Orcamento.objects.filter(
            status__in=['aprovado', 'finalizado'],
            data__gte=six_months_ago
        ).annotate(month=TruncMonth('data')) \
         .values('month') \
         .annotate(total=Sum('valor_total_com_desconto')) \
         .order_by('month')
        
        return self.prepare_chart_data(faturamento_mensal, 'total')

    def get_status_orcamentos(self):
        # Soma dos valores por status
        status_sums = Orcamento.objects.values('status').annotate(total=Sum('valor_total_com_desconto'))
        status_map = {
            'aberto': 'Abertos',
            'aprovado': 'Aprovados',
            'cancelado': 'Cancelados',
            'finalizado': 'Finalizados',
            'pendente_pagamento': 'Pendentes',
            'PAGO': 'Pagos',
        }
        labels = [status_map.get(s['status'], s['status']) for s in status_sums]
        data = [float(s['total'] or 0) for s in status_sums]
        return {'labels': labels, 'data': data}

    def prepare_chart_data(self, queryset, value_field):
        labels = []
        data = []
        months_data = {item['month'].strftime('%Y-%m-01'): item[value_field] for item in queryset}
        
        current_date = datetime.now()
        for i in range(5, -1, -1):
            month_date = current_date - timedelta(days=i*30)
            month_key = month_date.strftime('%Y-%m-01')
            month_label = month_date.strftime('%b/%y')
            
            labels.append(month_label)
            value = months_data.get(month_key, 0)
            data.append(float(value))
            
        return {'labels': labels, 'data': data}

    def get_projecao_faturamento(self):
        today = timezone.now().date()
        # Próximos 90 dias
        three_months_from_now = today + timedelta(days=90)
        
        # Filtra orçamentos aprovados com data futura
        projecao = Orcamento.objects.filter(
            status='aprovado',
            data__range=[today, three_months_from_now] 
        ).annotate(
            year=ExtractYear('data'),
            month=ExtractMonth('data')
        ).values('year', 'month') \
         .annotate(total=Sum('valor_total_com_desconto')) \
         .order_by('year', 'month')

        labels = []
        data = []
        # Formata os dados para o gráfico
        for item in projecao:
            # Cria um objeto de data para formatação
            month_date = datetime(item['year'], item['month'], 1)
            labels.append(month_date.strftime('%b/%y'))
            data.append(float(item['total']))
        
        return {'labels': labels, 'data': data}

def index(request):
    return render(request, 'index.html')






