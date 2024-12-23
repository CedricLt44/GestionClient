from django.urls import path

from . import views

app_name = 'liste_client'

urlpatterns = [
    path('customers/', views.customers, name='customers'),
    path('add/', views.add, name='add'),
    path('customers/<int:pk>/', views.customer, name='detail_client'),
    path('edit/<int:pk>/', views.edit, name='edit_client'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]
