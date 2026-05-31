from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'yape_number': settings.YAPE_NUMBER,
    })

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            msg = 'Cita agendada exitosamente.'
            if appointment.payment_method == 'yape':
                msg += f' Paga con Yape al número: {settings.YAPE_NUMBER}'
            messages.success(request, msg)
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})

@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if appointment.status == 'confirmed':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Cita cancelada.')
    else:
        messages.error(request, 'No se puede cancelar esta cita.')
    return redirect('appointment_list')
