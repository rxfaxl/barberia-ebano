from django.contrib import admin
from .models import Barber

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'available']
    list_filter = ['available']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
