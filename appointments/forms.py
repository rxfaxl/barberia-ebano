from django import forms
from .models import Appointment
from services.models import Service
from barbers.models import Barber

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['barber', 'service', 'date', 'time', 'payment_method', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['barber'].queryset = Barber.objects.filter(available=True)
        self.fields['service'].queryset = Service.objects.filter(available=True)
        self.fields['payment_method'].label = 'Método de pago'
        self.fields['payment_method'].widget = forms.RadioSelect(choices=Appointment.PAYMENT_CHOICES)
