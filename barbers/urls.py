from django.urls import path
from . import views

urlpatterns = [
    path('', views.barber_list, name='barber_list'),
    path('<int:pk>/', views.barber_detail, name='barber_detail'),
    path('finanzas/', views.finance_dashboard, name='finance_dashboard'),
    path('finanzas/exportar/', views.finance_export_csv, name='finance_export_csv'),
]
