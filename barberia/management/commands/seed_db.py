from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from barbers.models import Barber
from services.models import Service
from django.contrib.auth.hashers import make_password

User = get_user_model()

SERVICES_DATA = [
    {"name": "Corte Clásico", "description": "Corte tradicional con tijera y máquina, acabado perfecto para un look elegante y limpio.", "price": 20, "duration": 30},
    {"name": "Corte Degradado", "description": "Degradado moderno (fade) con difuminado progresivo. Incluye perfilado de cejas y patillas.", "price": 25, "duration": 40},
    {"name": "Barba Completa", "description": "Arreglo y perfilado de barba con navaja, toalla caliente y bálsamo hidratante.", "price": 25, "duration": 30},
    {"name": "Corte + Barba", "description": "Combo completo: corte degradado o clásico más arreglo de barba. Ahorra S/5.", "price": 30, "duration": 50},
    {"name": "Corte Infantil", "description": "Corte para niños hasta 12 años. Ambiente cómodo y paciente.", "price": 20, "duration": 25},
    {"name": "Lavado + Corte", "description": "Lavado con shampoo profesional, masaje capilar y corte personalizado.", "price": 35, "duration": 45},
]

class Command(BaseCommand):
    help = "Crea el usuario barber/admin y datos iniciales"

    def handle(self, *args, **options):
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
        if created:
            self.stdout.write(self.style.SUCCESS(f"Usuario 'rafael' creado"))
        else:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(f"Usuario 'rafael' ya existía, actualizado")

        barber, barber_created = Barber.objects.get_or_create(
            user=user,
            defaults={
                "bio": "Barbero profesional con más de 5 años de experiencia. Especialista en degradados, cortes clásicos y arreglo de barba. Apasionado por brindar una experiencia única a cada cliente.",
                "phone": "962305610",
                "available": True,
            },
        )
        if barber_created:
            self.stdout.write(self.style.SUCCESS(f"Perfil de barbero creado para Rafael"))
        else:
            self.stdout.write(f"Perfil de barbero ya existía")

        for data in SERVICES_DATA:
            _, svc_created = Service.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )
            if svc_created:
                self.stdout.write(f"  Servicio creado: {data['name']}")

        self.stdout.write(self.style.SUCCESS("Seed completado"))
