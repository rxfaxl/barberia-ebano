from django.db import models
from django.contrib.auth.models import User
from services.models import Service
from barbers.models import Barber

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]

    PAYMENT_CHOICES = [
        ('barbershop', 'Pagar en barbería'),
        ('yape', 'Yape'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='barbershop')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.user.username} - {self.service.name} - {self.date}'
