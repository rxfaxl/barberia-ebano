from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('conversacion/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('nuevo/', views.new_conversation, name='new_conversation'),
]
