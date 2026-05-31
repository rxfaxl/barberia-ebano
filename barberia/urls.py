from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from barbers.models import Barber
from services.models import Service

User = get_user_model()

SERVICES_DATA = [
    {"name": "Corte Clásico", "description": "Corte tradicional con tijera y máquina, acabado perfecto para un look elegante y limpio.", "price": 20, "duration": 30},
    {"name": "Corte Degradado", "description": "Degradado moderno (fade) con difuminado progresivo. Incluye perfilado de cejas y patillas.", "price": 25, "duration": 40},
    {"name": "Barba Completa", "description": "Arreglo y perfilado de barba con navaja, toalla caliente y bálsamo hidratante.", "price": 25, "duration": 30},
    {"name": "Corte + Barba", "description": "Combo completo: corte degradado o clásico más arreglo de barba. Ahorra S/5.", "price": 30, "duration": 50},
    {"name": "Corte Infantil", "description": "Corte para niños hasta 12 años. Ambiente cómodo y paciente.", "price": 20, "duration": 25},
    {"name": "Lavado + Corte", "description": "Lavado con shampoo profesional, masaje capilar y corte personalizado.", "price": 35, "duration": 45},
]

def home(request):
    return render(request, 'home.html')

def setup(request):
    if request.GET.get("key") != "ebano2024":
        return HttpResponse("Acceso denegado", status=403)
    user, created = User.objects.get_or_create(
        username="rafael",
        defaults={
            "email": "rafael@ebano.barber",
            "password": make_password("rafael123"),
            "first_name": "Rafael",
            "last_name": "Paquirachi",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if not created:
        user.is_staff = True
        user.is_superuser = True
        user.save()
    Barber.objects.get_or_create(
        user=user,
        defaults={
            "bio": "Barbero profesional con más de 5 años de experiencia. Especialista en degradados, cortes clásicos y arreglo de barba.",
            "phone": "962305610",
            "available": True,
        },
    )
    for data in SERVICES_DATA:
        Service.objects.get_or_create(name=data["name"], defaults=data)
    return HttpResponse("OK - Usuario rafael creado, servicios y barberos listos.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('setup/', setup, name='setup'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('services/', include('services.urls')),
    path('barbers/', include('barbers.urls')),
    path('appointments/', include('appointments.urls')),
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
