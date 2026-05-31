from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from .models import Conversation, Message
from barbers.models import Barber
from notifications.models import Notification

@login_required
def inbox(request):
    if request.user.is_staff:
        conversations = Conversation.objects.all()
    else:
        conversations = Conversation.objects.filter(user=request.user)
    for c in conversations:
        c.unread = c.messages.filter(read=False).exclude(sender=request.user).count()
    return render(request, 'chat/inbox.html', {'conversations': conversations})

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    if not request.user.is_staff and conversation.user != request.user:
        django_messages.error(request, 'No tienes acceso a esta conversación.')
        return redirect('inbox')

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text,
            )
            conversation.save()
            barber = Barber.objects.first()
            if barber and request.user != barber.user:
                Notification.objects.create(
                    user=barber.user,
                    message=f'Nuevo mensaje de {request.user.get_full_name() or request.user.username}',
                )
        return redirect('conversation_detail', pk=pk)

    conversation.messages.filter(read=False).exclude(sender=request.user).update(read=True)

    messages_list = conversation.messages.all()
    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'messages': messages_list,
    })

@login_required
def new_conversation(request):
    barber = Barber.objects.first()
    if not barber:
        django_messages.error(request, 'No hay barberos disponibles.')
        return redirect('inbox')

    conversation, created = Conversation.objects.get_or_create(
        user=request.user,
    )

    welcome_sent = conversation.messages.filter(sender=barber.user).exists()
    if created or not welcome_sent:
        if request.user != barber.user:
            welcome = (
                '👋 Bienvenido a *ÉBANO Barber Club* ✂️\n\n'
                '🔥 Donde la precisión, el estilo y la elegancia se unen para ofrecerte una experiencia única.\n\n'
                '💈 Nuestros servicios:\n'
                '• Cortes clásicos y modernos\n'
                '• Degradados profesionales\n'
                '• Arreglo y perfilado de barba\n'
                '• Asesoramiento de imagen\n'
                '• Experiencia premium ÉBANO\n\n'
                '📅 ¿Te gustaría reservar una cita?\n'
                'Indícanos el día y la hora que prefieres, y estaremos encantados de atenderte.\n\n'
                '✨ En ÉBANO no solo realizamos cortes, construimos presencia.\n\n'
                'Te esperamos. 🤝'
            )
            Message.objects.create(
                conversation=conversation,
                sender=barber.user,
                text=welcome,
            )

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text,
            )
            barber = Barber.objects.first()
            if barber and request.user != barber.user:
                Notification.objects.create(
                    user=barber.user,
                    message=f'Nuevo mensaje de {request.user.get_full_name() or request.user.username}',
                )
            django_messages.success(request, 'Mensaje enviado.')
            return redirect('conversation_detail', pk=conversation.pk)

    return redirect('conversation_detail', pk=conversation.pk)
