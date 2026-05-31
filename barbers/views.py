from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import HttpResponse
import csv
from datetime import timedelta
from calendar import monthrange
from .models import Barber
from appointments.models import Appointment


def barber_list(request):
    barbers = Barber.objects.filter(available=True)
    return render(request, 'barbers/barber_list.html', {'barbers': barbers})


def barber_detail(request, pk):
    barber = get_object_or_404(Barber, pk=pk)
    return render(request, 'barbers/barber_detail.html', {'barber': barber})


@staff_member_required
def finance_dashboard(request):
    today = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)

    base = Appointment.objects.filter(status__in=['confirmed', 'completed'])
    cancelled = Appointment.objects.filter(status='cancelled')
    all_qs = base
    today_qs = base.filter(date=today)
    week_qs = base.filter(date__gte=start_week)
    month_qs = base.filter(date__gte=start_month)

    def totals(qs):
        return qs.aggregate(total=Sum('service__price'), count=Count('id'))

    all_totals = totals(all_qs)
    today_totals = totals(today_qs)
    week_totals = totals(week_qs)
    month_totals = totals(month_qs)
    cancelled_totals = totals(cancelled)

    by_method = base.values('payment_method').annotate(
        total=Sum('service__price'), count=Count('id'),
    )

    week_days = []
    for i in range(7):
        day = start_week + timedelta(days=i)
        day_qs = base.filter(date=day)
        dt = totals(day_qs)
        week_days.append({
            'label': day.strftime('%a'),
            'date': day.strftime('%d/%m'),
            'total': dt['total'] or 0,
            'count': dt['count'] or 0,
        })

    months_data = []
    for i in range(5, -1, -1):
        y = today.year
        m = today.month - i
        if m <= 0:
            m += 12
            y -= 1
        _, last_day = monthrange(y, m)
        month_start = timezone.datetime(y, m, 1).date()
        month_end = timezone.datetime(y, m, last_day).date()
        month_qs = base.filter(date__gte=month_start, date__lte=month_end)
        dt = totals(month_qs)
        months_data.append({
            'label': timezone.datetime(y, m, 1).strftime('%b'),
            'total': float(dt['total'] or 0),
            'count': dt['count'] or 0,
        })
    max_month_total = max((m['total'] for m in months_data), default=1)

    by_service = base.values('service__name').annotate(
        total=Sum('service__price'), count=Count('id'),
    ).order_by('-total')[:5]
    max_service_total = float(by_service[0]['total']) if by_service else 1

    by_status = Appointment.objects.values('status').annotate(
        count=Count('id'),
    )
    status_counts = {s['status']: s['count'] for s in by_status}

    recent = base.order_by('-date', '-time')[:20]

    return render(request, 'barbers/finance.html', {
        'all_totals': all_totals,
        'today_totals': today_totals,
        'week_totals': week_totals,
        'month_totals': month_totals,
        'cancelled_totals': cancelled_totals,
        'by_method': by_method,
        'week_days': week_days,
        'months_data': months_data,
        'max_month_total': max_month_total,
        'by_service': by_service,
        'max_service_total': max_service_total,
        'status_counts': status_counts,
        'recent': recent,
    })


@staff_member_required
def finance_export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="finanzas_ebano.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Cliente', 'Servicio', 'Monto', 'Pago', 'Estado', 'Notas'])
    qs = Appointment.objects.filter(status__in=['confirmed', 'completed']).order_by('-date', '-time')
    for a in qs:
        writer.writerow([
            a.date.strftime('%d/%m/%Y'),
            a.user.get_full_name() or a.user.username,
            a.service.name,
            float(a.service.price),
            a.get_payment_method_display(),
            a.get_status_display(),
            a.notes,
        ])
    return response
