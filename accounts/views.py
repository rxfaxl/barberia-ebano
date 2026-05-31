from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import logging
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Cuenta creada exitosamente.')
                return redirect('home')
            except IntegrityError as e:
                logger.error(f'Error creating user: {e}')
                messages.error(request, 'Error al crear la cuenta. El usuario o email ya existe.')
            except Exception as e:
                logger.error(f'Unexpected error during registration: {e}')
                messages.error(request, 'Error inesperado al crear la cuenta. Intenta de nuevo.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'u_form': u_form, 'p_form': p_form})
