from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'barber', 'service', 'date', 'time', 'status', 'payment_method']
    list_filter = ['status', 'payment_method', 'date']
    search_fields = ['user__username', 'barber__user__first_name', 'service__name']
    date_hierarchy = 'date'
