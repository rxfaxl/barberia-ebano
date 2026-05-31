from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('read/<int:pk>/', views.notification_read, name='notification_read'),
]
