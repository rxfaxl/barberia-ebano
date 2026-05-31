from django.shortcuts import redirect
from django.contrib import messages

def payment_success(request):
    messages.success(request, 'Pago registrado.')
    return redirect('appointment_list')

def payment_cancel(request):
    messages.error(request, 'Pago cancelado.')
    return redirect('appointment_list')
